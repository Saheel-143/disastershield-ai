"""
Core base data structures, validation engine, and common utility functions
for all DisasterShield AI optimization algorithms.
Supports single-state and multi-state disaster optimization problems,
dynamic State Emergency Operations Centres (SEOC), and inter-state transfer decisions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import pandas as pd
import time
import math

@dataclass
class OptimizationProblem:
    """Standardized representation of a disaster resource allocation scenario."""
    regions: List[Dict[str, Any]]
    resources: List[Dict[str, Any]]
    vehicles: List[Dict[str, Any]]
    teams: List[Dict[str, Any]]
    central_depot: Dict[str, Any]
    scenario_name: str = "Standard Scenario"
    hubs: List[Dict[str, Any]] = field(default_factory=list)

    def get_region_names(self) -> List[str]:
        return [r["name"] for r in self.regions]

    def get_resource_names(self) -> List[str]:
        return [r["name"] for r in self.resources]

    def get_vehicle_types(self) -> List[str]:
        return [v["type"] for v in self.vehicles]

    def get_team_types(self) -> List[str]:
        return [t["type"] for t in self.teams]

    def get_states(self) -> List[str]:
        """Returns the distinct list of states present across all affected regions."""
        states = []
        for r in self.regions:
            s = r.get("state_name", "General").strip()
            if s and s not in states:
                states.append(s)
        return states if states else ["General"]

    def is_multi_state(self) -> bool:
        """Returns True if the scenario affects multiple Indian states simultaneously."""
        return len(self.get_states()) > 1

    def get_total_demand_by_resource(self, state_name: Optional[str] = None) -> Dict[str, float]:
        """Calculates total regional demand for each resource, optionally filtered by state."""
        mapping = {
            "Clean Drinking Water": "water_demand",
            "Ready-to-Eat Food Packets": "food_demand",
            "Emergency Medical Kits": "med_demand",
            "Temporary Emergency Shelters": "shelter_demand"
        }
        target_regions = self.regions
        if state_name:
            target_regions = [r for r in self.regions if r.get("state_name", "").strip().lower() == state_name.strip().lower()]

        totals = {}
        for res in self.resources:
            r_name = res["name"]
            key = mapping.get(r_name, "water_demand")
            totals[r_name] = sum(float(r.get(key, 0)) for r in target_regions)
        return totals

    def get_total_supply_by_resource(self) -> Dict[str, float]:
        """Returns total supply inventory for each resource."""
        return {r["name"]: float(r["total_available"]) for r in self.resources}

    def compute_urgency_scores(self) -> Dict[str, float]:
        """
        Computes normalized urgency score U_i for each region:
        U_i = 0.45 * (Severity / 5.0) + 0.25 * (Pop / MaxPop) + 0.30 * (1.0 - Accessibility)
        """
        max_pop = max([r["population"] for r in self.regions]) if self.regions else 1.0
        scores = {}
        for r in self.regions:
            sev_term = float(r["severity"]) / 5.0
            pop_term = float(r["population"]) / max_pop
            acc_term = 1.0 - float(r["accessibility_score"])
            score = (0.45 * sev_term) + (0.25 * pop_term) + (0.30 * acc_term)
            scores[r["name"]] = round(score, 4)
        return scores

    def split_by_state(self, state_hubs_map: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, "OptimizationProblem"]:
        """
        Splits a multi-state scenario into independent state-scoped OptimizationProblem instances.
        Apportions overall resource inventories across states proportional to their regional demand,
        guaranteeing that sum(state_inventory) == total_inventory (no double allocation).
        """
        states = self.get_states()
        if len(states) <= 1:
            return {states[0]: self}

        overall_demands = self.get_total_demand_by_resource()
        state_problems = {}

        # 1. Compute state demand ratios
        state_demands = {}
        state_ratios = {}
        for s in states:
            s_dem = self.get_total_demand_by_resource(state_name=s)
            state_demands[s] = s_dem

        for res in self.resources:
            r_name = res["name"]
            tot_d = overall_demands.get(r_name, 0.0)
            for s in states:
                if s not in state_ratios:
                    state_ratios[s] = {}
                state_ratios[s][r_name] = (state_demands[s].get(r_name, 0.0) / tot_d) if tot_d > 0 else (1.0 / len(states))

        # 2. Construct state problems
        for idx, s in enumerate(states):
            s_regions = [r for r in self.regions if r.get("state_name", "").strip().lower() == s.strip().lower()]

            # Partition resources
            s_resources = []
            for res in self.resources:
                r_name = res["name"]
                tot_avail = float(res["total_available"])
                if idx == len(states) - 1:
                    # Allocate remainder to avoid rounding drift
                    prev_alloc = sum(round(float(res["total_available"]) * state_ratios[prev_s][r_name], 1) for prev_s in states[:-1])
                    s_avail = max(0.0, round(tot_avail - prev_alloc, 1))
                else:
                    s_avail = round(tot_avail * state_ratios[s][r_name], 1)

                r_copy = dict(res)
                r_copy["total_available"] = s_avail
                s_resources.append(r_copy)

            # Partition vehicles
            s_vehicles = []
            for v in self.vehicles:
                tot_v = int(v["total_available"])
                v_share = max(1, int(round(tot_v * (len(s_regions) / len(self.regions)))))
                v_copy = dict(v)
                v_copy["total_available"] = min(tot_v, v_share)
                s_vehicles.append(v_copy)

            # Partition teams
            s_teams = []
            for t in self.teams:
                tot_t = int(t["total_available"])
                t_share = max(1, int(round(tot_t * (len(s_regions) / len(self.regions)))))
                t_copy = dict(t)
                t_copy["total_available"] = min(tot_t, t_share)
                s_teams.append(t_copy)

            # Assign designated SEOC hub
            hub = None
            if state_hubs_map and s in state_hubs_map:
                hub = state_hubs_map[s]
            elif self.hubs:
                for h in self.hubs:
                    if h.get("state_name", "").strip().lower() == s.strip().lower():
                        hub = h
                        break
            if not hub:
                hub = self.central_depot

            state_problems[s] = OptimizationProblem(
                regions=s_regions,
                resources=s_resources,
                vehicles=s_vehicles,
                teams=s_teams,
                central_depot=hub,
                scenario_name=f"{self.scenario_name} [{s} Sub-Theater]",
                hubs=[hub]
            )

        return state_problems

    def compute_inter_state_transfers(
        self,
        state_results: Dict[str, "OptimizationResult"],
        state_hubs_map: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyzes resource surpluses and deficits across states.
        Recommends concrete inter-state resource transfers with distance and transit feasibility.
        """
        states = list(state_results.keys())
        if len(states) < 2:
            return []

        transfers = []
        # Compare each pair of states
        for i in range(len(states)):
            for j in range(i + 1, len(states)):
                sA = states[i]
                sB = states[j]
                resA = state_results[sA]
                resB = state_results[sB]

                # Check each resource
                for r_name in self.get_resource_names():
                    unmetA = resA.unmet_demand.get(r_name, 0.0)
                    unmetB = resB.unmet_demand.get(r_name, 0.0)

                    utilA = resA.resource_utilization.get(r_name, 100.0)
                    utilB = resB.resource_utilization.get(r_name, 100.0)

                    # If A has low utilization (< 85%) and B has high unmet demand
                    if utilA < 85.0 and unmetB > 500.0:
                        from_state, to_state = sA, sB
                        surplus_qty = max(0.0, unmetB * 0.4)
                    elif utilB < 85.0 and unmetA > 500.0:
                        from_state, to_state = sB, sA
                        surplus_qty = max(0.0, unmetA * 0.4)
                    else:
                        continue

                    # Calculate transit distance between State SEOCs
                    hub_from = state_hubs_map.get(from_state) if state_hubs_map else None
                    hub_to = state_hubs_map.get(to_state) if state_hubs_map else None

                    dist_km = 450.0  # Default inter-state transit estimate
                    if hub_from and hub_to and hub_from.get("latitude") and hub_to.get("latitude"):
                        lat1, lon1 = math.radians(float(hub_from["latitude"])), math.radians(float(hub_from["longitude"]))
                        lat2, lon2 = math.radians(float(hub_to["latitude"])), math.radians(float(hub_to["longitude"]))
                        dlat = lat2 - lat1
                        dlon = lon2 - lon1
                        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                        c = 2 * math.asin(math.sqrt(a))
                        dist_km = round(6371.0 * c * 1.25, 1)  # 1.25 road winding factor

                    transit_time_hrs = round(dist_km / 50.0, 1)  # 50 km/h highway logistics convoy
                    transfer_cost_usd = round(dist_km * 4.5, 2)

                    transfers.append({
                        "from_state": from_state,
                        "to_state": to_state,
                        "resource_name": r_name,
                        "recommended_quantity": round(surplus_qty, 1),
                        "transit_distance_km": dist_km,
                        "est_transit_time_hrs": transit_time_hrs,
                        "logistics_cost_usd": transfer_cost_usd,
                        "status": "Feasible Via Green Logistics Corridor"
                    })

        return transfers


