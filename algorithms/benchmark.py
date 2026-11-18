"""
Benchmark & Unified Algorithm Comparison Engine for DisasterShield AI.
Executes all 6 optimization algorithms (LP, IP, Greedy, GA, SA, MOO) on the identical
disaster scenario and generates side-by-side comparative analytics.
"""

from typing import Dict, Any, List
import pandas as pd
import time

from algorithms.base import OptimizationProblem, OptimizationResult
from algorithms.linear_programming import solve_linear_programming
from algorithms.integer_programming import solve_integer_programming
from algorithms.greedy import solve_greedy
from algorithms.genetic_algorithm import solve_genetic_algorithm
from algorithms.simulated_annealing import solve_simulated_annealing
from algorithms.multi_objective import solve_multi_objective

ALGORITHMS = {
    "Linear Programming": {
        "fn": solve_linear_programming,
        "category": "Exact Optimization",
        "module": "Module IV: Linear Programming & Simplex",
        "description": "Continuous relaxation via SciPy HiGHS Simplex; guarantees mathematical optimality for divisible resources."
    },
    "Integer Programming": {
        "fn": solve_integer_programming,
        "category": "Exact Optimization",
        "module": "Module IV: Integer Programming & Branch-and-Bound",
        "description": "OR-Tools SCIP solver; enforces strict whole-number dispatch of vehicles and rescue teams."
    },
    "Greedy Heuristic": {
        "fn": solve_greedy,
        "category": "Heuristic Algorithm",
        "module": "Module V: Priority Heuristics",
        "description": "Explainable urgency scoring; allocates resources sequentially with complete decision audit logs."
    },
    "Genetic Algorithm": {
        "fn": solve_genetic_algorithm,
        "category": "Metaheuristic (Population-based)",
        "module": "Module V: Evolutionary Metaheuristics",
        "description": "DEAP-powered evolutionary search with chromosome repair operator ensuring strict feasibility."
    },
    "Simulated Annealing": {
        "fn": solve_simulated_annealing,
        "category": "Metaheuristic (Neighborhood Search)",
        "module": "Module V: Trajectory Metaheuristics",
        "description": "Metropolis criteria and geometric cooling schedule; perturbs feasible neighbor allocations."
    },
    "Multi-Objective (NSGA-II)": {
        "fn": solve_multi_objective,
        "category": "Multi-Objective Decision Making",
        "module": "Module V: Pareto Optimization",
        "description": "pymoo NSGA-II; simultaneously minimizes delivery time & cost while maximizing demand fulfillment."
    }
}

def run_single_algorithm(algo_name: str, problem: OptimizationProblem, **kwargs) -> OptimizationResult:
    """Runs a single algorithm by key name."""
    if algo_name not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algo_name}. Options: {list(ALGORITHMS.keys())}")
    fn = ALGORITHMS[algo_name]["fn"]
    return fn(problem, **kwargs)

def run_all_benchmarks(problem: OptimizationProblem) -> Dict[str, Any]:
    """
    Runs all 6 algorithms on the exact same problem scenario and returns
    a comprehensive benchmark report with summary DataFrame.
    """
    results: Dict[str, OptimizationResult] = {}
    comparison_rows: List[Dict[str, Any]] = []

    for name, config in ALGORITHMS.items():
        try:
            res = config["fn"](problem)
            results[name] = res

            comparison_rows.append({
                "Algorithm": name,
                "Academic Module": config["module"],
                "Category": config["category"],
                "Fulfilled Demand (%)": round(res.fulfilled_demand_ratio * 100.0, 1),
                "Total Cost ($)": round(res.total_cost, 2),
                "Avg Delivery Time (h)": round(res.avg_delivery_time, 2),
                "Execution Time (s)": round(res.execution_time_sec, 4),
                "Feasible": "Yes" if res.is_feasible else "No",
                "Unmet Water (L)": round(res.unmet_demand.get("Clean Drinking Water", 0.0), 0),
                "Unmet Food (Pkts)": round(res.unmet_demand.get("Ready-to-Eat Food Packets", 0.0), 0),
                "Unmet Meds (Kits)": round(res.unmet_demand.get("Emergency Medical Kits", 0.0), 0)
            })
        except Exception as e:
            comparison_rows.append({
                "Algorithm": name,
                "Academic Module": config["module"],
                "Category": config["category"],
                "Fulfilled Demand (%)": 0.0,
                "Total Cost ($)": 0.0,
                "Avg Delivery Time (h)": 0.0,
                "Execution Time (s)": 0.0,
                "Feasible": f"Error: {str(e)[:30]}",
                "Unmet Water (L)": 0,
                "Unmet Food (Pkts)": 0,
                "Unmet Meds (Kits)": 0
            })

    comparison_df = pd.DataFrame(comparison_rows)

    return {
        "results": results,
        "comparison_table": comparison_df,
        "scenario_name": problem.scenario_name
    }
