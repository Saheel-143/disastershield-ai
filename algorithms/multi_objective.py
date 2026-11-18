"""
Algorithm F: Multi-Objective Optimization (MOO) using NSGA-II.
Course Reference: CSDX 507 Decision-Making for Data Science - Module V.
Uses pymoo to solve simultaneous conflicting objectives:
  1. Minimize Total Delivery Time / Latency (Urgency-Weighted Hours)
  2. Minimize Total Operational & Distribution Cost (USD)
  3. Minimize Resource Shortage / Unmet Demand (Maximizing Fulfilled Demand)
Generates non-dominated Pareto front and extracts compromise solution via TOPSIS/Euclidean ideal.
"""

import time
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination

from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    compute_metrics_and_summary
)

class DisasterAllocationProblem(ElementwiseProblem):
    """Pymoo Elementwise Problem definition for Disaster Resource Allocation."""

    def __init__(self, problem: OptimizationProblem):
        self.opt_prob = problem
        self.regions = problem.regions
        self.resources = problem.resources
        self.num_regions = len(self.regions)
        self.num_resources = len(self.resources)
        self.urgency_scores = problem.compute_urgency_scores()

        demand_mapping = {
            "Clean Drinking Water": "water_demand",
            "Ready-to-Eat Food Packets": "food_demand",
            "Emergency Medical Kits": "med_demand",
            "Temporary Emergency Shelters": "shelter_demand"
        }

        self.demands = np.zeros((self.num_regions, self.num_resources))
        self.supplies = np.zeros(self.num_resources)
        self.unit_costs = np.zeros(self.num_resources)

        for r, res in enumerate(self.resources):
            self.supplies[r] = float(res["total_available"])
            self.unit_costs[r] = float(res["unit_cost"])
            key = demand_mapping.get(res["name"], "water_demand")
            for i, reg in enumerate(self.regions):
                self.demands[i, r] = float(reg.get(key, 0.0))

        # Upper bounds for variables: x_{i, r} in [0, Demand_{i, r}]
        xl = np.zeros(self.num_regions * self.num_resources)
        xu = self.demands.flatten()

        super().__init__(
            n_var=self.num_regions * self.num_resources,
            n_obj=3,                      # 3 conflicting objectives
            n_ieq_constr=self.num_resources, # Resource supply limits
            xl=xl,
            xu=xu
        )

    def _evaluate(self, x, out, *args, **kwargs):
        alloc = x.reshape((self.num_regions, self.num_resources))

        # Objective 1: Delivery Latency (weighted hours)
        total_latency = 0.0
        # Objective 2: Total Distribution & Material Cost
        total_cost = 0.0
        # Objective 3: Shortage (Unmet Demand Units)
        total_shortage = 0.0

        for i, reg in enumerate(self.regions):
            u_score = self.urgency_scores.get(reg["name"], 0.5)
            travel_hours = float(reg["travel_time_hours"])
            acc = max(0.15, float(reg["accessibility_score"]))
            dist_km = float(reg["distance_km"])

            eff_time = travel_hours / acc

            for r in range(self.num_resources):
                allocated_qty = alloc[i, r]
                dem = self.demands[i, r]
                cost_unit = self.unit_costs[r]

                total_cost += allocated_qty * cost_unit
                total_shortage += max(0.0, dem - allocated_qty)

                # Latency weighted by allocated critical shipments
                if allocated_qty > 0:
                    total_latency += eff_time * (1.0 + u_score)

        # Transport fleet mileage cost
        total_cost += (total_latency * 15.0)

        # Constraints: Sum_{i} alloc_{i, r} - Supply_r <= 0
        g = np.zeros(self.num_resources)
        for r in range(self.num_resources):
            g[r] = np.sum(alloc[:, r]) - self.supplies[r]

        out["F"] = [total_latency, total_cost, total_shortage]
        out["G"] = g


def solve_multi_objective(
    problem: OptimizationProblem,
    pop_size: int = 30,
    n_gen: int = 25,
    seed: int = 42
) -> OptimizationResult:
    """
    Solves Multi-Objective Optimization using pymoo NSGA-II.
    Extracts Pareto front, computes Ideal Point (Utopia) compromise,
    and returns rich trade-off metrics.
    """
    start_time = time.time()

    moo_prob = DisasterAllocationProblem(problem)

    algorithm = NSGA2(
        pop_size=pop_size,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.8, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    termination = get_termination("n_gen", n_gen)

    res = minimize(
        moo_prob,
        algorithm,
        termination,
        seed=seed,
        save_history=False,
        verbose=False
    )

    exec_time = time.time() - start_time

    # Collect Pareto Front
    pareto_F = res.F  # Shape: (N_pareto, 3)
    pareto_X = res.X  # Shape: (N_pareto, N_vars)

    # Find Best Compromise Solution using Min-Distance to Ideal Point
    # Normalize objectives across Pareto set
    f_min = np.min(pareto_F, axis=0)
    f_max = np.max(pareto_F, axis=0)
    f_range = np.where(f_max - f_min > 1e-6, f_max - f_min, 1.0)

    f_normalized = (pareto_F - f_min) / f_range
    # Euclidean distance to ideal point [0, 0, 0]
    distances = np.linalg.norm(f_normalized, axis=1)
    best_idx = int(np.argmin(distances))

    best_x = pareto_X[best_idx]
    best_f = pareto_F[best_idx]

    # Convert best compromise to allocation matrix
    best_alloc = best_x.reshape((moo_prob.num_regions, moo_prob.num_resources))

    # Repair small float numerical artifacts if any
    for r in range(moo_prob.num_resources):
        tot = np.sum(best_alloc[:, r])
        if tot > moo_prob.supplies[r]:
            best_alloc[:, r] *= (moo_prob.supplies[r] / tot)
    best_alloc = np.minimum(best_alloc, moo_prob.demands)
    best_alloc = np.maximum(best_alloc, 0.0)

    allocation_matrix: Dict[str, Dict[str, float]] = {r["name"]: {} for r in problem.regions}
    for i, reg in enumerate(problem.regions):
        r_name = reg["name"]
        for r, resource in enumerate(problem.resources):
            allocation_matrix[r_name][resource["name"]] = round(float(best_alloc[i, r]), 1)

    from algorithms.linear_programming import _allocate_fleet_and_teams_proportional
    vehicle_allocation, team_allocation = _allocate_fleet_and_teams_proportional(problem, moo_prob.urgency_scores)

    result = compute_metrics_and_summary(
        problem=problem,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        execution_time_sec=exec_time,
        algorithm_name="Multi-Objective (NSGA-II Pareto)",
        objective_val=float(best_f[2]) # Shortage value
    )

    # Format Pareto solutions for Plotly visualization
    pareto_points = []
    for idx, (f_vec, dist) in enumerate(zip(pareto_F, distances)):
        pareto_points.append({
            "solution_id": idx + 1,
            "delivery_latency_hrs": round(float(f_vec[0]), 2),
            "total_cost_usd": round(float(f_vec[1]), 2),
            "unmet_shortage_units": round(float(f_vec[2]), 1),
            "is_compromise_knee_point": (idx == best_idx)
        })

    result.summary["num_pareto_solutions"] = len(pareto_points)
    result.summary["pareto_solutions"] = pareto_points
    result.summary["knee_point_tradeoff"] = {
        "latency_hrs": round(float(best_f[0]), 2),
        "cost_usd": round(float(best_f[1]), 2),
        "shortage_units": round(float(best_f[2]), 1)
    }
    result.summary["method"] = "Non-dominated Sorting Genetic Algorithm II (Module V)"

    return result
