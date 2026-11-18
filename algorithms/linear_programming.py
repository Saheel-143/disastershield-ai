"""
Algorithm A: Linear Programming (LP) Resource Allocation.
Course Reference: CSDX 507 Decision-Making for Data Science - Module IV.
Uses SciPy optimize linprog (HiGHS Simplex solver) to maximize weighted fulfilled demand
subject to inventory supply, regional demand, and road accessibility constraints.
"""

import time
import numpy as np
from scipy.optimize import linprog
from typing import Dict, Any, Tuple, List

from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    compute_metrics_and_summary
)

def solve_linear_programming(problem: OptimizationProblem) -> OptimizationResult:
    """
    Solves continuous resource allocation using SciPy Linear Programming.
    Objective:
      Maximize: Sum_{i in Regions} Sum_{r in Resources} [ Priority_r * Urgency_i * (x_{i,r} / Demand_{i,r}) ]
      - lambda * Sum_{i, r} [ (Distance_i / 100) * (Cost_r / 100) * x_{i,r} ]
    Subject to:
      1. Supply: Sum_{i} x_{i,r} <= Total_Available_r,  for all r
      2. Regional bounds: 0 <= x_{i,r} <= Demand_{i,r}, for all i, r
    """
    start_time = time.time()

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

    # Total decision variables: num_regions * num_resources
    # Index mapping: var_idx(i, r) = i * num_resources + r
    num_vars = num_regions * num_resources

    # Objective Vector c (SciPy minimizes c^T * x, so we negate our maximization objective)
    c = np.zeros(num_vars)
    bounds = []

    # Prepare objective coefficients and upper bounds
    for i, reg in enumerate(regions):
        r_name = reg["name"]
        u_score = urgency_scores.get(r_name, 0.5)
        dist_km = float(reg["distance_km"])

        for r, res in enumerate(resources):
            res_name = res["name"]
            key = demand_mapping.get(res_name, "water_demand")
            dem = float(reg.get(key, 100.0))
            priority = float(res.get("priority_weight", 1.0))
            unit_cost = float(res.get("unit_cost", 1.0))

            idx = i * num_resources + r

            # Normalized utility term: how much utility 1 unit of resource brings to this region
            # (Weight * Urgency) / Demand
            benefit_per_unit = (priority * (1.0 + u_score * 2.0)) / max(dem, 1.0)
            cost_penalty = 0.0001 * (dist_km / 50.0) * (unit_cost / 10.0)

            # Net coefficient to maximize: (benefit - penalty) -> negate for minimization
            c[idx] = -(benefit_per_unit - cost_penalty)

            # Bound: [0, Demand_{i,r}]
            bounds.append((0.0, max(0.0, dem)))

    # Supply Constraints: A_ub * x <= b_ub
    # Exactly num_resources supply constraints
    A_ub = np.zeros((num_resources, num_vars))
    b_ub = np.zeros(num_resources)

    for r, res in enumerate(resources):
        b_ub[r] = float(res["total_available"])
        for i in range(num_regions):
            idx = i * num_resources + r
            A_ub[r, idx] = 1.0

    # Solve via SciPy linprog (method='highs' - modern dual simplex)
    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    exec_time = time.time() - start_time

    # Parse solution
    allocation_matrix: Dict[str, Dict[str, float]] = {r["name"]: {} for r in regions}

    if res.success:
        x_sol = res.x
        for i, reg in enumerate(regions):
            r_name = reg["name"]
            for r, resource in enumerate(resources):
                res_name = resource["name"]
                idx = i * num_resources + r
                val = float(x_sol[idx])
                # Round to 1 decimal place
                allocation_matrix[r_name][res_name] = round(max(0.0, val), 1)
        obj_val = float(-res.fun)
    else:
        # Fallback if solver failed
        x_sol = np.zeros(num_vars)
        obj_val = 0.0

    # Fleet and Team allocation via proportional integer rounding based on LP urgency
    vehicle_allocation, team_allocation = _allocate_fleet_and_teams_proportional(problem, urgency_scores)

    # Compute standardized summary and verify feasibility
    result = compute_metrics_and_summary(
        problem=problem,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        execution_time_sec=exec_time,
        algorithm_name="Linear Programming (HiGHS Simplex)",
        objective_val=obj_val
    )

    # Academic explanation metadata
    result.summary["solver_status"] = res.message
    result.summary["num_variables"] = int(num_vars)
    result.summary["num_constraints"] = int(num_resources + num_vars)
    result.summary["method"] = "Highs Dual Simplex (Module IV)"
    if hasattr(res, "slack") and res.slack is not None:
        result.summary["supply_slacks"] = {
            resources[r]["name"]: round(float(res.slack[r]), 1) for r in range(min(num_resources, len(res.slack)))
        }

    return result

def _allocate_fleet_and_teams_proportional(
    problem: OptimizationProblem,
    urgency_scores: Dict[str, float]
) -> Tuple[Dict[str, Dict[str, int]], Dict[str, Dict[str, int]]]:
    """Allocates available vehicles and teams proportionally to regional urgency scores."""
    regions = sorted(problem.regions, key=lambda x: urgency_scores.get(x["name"], 0), reverse=True)
    v_alloc: Dict[str, Dict[str, int]] = {r["name"]: {v["type"]: 0 for v in problem.vehicles} for r in regions}
    t_alloc: Dict[str, Dict[str, int]] = {r["name"]: {t["type"]: 0 for t in problem.teams} for r in regions}

    # Vehicles
    for v in problem.vehicles:
        v_type = v["type"]
        avail = int(v["total_available"])
        for reg in regions:
            if avail <= 0:
                break
            # Give 1 or 2 to higher urgency regions
            needed = int(reg.get("vehicle_demand", 2))
            grant = min(avail, max(1, needed // 2))
            v_alloc[reg["name"]][v_type] = grant
            avail -= grant

    # Teams
    for t in problem.teams:
        t_type = t["type"]
        avail = int(t["total_available"])
        for reg in regions:
            if avail <= 0:
                break
            needed = int(reg.get("team_demand", 2))
            grant = min(avail, max(1, needed // 2))
            t_alloc[reg["name"]][t_type] = grant
            avail -= grant

    return v_alloc, t_alloc
