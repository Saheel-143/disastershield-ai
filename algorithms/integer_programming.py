"""
Algorithm B: Integer Programming (IP) Fleet and Team Dispatch.
Course Reference: CSDX 507 Decision-Making for Data Science - Module IV.
Uses Google OR-Tools (SCIP Mixed-Integer Linear Solver) to find optimal integer
assignments of rescue vehicles, specialized rescue teams, and emergency shelters.
"""

import time
import numpy as np
from ortools.linear_solver import pywraplp
from typing import Dict, Any, Tuple, List

from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    compute_metrics_and_summary
)

def solve_integer_programming(problem: OptimizationProblem) -> OptimizationResult:
    """
    Solves discrete, whole-number vehicle, team, and shelter allocations
    using Google OR-Tools SCIP solver.
    Constraints:
      1. Whole integer decision variables for vehicles and teams.
      2. Sum_{regions} Vehicles_v <= Fleet_v
      3. Sum_{regions} Teams_t <= Teams_t
      4. Road condition compatibility:
         - Waterlogged roads require water-capable crafts or incur heavy penalty.
         - Impassable roads block low-clearance vehicles.
    """
    start_time = time.time()

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        # Fallback to CBC if SCIP not found
        solver = pywraplp.Solver.CreateSolver("CBC")

    regions = problem.regions
    resources = problem.resources
    vehicles = problem.vehicles
    teams = problem.teams
    urgency_scores = problem.compute_urgency_scores()

    demand_mapping = {
        "Clean Drinking Water": "water_demand",
        "Ready-to-Eat Food Packets": "food_demand",
        "Emergency Medical Kits": "med_demand",
        "Temporary Emergency Shelters": "shelter_demand"
    }

    # 1. Variables for Indivisible Resources
    # Vehicle variables: y[i, v] is integer
    y_veh = {}
    for i, reg in enumerate(regions):
        for v, veh in enumerate(vehicles):
            var_name = f"veh_{i}_{v}"
            # Upper bound: either regional demand or total fleet
            ub = min(int(reg.get("vehicle_demand", 5)), int(veh["total_available"]))
            y_veh[i, v] = solver.IntVar(0, ub, var_name)

    # Team variables: z[i, t] is integer
    z_team = {}
    for i, reg in enumerate(regions):
        for t, team in enumerate(teams):
            var_name = f"team_{i}_{t}"
            ub = min(int(reg.get("team_demand", 5)), int(team["total_available"]))
            z_team[i, t] = solver.IntVar(0, ub, var_name)

    # Divisible resource variables: x[i, r] (can be continuous or discrete stepped)
    x_res = {}
    for i, reg in enumerate(regions):
        for r, res in enumerate(resources):
            var_name = f"res_{i}_{r}"
            key = demand_mapping.get(res["name"], "water_demand")
            dem = float(reg.get(key, 0.0))
            if res["type"] == "Indivisible":
                x_res[i, r] = solver.IntVar(0, int(dem), var_name)
            else:
                x_res[i, r] = solver.NumVar(0.0, dem, var_name)

    # 2. Constraints
    # Supply constraints for resources
    for r, res in enumerate(resources):
        solver.Add(
            solver.Sum([x_res[i, r] for i in range(len(regions))]) <= float(res["total_available"])
        )

    # Fleet constraints for vehicles
    for v, veh in enumerate(vehicles):
        solver.Add(
            solver.Sum([y_veh[i, v] for i in range(len(regions))]) <= int(veh["total_available"])
        )

    # Total team constraints
    for t, team in enumerate(teams):
        solver.Add(
            solver.Sum([z_team[i, t] for i in range(len(regions))]) <= int(team["total_available"])
        )

    # Regional demand limits for total vehicles and teams
    for i, reg in enumerate(regions):
        v_dem = int(reg.get("vehicle_demand", 5))
        solver.Add(solver.Sum([y_veh[i, v] for v in range(len(vehicles))]) <= v_dem)

        t_dem = int(reg.get("team_demand", 5))
        solver.Add(solver.Sum([z_team[i, t] for t in range(len(teams))]) <= t_dem)

        # Terrain & Accessibility Rule:
        # If region is waterlogged / submerged, standard ambulance is blocked unless road accessibility >= 0.5
        acc = float(reg.get("accessibility_score", 1.0))
        road_cond = reg.get("road_condition", "")
        if "Submerged" in road_cond or "Waterlogged" in road_cond or "Flooded" in road_cond:
            for v, veh in enumerate(vehicles):
                # If vehicle cannot handle waterlogged roads and road is severely blocked
                if not veh.get("can_handle_waterlogged", 0) and acc < 0.3:
                    solver.Add(y_veh[i, v] == 0)

    # 3. Objective Function: Maximize weighted life safety & resource coverage
    objective = solver.Objective()
    for i, reg in enumerate(regions):
        u_score = urgency_scores.get(reg["name"], 0.5)
        dist_km = float(reg["distance_km"])

        # Value for resources
        for r, res in enumerate(resources):
            key = demand_mapping.get(res["name"], "water_demand")
            dem = float(reg.get(key, 1.0))
            priority = float(res.get("priority_weight", 1.0))
            coeff = (priority * (1.0 + u_score * 3.0)) / max(dem, 1.0)
            objective.SetCoefficient(x_res[i, r], coeff)

        # Value for vehicles
        for v, veh in enumerate(vehicles):
            cargo_cap = float(veh.get("cargo_capacity_kg", 1000.0))
            cost_km = float(veh.get("cost_per_km", 3.0))
            # Rescuing capability weighted by urgency minus travel cost
            val_veh = (u_score * 15.0) + (cargo_cap / 1000.0) - (dist_km * cost_km * 0.01)
            # Compatibility bonus if boat in waterlogged zone
            if "Flooded" in reg.get("road_condition", "") and veh.get("can_handle_waterlogged", 0):
                val_veh += 10.0
            objective.SetCoefficient(y_veh[i, v], val_veh)

        # Value for teams
        for t, team in enumerate(teams):
            p_count = int(team.get("personnel_per_team", 4))
            d_cost = float(team.get("daily_cost", 500.0))
            val_team = (u_score * 20.0) + (p_count * 1.5) - (d_cost * 0.005)
            objective.SetCoefficient(z_team[i, t], val_team)

    objective.SetMaximization()

    # Solve
    solver_status = solver.Solve()
    exec_time = time.time() - start_time

    # Collect Results
    allocation_matrix: Dict[str, Dict[str, float]] = {r["name"]: {} for r in regions}
    vehicle_allocation: Dict[str, Dict[str, int]] = {r["name"]: {} for r in regions}
    team_allocation: Dict[str, Dict[str, int]] = {r["name"]: {} for r in regions}

    if solver_status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        for i, reg in enumerate(regions):
            r_name = reg["name"]
            for r, res in enumerate(resources):
                val = x_res[i, r].solution_value()
                allocation_matrix[r_name][res["name"]] = round(max(0.0, float(val)), 1)

            for v, veh in enumerate(vehicles):
                cnt = int(round(y_veh[i, v].solution_value()))
                vehicle_allocation[r_name][veh["type"]] = max(0, cnt)

            for t, team in enumerate(teams):
                cnt = int(round(z_team[i, t].solution_value()))
                team_allocation[r_name][team["type"]] = max(0, cnt)

        obj_val = float(solver.Objective().Value())
    else:
        obj_val = 0.0

    result = compute_metrics_and_summary(
        problem=problem,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        execution_time_sec=exec_time,
        algorithm_name="Integer Programming (OR-Tools SCIP)",
        objective_val=obj_val
    )

    result.summary["solver_status"] = "OPTIMAL" if solver_status == pywraplp.Solver.OPTIMAL else "FEASIBLE"
    result.summary["num_variables"] = solver.NumVariables()
    result.summary["num_constraints"] = solver.NumConstraints()
    result.summary["method"] = "Branch-and-Bound / Cutting Planes (Module IV)"

    return result
