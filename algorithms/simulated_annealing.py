"""
Algorithm E: Simulated Annealing (SA) Metaheuristic.
Course Reference: CSDX 507 Decision-Making for Data Science - Module V.
Implements a genuine trajectory-based neighborhood search metaheuristic with
Metropolis acceptance criterion and geometric cooling schedule (T_{k+1} = alpha * T_k).
Maintains strict solution feasibility throughout neighbor generation.
"""

import time
import math
import random
import numpy as np
from typing import Dict, Any, List, Tuple

from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    compute_metrics_and_summary
)

def solve_simulated_annealing(
    problem: OptimizationProblem,
    initial_temp: float = 100.0,
    cooling_rate: float = 0.94,
    min_temp: float = 0.05,
    steps_per_temp: int = 15,
    seed: int = 42
) -> OptimizationResult:
    """
    Executes Simulated Annealing to optimize resource allocation.
    Neighbor Operator: Selects a donor region i and a recipient region j for resource r,
    and shifts delta units while strictly respecting demand ceilings and supply bounds.
    Acceptance:
      If Delta_E < 0: accept move.
      Else: accept with probability P = exp(-Delta_E / T).
    """
    start_time = time.time()
    random.seed(seed)
    np.random.seed(seed)

    regions = problem.regions
    resources = problem.resources
    num_regions = len(regions)
    num_resources = len(resources)
    urgency_scores = problem.compute_urgency_scores()

    demand_mapping = {
        "Clean Drinking Water": "water_demand",
        "Ready-to-Eat Food Packets": "food_demand",
        "Emergency Medical Kits": "med_demand",
        "Temporary Emergency Shelters": "shelter_demand"
    }

    # Demands and supplies
    demands = np.zeros((num_regions, num_resources))
    supplies = np.zeros(num_resources)

    for r, res in enumerate(resources):
        supplies[r] = float(res["total_available"])
        key = demand_mapping.get(res["name"], "water_demand")
        for i, reg in enumerate(regions):
            demands[i, r] = float(reg.get(key, 0.0))

    # --- Initial Feasible Solution (Proportional Allocation) ---
    current_alloc = np.zeros((num_regions, num_resources))
    for r in range(num_resources):
        tot_dem = np.sum(demands[:, r])
        ratio = min(1.0, supplies[r] / tot_dem) if tot_dem > 0 else 0.0
        current_alloc[:, r] = demands[:, r] * ratio

    # --- Energy Function (Negative Utility) ---
    def compute_energy(alloc: np.ndarray) -> float:
        utility = 0.0
        for i, reg in enumerate(regions):
            u_score = urgency_scores.get(reg["name"], 0.5)
            dist_km = float(reg["distance_km"])
            acc = float(reg["accessibility_score"])

            for r in range(num_resources):
                dem = demands[i, r]
                if dem > 0:
                    pct_met = alloc[i, r] / dem
                    utility += (1.0 + u_score * 3.0) * pct_met * 10.0

            # Small accessibility-weighted transport penalty
            utility -= (dist_km / 100.0) * (1.0 - acc) * 0.4

        return -utility  # Minimize energy to maximize utility

    current_energy = compute_energy(current_alloc)
    best_alloc = np.copy(current_alloc)
    best_energy = current_energy

    # Tracking metrics
    cooling_history = []
    accepted_moves = 0
    rejected_moves = 0

    temperature = initial_temp
    iteration = 0

    while temperature > min_temp:
        for _ in range(steps_per_temp):
            iteration += 1

            # Pick random resource
            r = random.randint(0, num_resources - 1)

            # Pick random donor and recipient regions
            i = random.randint(0, num_regions - 1)
            j = random.randint(0, num_regions - 1)
            if i == j:
                continue

            donor_current = current_alloc[i, r]
            recipient_room = demands[j, r] - current_alloc[j, r]

            if donor_current <= 0 or recipient_room <= 0:
                continue

            # Step size scaled by temperature
            max_transfer = min(donor_current, recipient_room)
            step_fraction = random.uniform(0.05, 0.35)
            transfer_qty = max_transfer * step_fraction

            # Generate candidate neighbor
            candidate_alloc = np.copy(current_alloc)
            candidate_alloc[i, r] -= transfer_qty
            candidate_alloc[j, r] += transfer_qty

            candidate_energy = compute_energy(candidate_alloc)
            delta_e = candidate_energy - current_energy

            # Metropolis acceptance
            if delta_e < 0:
                # Improving move
                current_alloc = candidate_alloc
                current_energy = candidate_energy
                accepted_moves += 1
                if current_energy < best_energy:
                    best_energy = current_energy
                    best_alloc = np.copy(current_alloc)
            else:
                # Worsening move: accept with probability exp(-delta_e / T)
                prob = math.exp(-delta_e / max(temperature, 1e-6))
                if random.random() < prob:
                    current_alloc = candidate_alloc
                    current_energy = candidate_energy
                    accepted_moves += 1
                else:
                    rejected_moves += 1

        cooling_history.append({
            "iteration": iteration,
            "temperature": round(float(temperature), 2),
            "energy": round(float(current_energy), 3),
            "best_energy": round(float(best_energy), 3),
            "acceptance_rate": round((accepted_moves / max(1, accepted_moves + rejected_moves)) * 100.0, 1)
        })

        temperature *= cooling_rate

    exec_time = time.time() - start_time

    # Build final allocation matrix
    allocation_matrix: Dict[str, Dict[str, float]] = {r["name"]: {} for r in regions}
    for i, reg in enumerate(regions):
        r_name = reg["name"]
        for r, res in enumerate(resources):
            allocation_matrix[r_name][res["name"]] = round(float(best_alloc[i, r]), 1)

    from algorithms.linear_programming import _allocate_fleet_and_teams_proportional
    vehicle_allocation, team_allocation = _allocate_fleet_and_teams_proportional(problem, urgency_scores)

    result = compute_metrics_and_summary(
        problem=problem,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        execution_time_sec=exec_time,
        algorithm_name="Simulated Annealing (Metropolis Search)",
        objective_val=-best_energy
    )

    result.convergence_history = cooling_history
    result.summary["initial_temp"] = initial_temp
    result.summary["cooling_rate"] = cooling_rate
    result.summary["total_iterations"] = iteration
    result.summary["accepted_moves"] = accepted_moves
    result.summary["rejected_moves"] = rejected_moves
    result.summary["final_acceptance_pct"] = round((accepted_moves / max(1, accepted_moves + rejected_moves)) * 100.0, 1)
    result.summary["method"] = "Neighborhood Trajectory Metaheuristic (Module V)"

    return result