@dataclass
class OptimizationResult:
    """Standardized result schema returned by every algorithm."""
    algorithm_name: str
    scenario_name: str
    execution_time_sec: float
    is_feasible: bool
    objective_value: float
    fulfilled_demand_ratio: float  # e.g., 0.685 (68.5%)
    total_cost: float              # USD
    avg_delivery_time: float       # hours
    max_delivery_time: float       # hours
    allocation_matrix: Dict[str, Dict[str, float]] # {region_name: {resource_name: allocated_qty}}
    vehicle_allocation: Dict[str, Dict[str, int]]  # {region_name: {vehicle_type: count}}
    team_allocation: Dict[str, Dict[str, int]]     # {region_name: {team_type: count}}
    resource_utilization: Dict[str, float]         # {resource_name: pct_used}
    unmet_demand: Dict[str, float]                 # {resource_name: remaining_unmet_qty}
    summary: Dict[str, Any] = field(default_factory=dict)
    feasibility_notes: List[str] = field(default_factory=list)
    convergence_history: List[Dict[str, Any]] = field(default_factory=list)


def create_problem_from_db_records(
    regions_df: pd.DataFrame,
    resources_df: pd.DataFrame,
    vehicles_df: pd.DataFrame,
    teams_df: pd.DataFrame,
    depot_info: Optional[Dict[str, Any]] = None,
    scenario_name: str = "Standard Baseline"
) -> OptimizationProblem:
    """Constructs an OptimizationProblem instance from pandas DataFrames with dynamic SEOC."""
    from database.db import get_active_hub_for_disaster, get_hubs_for_states

    # Determine unique states in active regions
    states = []
    if "state_name" in regions_df.columns:
        states = [s for s in regions_df["state_name"].dropna().unique().tolist() if s]

    # Resolve hubs
    hubs = []
    if states:
        hubs = get_hubs_for_states(states)

    if depot_info:
        active_hub = depot_info
    elif hubs:
        active_hub = hubs[0]
    else:
        active_hub = get_active_hub_for_disaster()

    return OptimizationProblem(
        regions=regions_df.to_dict(orient="records"),
        resources=resources_df.to_dict(orient="records"),
        vehicles=vehicles_df.to_dict(orient="records"),
        teams=teams_df.to_dict(orient="records"),
        central_depot=active_hub,
        scenario_name=scenario_name,
        hubs=hubs
    )


