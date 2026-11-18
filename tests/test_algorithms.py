"""
Comprehensive test suite for DisasterShield AI optimization algorithms & dynamic SEOC system.
Tests allocation constraints, algorithm feasibility, edge cases, multi-state scenarios,
and official State Emergency Operations Centre (SEOC) detection across Indian states.
"""

import unittest
import numpy as np
import pandas as pd

from database.db import (
    init_db,
    get_all_regions,
    get_all_resources,
    get_all_vehicles,
    get_all_teams,
    get_all_state_hubs,
    get_state_hub,
    get_hubs_for_states,
    get_hub_verification_summary,
    get_active_hub_for_disaster,
    load_scenario_by_name,
    get_disaster_info
)
from algorithms.base import (
    OptimizationProblem,
    create_problem_from_db_records,
    verify_solution_feasibility
)
from algorithms.linear_programming import solve_linear_programming
from algorithms.integer_programming import solve_integer_programming
from algorithms.greedy import solve_greedy
from algorithms.genetic_algorithm import solve_genetic_algorithm
from algorithms.simulated_annealing import solve_simulated_annealing
from algorithms.multi_objective import solve_multi_objective
from utils.map_visualizer import create_disaster_map

class TestDisasterShieldAlgorithms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize database with default Tamil Nadu scenario for testing."""
        init_db(force_reset=True)
        cls.regions_df = get_all_regions()
        cls.resources_df = get_all_resources()
        cls.vehicles_df = get_all_vehicles()
        cls.teams_df = get_all_teams()
        cls.problem = create_problem_from_db_records(
            cls.regions_df, cls.resources_df, cls.vehicles_df, cls.teams_df, scenario_name="Test Baseline"
        )

    # ---------------------------------------------------------------------------------------------
    # 1. State-Wise SEOC Database & Directory Tests
    # ---------------------------------------------------------------------------------------------

    def test_state_emergency_hubs_database(self):
        """Verify all 28 Indian States and 8 Union Territories are seeded in the database."""
        hubs_df = get_all_state_hubs()
        self.assertEqual(len(hubs_df), 36, "Database must configure all 28 states and 8 union territories (36 total).")

        summary = get_hub_verification_summary()
        self.assertEqual(summary["total"], 36)
        self.assertEqual(summary["verified"], 35, "35 states/UTs have officially verified coordinates.")
        self.assertEqual(summary["unverified"], 1, "Lakshadweep is designated UNVERIFIED pending official site confirmation.")

    # ---------------------------------------------------------------------------------------------
    # 2. Automatic State Detection: Scenario Tests
    # ---------------------------------------------------------------------------------------------

    def test_tamil_nadu_flood_seoc(self):
        """Verify Flood in Tamil Nadu automatically binds to Tamil Nadu SEOC (Chennai)."""
        loaded = load_scenario_by_name("Tamil Nadu Flood & Coastal Surge")
        self.assertTrue(loaded)
        active_hub = get_active_hub_for_disaster()
        self.assertEqual(active_hub["state_name"], "Tamil Nadu")
        self.assertIn("Tamil Nadu State Emergency Operations Centre", active_hub["hub_name"])
        self.assertEqual(active_hub["verification_status"], "VERIFIED")
        self.assertAlmostEqual(active_hub["latitude"], 13.0645, places=3)
        self.assertAlmostEqual(active_hub["longitude"], 80.2810, places=3)

        # Run LP optimization
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        res = solve_linear_programming(prob)
        self.assertTrue(res.is_feasible)
        self.assertGreater(res.fulfilled_demand_ratio, 0.4)

    def test_odisha_cyclone_seoc(self):
        """Verify Cyclone in Odisha automatically binds to Odisha SEOC (OSDMA Bhubaneswar)."""
        loaded = load_scenario_by_name("Odisha Cyclone Dana (Bay of Bengal)")
        self.assertTrue(loaded)
        active_hub = get_active_hub_for_disaster()
        self.assertEqual(active_hub["state_name"], "Odisha")
        self.assertIn("OSDMA", active_hub["hub_name"])
        self.assertEqual(active_hub["verification_status"], "VERIFIED")
        self.assertAlmostEqual(active_hub["latitude"], 20.2706, places=3)
        self.assertAlmostEqual(active_hub["longitude"], 85.8334, places=3)

        # Run Greedy algorithm
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        res = solve_greedy(prob)
        self.assertTrue(res.is_feasible)

    def test_kerala_landslide_seoc(self):
        """Verify Landslide in Kerala automatically binds to Kerala SEOC (Thiruvananthapuram)."""
        loaded = load_scenario_by_name("Kerala Cloudburst & Wayanad Landslides")
        self.assertTrue(loaded)
        active_hub = get_active_hub_for_disaster()
        self.assertEqual(active_hub["state_name"], "Kerala")
        self.assertIn("Kerala State Emergency Operations Centre", active_hub["hub_name"])
        self.assertEqual(active_hub["verification_status"], "VERIFIED")
        self.assertAlmostEqual(active_hub["latitude"], 8.5060, places=3)
        self.assertAlmostEqual(active_hub["longitude"], 76.9740, places=3)

        # Run Integer Programming (IP)
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        res = solve_integer_programming(prob)
        self.assertTrue(res.is_feasible)

    def test_gujarat_earthquake_seoc(self):
        """Verify Earthquake in Gujarat automatically binds to Gujarat SEOC (Gandhinagar)."""
        loaded = load_scenario_by_name("Gujarat Kutch Fault Earthquake (M 7.1)")
        self.assertTrue(loaded)
        active_hub = get_active_hub_for_disaster()
        self.assertEqual(active_hub["state_name"], "Gujarat")
        self.assertIn("Gujarat State Disaster Management Authority", active_hub["hub_name"])
        self.assertEqual(active_hub["verification_status"], "VERIFIED")
        self.assertAlmostEqual(active_hub["latitude"], 23.2230, places=3)
        self.assertAlmostEqual(active_hub["longitude"], 72.6500, places=3)

        # Run Simulated Annealing (SA)
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        res = solve_simulated_annealing(prob, initial_temp=40.0, cooling_rate=0.90, min_temp=1.0, steps_per_temp=5)
        self.assertTrue(res.is_feasible)

    def test_simultaneous_multi_state_disasters(self):
        """Verify simultaneous disasters across Tamil Nadu & Kerala maintain separate state-wise plans and non-duplication."""
        loaded = load_scenario_by_name("South India Dual-State Flood (Tamil Nadu & Kerala)")
        self.assertTrue(loaded)

        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        self.assertTrue(prob.is_multi_state())
        states = prob.get_states()
        self.assertEqual(set(states), {"Tamil Nadu", "Kerala"})

        # Split into independent state subproblems
        state_problems = prob.split_by_state()
        self.assertEqual(len(state_problems), 2)
        self.assertIn("Tamil Nadu", state_problems)
        self.assertIn("Kerala", state_problems)

        # Check no resource is allocated twice
        tot_avail = prob.get_total_supply_by_resource()
        sum_split = {}
        for s_prob in state_problems.values():
            for res_name, sup in s_prob.get_total_supply_by_resource().items():
                sum_split[res_name] = sum_split.get(res_name, 0.0) + sup

        for res_name in tot_avail:
            self.assertAlmostEqual(tot_avail[res_name], sum_split[res_name], places=1, msg="Resource inventory must not be duplicated across states.")

        # Solve both independently
        res_tn = solve_linear_programming(state_problems["Tamil Nadu"])
        res_kl = solve_linear_programming(state_problems["Kerala"])
        self.assertTrue(res_tn.is_feasible)
        self.assertTrue(res_kl.is_feasible)

        # Inter-state transfer evaluation
        state_hubs = {"Tamil Nadu": get_state_hub("Tamil Nadu"), "Kerala": get_state_hub("Kerala")}
        transfers = prob.compute_inter_state_transfers({"Tamil Nadu": res_tn, "Kerala": res_kl}, state_hubs)
        self.assertIsInstance(transfers, list)

    def test_unverified_seoc_handling(self):
        """Verify unverified SEOC (Lakshadweep) is handled cleanly without placing fabricated coordinates."""
        loaded = load_scenario_by_name("Lakshadweep Archipelago Cyclone (Unverified SEOC)")
        self.assertTrue(loaded)

        active_hub = get_active_hub_for_disaster()
        self.assertEqual(active_hub["state_name"], "Lakshadweep")
        self.assertEqual(active_hub["verification_status"], "UNVERIFIED")
        self.assertIsNone(active_hub["latitude"])
        self.assertIsNone(active_hub["longitude"])
        self.assertIn("SEOC LOCATION NOT VERIFIED", active_hub["address"])

        # Map visualizer should build without crashing and without fabricating hub marker
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        folium_map = create_disaster_map(prob.regions, hubs=[active_hub])
        self.assertIsNotNone(folium_map)

    # ---------------------------------------------------------------------------------------------
    # 3. Core Algorithm Feasibility & Constraint Tests
    # ---------------------------------------------------------------------------------------------

    def test_genetic_algorithm_feasibility(self):
        """Verify GA repair operator enforces 100% feasibility."""
        load_scenario_by_name("Tamil Nadu Flood & Coastal Surge")
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        res = solve_genetic_algorithm(prob, pop_size=20, generations=10)
        self.assertTrue(res.is_feasible)

    def test_multi_objective_pareto_front(self):
        """Verify pymoo NSGA-II produces valid Pareto front trade-offs."""
        load_scenario_by_name("Tamil Nadu Flood & Coastal Surge")
        prob = create_problem_from_db_records(get_all_regions(), get_all_resources(), get_all_vehicles(), get_all_teams())
        res = solve_multi_objective(prob, pop_size=20, n_gen=10)
        self.assertTrue(res.is_feasible)
        self.assertIn("pareto_solutions", res.summary)

if __name__ == "__main__":
    unittest.main()
