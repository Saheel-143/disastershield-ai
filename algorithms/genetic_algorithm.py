"""
Algorithm D: Genetic Algorithm (GA) Resource Allocation.
Course Reference: CSDX 507 Decision-Making for Data Science - Module V.
Uses DEAP (Distributed Evolutionary Algorithms in Python) to evolve optimal disaster
resource distribution plans. Features a dedicated repair operator guaranteeing 100%
strict feasibility for all candidate solutions, tournament selection, blend crossover,
and generational convergence tracking.
"""

import time
import random
import numpy as np
from typing import Dict, Any, List, Tuple
from deap import base, creator, tools

from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    compute_metrics_and_summary
)

# Setup DEAP creator classes cleanly (avoid re-registration warnings)
if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMax)

def solve_genetic_algorithm(
    problem: OptimizationProblem,
    pop_size: int = 40,
    generations: int = 35,
    crossover_prob: float = 0.7,
    mutation_prob: float = 0.25,
    seed: int = 42
) -> OptimizationResult:
    """
    Evolves resource allocations using DEAP Genetic Algorithm.
    Chromosome: Vector of continuous genes in [0, 1] representing the allocation
    fraction for each (region, resource) pair.
    Repair Operator: Normalizes allocations per resource so total <= Supply, and alloc <= Demand.
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

    # Pre-extract demands and supplies
    demands = np.zeros((num_regions, num_resources))
    supplies = np.zeros(num_resources)

    for r, res in enumerate(resources):
        supplies[r] = float(res["total_available"])
        key = demand_mapping.get(res["name"], "water_demand")
        for i, reg in enumerate(regions):
            demands[i, r] = float(reg.get(key, 0.0))

    genome_len = num_regions * num_resources

    # --- Repair & Decoding Operator ---
    def decode_and_repair(individual: List[float]) -> np.ndarray:
        """
        Decodes a genome of [0, 1] fractions into physical resource allocations,
        strictly repairing any violations of supply or regional demand.
        """
        arr = np.array(individual).reshape((num_regions, num_resources))
        arr = np.clip(arr, 0.0, 1.0)

        # Proposed allocation: fraction * demand
        alloc = arr * demands

        # Supply feasibility repair
        for r in range(num_resources):
            tot = np.sum(alloc[:, r])
            if tot > supplies[r] and tot > 1e-6:
                # Proportional downscaling
                alloc[:, r] = alloc[:, r] * (supplies[r] / tot)

        # Upper bound clamp
        alloc = np.minimum(alloc, demands)
        alloc = np.maximum(alloc, 0.0)
        return alloc

    # --- Fitness Evaluation Function ---
    def eval_individual(individual: List[float]) -> Tuple[float]:
        alloc = decode_and_repair(individual)
        fitness = 0.0

        for i, reg in enumerate(regions):
            u_score = urgency_scores.get(reg["name"], 0.5)
            dist_km = float(reg["distance_km"])
            acc = float(reg["accessibility_score"])

            for r in range(num_resources):
                dem = demands[i, r]
                if dem > 0:
                    fraction_met = alloc[i, r] / dem
                    # Weighted utility
                    fitness += (1.0 + u_score * 2.5) * fraction_met * 10.0

            # Small transport penalty
            fitness -= (dist_km / 100.0) * (1.0 - acc) * 0.5

        return (fitness,)

    # Setup DEAP Toolbox
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, 0.1, 0.9)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=genome_len)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval_individual)
    toolbox.register("mate", tools.cxBlend, alpha=0.3)
    toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=0.15, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Initialize Population
    population = toolbox.population(n=pop_size)

    # Evaluate initial population
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    convergence_history = []

    # Evolution Loop
    for gen in range(1, generations + 1):
        # Selection
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Mutation
        for mutant in offspring:
            if random.random() < mutation_prob:
                toolbox.mutate(mutant)
                # Keep within bounds [0, 1]
                for k in range(len(mutant)):
                    mutant[k] = min(1.0, max(0.0, mutant[k]))
                del mutant.fitness.values

        # Re-evaluate invalid individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        fits = [ind.fitness.values[0] for ind in population]
        best_f = max(fits)
        avg_f = np.mean(fits)
        min_f = min(fits)

        convergence_history.append({
            "generation": gen,
            "best_fitness": round(float(best_f), 3),
            "avg_fitness": round(float(avg_f), 3),
            "min_fitness": round(float(min_f), 3)
        })

    exec_time = time.time() - start_time

    # Best Individual
    best_ind = tools.selBest(population, 1)[0]
    best_alloc = decode_and_repair(best_ind)

    # Convert to standard allocation matrix
    allocation_matrix: Dict[str, Dict[str, float]] = {r["name"]: {} for r in regions}
    for i, reg in enumerate(regions):
        r_name = reg["name"]
        for r, res in enumerate(resources):
            allocation_matrix[r_name][res["name"]] = round(float(best_alloc[i, r]), 1)

    # Vehicles and Teams proportional allocation
    from algorithms.linear_programming import _allocate_fleet_and_teams_proportional
    vehicle_allocation, team_allocation = _allocate_fleet_and_teams_proportional(problem, urgency_scores)

    result = compute_metrics_and_summary(
        problem=problem,
        allocation_matrix=allocation_matrix,
        vehicle_allocation=vehicle_allocation,
        team_allocation=team_allocation,
        execution_time_sec=exec_time,
        algorithm_name="Genetic Algorithm (DEAP)",
        objective_val=best_ind.fitness.values[0]
    )

    result.convergence_history = convergence_history
    result.summary["population_size"] = pop_size
    result.summary["total_generations"] = generations
    result.summary["crossover_prob"] = crossover_prob
    result.summary["mutation_prob"] = mutation_prob
    result.summary["final_best_fitness"] = round(best_ind.fitness.values[0], 2)
    result.summary["method"] = "Evolutionary Metaheuristic with Constraint Repair (Module V)"

    return result