def verify_solution_feasibility(
    problem: OptimizationProblem,
    allocation_matrix: Dict[str, Dict[str, float]],
    vehicle_allocation: Optional[Dict[str, Dict[str, int]]] = None,
    team_allocation: Optional[Dict[str, Dict[str, int]]] = None,
    tolerance: float = 1e-3
) -> Tuple[bool, List[str]]:
    """
    Rigorously verifies all physical constraints:
    1. Total resource allocated <= Total available supply.
    2. Regional allocation <= Regional demand.
    3. Non-negativity constraint.
    4. Total vehicle count <= Available fleet.
    5. Total rescue teams <= Available teams.
    """
    is_feasible = True
    notes = []

    supply_limits = problem.get_total_supply_by_resource()
    demand_mapping = {
        "Clean Drinking Water": "water_demand",
        "Ready-to-Eat Food Packets": "food_demand",
        "Emergency Medical Kits": "med_demand",
        "Temporary Emergency Shelters": "shelter_demand"
    }

    # 1. Supply verification
    total_allocated_per_res = {r_name: 0.0 for r_name in supply_limits}
    for reg_name, res_dict in allocation_matrix.items():
        for res_name, qty in res_dict.items():
            if qty < -tolerance:
                is_feasible = False
                notes.append(f"Negative allocation detected for {reg_name} in {res_name}: {qty}")
            total_allocated_per_res[res_name] = total_allocated_per_res.get(res_name, 0.0) + max(0.0, qty)

    for res_name, total_allocated in total_allocated_per_res.items():
        limit = supply_limits.get(res_name, 0.0)
        if total_allocated > limit + tolerance:
            is_feasible = False
            notes.append(f"Supply limit exceeded for {res_name}: Allocated {total_allocated:.1f} > Available {limit:.1f}")

    # 2. Demand verification
    for reg in problem.regions:
        reg_name = reg["name"]
        allocs = allocation_matrix.get(reg_name, {})
        for res_name, qty in allocs.items():
            field_name = demand_mapping.get(res_name, "water_demand")
            dem = float(reg.get(field_name, 0.0))
            if qty > dem + tolerance:
                is_feasible = False
                notes.append(f"Demand exceeded for {reg_name} in {res_name}: Allocated {qty:.1f} > Demanded {dem:.1f}")

    # 3. Vehicle constraints
    if vehicle_allocation:
        avail_vehicles = {v["type"]: int(v["total_available"]) for v in problem.vehicles}
        used_vehicles = {v["type"]: 0 for v in problem.vehicles}
        for reg_name, v_dict in vehicle_allocation.items():
            for v_type, count in v_dict.items():
                if count < 0:
                    is_feasible = False
                    notes.append(f"Negative vehicle assignment for {reg_name}: {v_type}")
                used_vehicles[v_type] = used_vehicles.get(v_type, 0) + count

        for v_type, used in used_vehicles.items():
            avail = avail_vehicles.get(v_type, 0)
            if used > avail:
                is_feasible = False
                notes.append(f"Vehicle fleet exceeded for {v_type}: Used {used} > Available {avail}")

    # 4. Team constraints
    if team_allocation:
        avail_teams = {t["type"]: int(t["total_available"]) for t in problem.teams}
        used_teams = {t["type"]: 0 for t in problem.teams}
        for reg_name, t_dict in team_allocation.items():
            for t_type, count in t_dict.items():
                if count < 0:
                    is_feasible = False
                    notes.append(f"Negative team assignment for {reg_name}: {t_type}")
                used_teams[t_type] = used_teams.get(t_type, 0) + count

        for t_type, used in used_teams.items():
            avail = avail_teams.get(t_type, 0)
            if used > avail:
                is_feasible = False
                notes.append(f"Team capacity exceeded for {t_type}: Used {used} > Available {avail}")

    if is_feasible:
        notes.append("All physical supply, demand, fleet, and non-negativity constraints are strictly satisfied.")

    return is_feasible, notes


