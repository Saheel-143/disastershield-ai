"""
Algorithm C: Greedy Urgency Heuristic.
Course Reference: CSDX 507 Decision-Making for Data Science - Module V.
Explainable, priority-driven heuristic that ranks affected regions by a multi-factor
urgency index and allocates resources sequentially until supplies are exhausted.
Produces an audit trail explaining decision rationale.
"""

import time
from typing import Dict, Any, List, Tuple
import numpy as np

from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    compute_metrics_and_summary
)

def solve_greedy(problem: OptimizationProblem) -> OptimizationResult:
    """
    Executes an explainable Greedy Resource Allocation.
    1. Computes composite Urgency Index for all regions:
       U_i = 0.40 * (Severity / 5.0) + 0.25 * (Pop / MaxPop) + 0.20 * (1 - Acc) + 0.15 * PriorityFactor
    2. Sorts regions by descending urgency.
    3. Allocates available resources greedily up to region demand.
    4. Records step-by-step decision log.
    """
    start_time = time.time()

    regions = problem.regions
    resources = problem.resources
    vehicles = problem.vehicles
    teams = problem.teams

    demand_mapping = {
        "Clean Drinking Water": "water_demand",
        "Ready-to-Eat Food Packets": "food_demand",
        "Emergency Medical Kits": "med_demand",
        "Temporary Emergency Shelters": "shelter_demand"
    }

    # Step 1: Compute Urgency Index & Sort
    max_pop = max([r["population"] for r in regions]) if regions else 1.0
    priority_weights = {"Critical": 1.0, "High": 0.8, "Medium": 0.5, "Low": 0.2}

    ranked_regions = []
    for reg in regions:
        sev_term = float(reg["severity"]) / 5.0
        pop_term = float(reg["population"]) / max_pop
        acc_term = 1.0 - float(reg["accessibility_score"])
        crit_term = priority_weights.get(reg.get("critical_priority", "Medium"), 0.5)

        urgency_idx = (0.40 * sev_term) + (0.25 * pop_term) + (0.20 * acc_term) + (0.15 * crit_term)
        ranked_regions.append({
            "region": reg,
            "urgency_score": round(urgency_idx, 4),
            "name": reg["name"]
        })

    # Sort descending by urgency score
    ranked_regions.sort(key=lambda x: x["urgency_score"], reverse=True)

    # Step 2: Track remaining inventory
    remaining_supply = {res["name"]: float(res["total_available"]) for res in resources}
    remaining_vehicles = {v["type"]: int(v["total_available"]) for v in vehicles}
    remaining_teams = {t["type"]: int(t["total_available"]) for t in teams}

    allocation_matrix: Dict[str, Dict[str, float]] = {r["name"]: {} for r in regions}
    vehicle_allocation: Dict[str, Dict[str, int]] = {r["name"]: {} for r in regions}
    team_allocation: Dict[str, Dict[str, int]] = {r["name"]: {} for r in regions}

    decision_logs: List[str] = []

    # Step 3: Sequential Greedy Allocation
    for rank, item in enumerate(ranked_regions, 1):
        reg = item["region"]
        r_name = item["name"]
        u_score = item["urgency_score"]

        decision_logs.append(f"Rank #{rank} [{r_name}] - Urgency Index: {u_score:.4f} (Severity: {reg['severity']}, Pop: {reg['population']:,})")

        # 3A. Resources
        for res in resources:
            res_name = res["name"]
            key = demand_mapping.get(res_name, "water_demand")
            dem = float(reg.get(key, 0.0))
            avail = remaining_supply.get(res_name, 0.0)

            # Greedy choice: min(demand, remaining available)
            alloc_qty = min(dem, avail)
            if res["type"] == "Indivisible":
                alloc_qty = float(int(alloc_qty))

            allocation_matrix[r_name][res_name] = round(alloc_qty, 1)
            remaining_supply[res_name] -= alloc_qty

            if alloc_qty < dem:
                deficit = dem - alloc_qty
                decision_logs.append(f"  -> {res_name}: Shortage! Allocated {alloc_qty:,.0f}/{dem:,.0f} units (Deficit: {deficit:,.0f})")
            else:
                decision_logs.append(f"  -> {res_name}: 100% Demand Met ({alloc_qty:,.0f} units)")

        # 3B. Vehicles
        v_demand = int(reg.get("vehicle_demand", 3))
        v_granted = 0
        road_cond = reg.get("road_condition", "")
        is_flooded = "Flooded" in road_cond or "Submerged" in road_cond or "Waterlogged" in road_cond

        for v in vehicles:
            v_type = v["type"]
            v_avail = remaining_vehicles.get(v_type, 0)
            needed = max(0, v_demand - v_granted)

            # Heuristic match: prioritize boats in flooded zones, trucks elsewhere
            if is_flooded and "Boat" in v_type:
                take = min(needed, v_avail)
            elif not is_flooded and "Boat" in v_type:
                take = 0  # save boats for flood zones
            else:
                take = min(needed, v_avail)

            vehicle_allocation[r_name][v_type] = take
            remaining_vehicles[v_type] -= take
            v_granted += take

        # 3C. Teams
        t_demand = int(reg.get("team_demand", 3))
        t_granted = 0
        for t in teams:
            t_type = t["type"]
            t_avail = remaining_teams.get(t_type, 0)
            needed = max(0, t_demand - t_granted)
            take = min(needed, t_avail)
            team_allocation[r_name][t_type] = take
            remaining_teams[t_type] -= take
            t_granted += take

    exec_time = time.time() - start_time

    # Compute standardized metrics
    result = compute_metrics_and_summary(
        problem=problem,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        execution_time_sec=exec_time,
        algorithm_name="Greedy Urgency Heuristic",
        objective_val=sum(item["urgency_score"] for item in ranked_regions)
    )

    result.summary["ranked_regions_order"] = [item["name"] for item in ranked_regions]
    result.summary["decision_audit_logs"] = decision_logs
    result.summary["method"] = "Explainable Multi-Attribute Greedy Priority (Module V)"

    return result