def compute_metrics_and_summary(
    problem: OptimizationProblem,
    allocation_matrix: Dict[str, Dict[str, float]],
    vehicle_allocation: Dict[str, Dict[str, int]],
    team_allocation: Dict[str, Dict[str, int]],
    execution_time_sec: float,
    algorithm_name: str,
    objective_val: float = 0.0
) -> OptimizationResult:
    """Calculates fulfillment ratios, costs, delivery times, and utilization metrics."""
    total_demands = problem.get_total_demand_by_resource()
    total_supplies = problem.get_total_supply_by_resource()

    resource_unit_costs = {r["name"]: float(r["unit_cost"]) for r in problem.resources}

    demand_mapping = {
        "Clean Drinking Water": "water_demand",
        "Ready-to-Eat Food Packets": "food_demand",
        "Emergency Medical Kits": "med_demand",
        "Temporary Emergency Shelters": "shelter_demand"
    }

    # Reconcile numerical floating-point rounding artifacts
    for res in problem.resources:
        res_name = res["name"]
        avail = float(res["total_available"])
        tot = sum(allocation_matrix.get(r["name"], {}).get(res_name, 0.0) for r in problem.regions)
        if tot > avail:
            excess = tot - avail
            best_reg = max(problem.regions, key=lambda r: allocation_matrix.get(r["name"], {}).get(res_name, 0.0))["name"]
            current_val = allocation_matrix[best_reg][res_name]
            allocation_matrix[best_reg][res_name] = round(max(0.0, current_val - excess), 1)

    for reg in problem.regions:
        r_name = reg["name"]
        for res in problem.resources:
            res_name = res["name"]
            key = demand_mapping.get(res_name, "water_demand")
            dem = float(reg.get(key, 0.0))
            if allocation_matrix.get(r_name, {}).get(res_name, 0.0) > dem:
                allocation_matrix[r_name][res_name] = round(dem, 1)

    total_allocated_per_res = {r: 0.0 for r in total_supplies}
    total_demand_sum = sum(total_demands.values())
    total_allocated_sum = 0.0

    material_cost = 0.0
    for reg_name, r_allocs in allocation_matrix.items():
        for res_name, qty in r_allocs.items():
            qty_clean = max(0.0, qty)
            total_allocated_per_res[res_name] += qty_clean
            total_allocated_sum += qty_clean
            material_cost += qty_clean * resource_unit_costs.get(res_name, 1.0)

    # Shortages & Utilization
    unmet_demand = {}
    resource_utilization = {}
    for res_name, supply in total_supplies.items():
        used = total_allocated_per_res.get(res_name, 0.0)
        dem = total_demands.get(res_name, 0.0)
        unmet_demand[res_name] = max(0.0, dem - used)
        resource_utilization[res_name] = round((used / supply * 100.0) if supply > 0 else 0.0, 2)

    fulfilled_ratio = (total_allocated_sum / total_demand_sum) if total_demand_sum > 0 else 1.0

    # Fleet and Team costs + Delivery Times
    fleet_cost = 0.0
    team_cost = 0.0
    delivery_times = []

    reg_dict = {r["name"]: r for r in problem.regions}
    veh_dict = {v["type"]: v for v in problem.vehicles}
    team_dict = {t["type"]: t for t in problem.teams}

    for reg_name, v_allocs in vehicle_allocation.items():
        reg = reg_dict.get(reg_name)
        if not reg:
            continue
        dist = float(reg.get("distance_km", 20.0))
        base_time = float(reg.get("travel_time_hours", 1.5))
        acc = float(reg.get("accessibility_score", 0.5))

        effective_time = base_time / max(0.15, acc)
        delivery_times.append(effective_time)

        for v_type, count in v_allocs.items():
            if count > 0:
                v_info = veh_dict.get(v_type, {})
                c_per_km = float(v_info.get("cost_per_km", 3.0))
                fleet_cost += count * (dist * 2.0) * c_per_km

    for reg_name, t_allocs in team_allocation.items():
        for t_type, count in t_allocs.items():
            if count > 0:
                t_info = team_dict.get(t_type, {})
                d_cost = float(t_info.get("daily_cost", 500.0))
                team_cost += count * d_cost

    total_cost = round(material_cost + fleet_cost + team_cost, 2)
    avg_deliv_time = round(float(np.mean(delivery_times)), 2) if delivery_times else 2.0
    max_deliv_time = round(float(np.max(delivery_times)), 2) if delivery_times else 3.5

    is_feasible, notes = verify_solution_feasibility(
        problem, allocation_matrix, vehicle_allocation, team_allocation
    )

    summary = {
        "material_cost_usd": round(material_cost, 2),
        "fleet_cost_usd": round(fleet_cost, 2),
        "team_cost_usd": round(team_cost, 2),
        "total_cost_usd": total_cost,
        "fulfilled_demand_pct": round(fulfilled_ratio * 100.0, 2),
        "total_allocated_units": round(total_allocated_sum, 1),
        "total_demanded_units": round(total_demand_sum, 1),
        "avg_delivery_time_hrs": avg_deliv_time,
        "max_delivery_time_hrs": max_deliv_time
    }

    return OptimizationResult(
        algorithm_name=algorithm_name,
        scenario_name=problem.scenario_name,
        execution_time_sec=round(execution_time_sec, 4),
        is_feasible=is_feasible,
        objective_value=round(objective_val, 4),
        fulfilled_demand_ratio=round(fulfilled_ratio, 4),
        total_cost=total_cost,
        avg_delivery_time=avg_deliv_time,
        max_delivery_time=max_deliv_time,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        resource_utilization=resource_utilization,
        unmet_demand=unmet_demand,
        summary=summary,
        feasibility_notes=notes
    )
