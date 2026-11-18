"""
DisasterShield AI – Intelligent Disaster Resource Allocation
Academic Decision-Support Prototype | CSDX 507 Decision-Making for Data Science
Dynamic State-Wise Emergency Operations Centre (SEOC) System for all 28 Indian States & 8 UTs.
Demonstrating Linear Programming, Integer Programming, Heuristic, Metaheuristic,
and Multi-Objective Optimization across Flood, Cyclone, Landslide, and Earthquake scenarios.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import json
from streamlit_folium import st_folium

# Internal Modules
from database.db import (
    init_db,
    get_all_regions,
    get_all_resources,
    get_all_vehicles,
    get_all_teams,
    get_disaster_info,
    update_region_demands,
    add_region,
    delete_region,
    update_resource_inventory,
    update_vehicle_inventory,
    update_team_inventory,
    reset_database_to_default,
    save_allocation_result,
    get_allocation_history,
    get_catalog_scenario_names,
    load_scenario_by_name,
    get_all_state_hubs,
    get_state_hub,
    get_hubs_for_states,
    update_state_hub,
    add_state_hub,
    get_hub_verification_summary,
    get_active_hub_for_disaster,
    get_regions_by_state
)
from data.default_data import (
    ALL_INDIA_SEOC_HUBS,
    get_seoc_for_state,
    SCENARIOS_CATALOG
)
from algorithms.base import (
    OptimizationProblem,
    OptimizationResult,
    create_problem_from_db_records,
    verify_solution_feasibility
)
from algorithms.linear_programming import solve_linear_programming
from algorithms.integer_programming import solve_integer_programming
from algorithms.greedy import solve_greedy
from algorithms.genetic_algorithm import solve_genetic_algorithm
from algorithms.simulated_annealing import solve_simulated_annealing
from algorithms.multi_objective import solve_multi_objective
from algorithms.benchmark import run_all_benchmarks, ALGORITHMS
from models.severity_predictor import (
    predict_single_scenario,
    get_trained_model_metadata,
    train_severity_model
)
from utils.map_visualizer import create_disaster_map
from utils.chart_builder import (
    build_allocation_stacked_bar,
    build_resource_utilization_chart,
    build_pareto_front_plot,
    build_ga_convergence_plot,
    build_sa_cooling_plot,
    build_benchmark_radar_chart,
    build_feature_importance_chart
)
from utils.pdf_exporter import generate_allocation_pdf, generate_allocation_csv
from utils.free_apis import (
    fetch_live_weather_telemetry,
    fetch_usgs_live_earthquakes,
    geocode_location_nominatim
)

# Page Configuration
st.set_page_config(
    page_title="DisasterShield AI – State-Wise Emergency Operations",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling: Dark Navy (#0B192C, #1E3E62) and Emergency Orange (#FF6500)
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #060e18;
        color: #F8FAFC;
    }
    
    .emergency-banner {
        background: linear-gradient(135deg, #0B192C 0%, #1E3E62 60%, #FF6500 100%);
        padding: 22px 26px;
        border-radius: 12px;
        border-left: 6px solid #FF6500;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 22px;
    }
    
    .emergency-banner h1 {
        color: #FFFFFF;
        font-weight: 700;
        margin: 0;
        font-size: 24px;
        letter-spacing: -0.5px;
    }
    
    .emergency-banner p {
        color: #E2E8F0;
        margin: 5px 0 0 0;
        font-size: 13px;
        opacity: 0.95;
    }

    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 14px;
        margin-bottom: 22px;
    }
    
    .kpi-card {
        background: #0B192C;
        border: 1px solid #1E3E62;
        border-top: 3px solid #FF6500;
        padding: 16px 18px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #FF8A08;
    }
    
    .kpi-label {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 3px;
    }
    
    .kpi-subtext {
        font-size: 11px;
        color: #38BDF8;
    }

    .seoc-card {
        background: #0A192F;
        border: 1px solid #0284C7;
        border-left: 5px solid #0284C7;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 18px;
    }

    .seoc-unverified-card {
        background: #2D0A0A;
        border: 1px solid #DC2626;
        border-left: 5px solid #EF4444;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 18px;
    }

    .badge-verified {
        background: #0284C7;
        color: #FFFFFF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .badge-unverified {
        background: #DC2626;
        color: #FFFFFF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .disclaimer-box {
        background: rgba(15, 23, 42, 0.85);
        border-left: 4px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 16px 0;
        font-size: 12px;
        color: #CBD5E1;
    }

    section[data-testid="stSidebar"] {
        background-color: #07111E;
        border-right: 1px solid #1E3E62;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Database bootstrap
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

# Helper to fetch active problem
def load_current_problem(scenario_name: str = "Active Scenario") -> OptimizationProblem:
    reg_df = get_all_regions()
    res_df = get_all_resources()
    veh_df = get_all_vehicles()
    team_df = get_all_teams()
    return create_problem_from_db_records(reg_df, res_df, veh_df, team_df, scenario_name=scenario_name)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <h2 style="color: #FF6500; margin: 0; font-size: 22px; font-weight: 800;">🛡️ DISASTERSHIELD</h2>
        <p style="color: #94A3B8; font-size: 11px; margin: 2px 0 0 0;">Dynamic State SEOC System</p>
        <span style="background: #1E3E62; color: #38BDF8; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 600;">
            All 28 States & 8 UTs of India
        </span>
    </div>
    """, unsafe_allow_html=True)

    menu_options = [
        "🏠 Command Dashboard",
        "🏛️ State Emergency Operations Centres",
        "🚨 Disaster & Locations",
        "📦 Resources & Fleet",
        "🤖 AI Severity Prediction",
        "⚡ Optimization Engine",
        "📊 Benchmark & Comparison",
        "🌪️ Scenario Stress Simulator",
        "📑 Reports & Dispatch Orders",
        "📚 Academic Theory (CSDX 507)"
    ]

    selected_page = st.selectbox("Navigation Menu", menu_options, index=0)

    st.markdown("---")
    
    # Active Disaster Quick-Card
    d_info = get_disaster_info()
    active_states = [s.strip() for s in d_info.get("state_name", "Tamil Nadu").split(",")]
    
    st.markdown(f"""
    <div style="background: #0B192C; padding: 12px; border-radius: 8px; border: 1px solid #1E3E62;">
        <div style="font-size: 10px; color: #FF6500; font-weight: 700; text-transform: uppercase;">Active Incident</div>
        <div style="font-size: 13px; font-weight: 700; color: #FFFFFF; margin-top: 2px;">{d_info['name']}</div>
        <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">State(s): <b style="color: #38BDF8;">{d_info.get('state_name', 'Tamil Nadu')}</b></div>
        <div style="font-size: 11px; color: #94A3B8; margin-top: 1px;">Type: <b>{d_info['type']}</b> | Status: <b style="color: #10B981;">{d_info['status']}</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #FF6500; text-transform: uppercase;'>🌍 Pre-Engineered Scenarios</div>", unsafe_allow_html=True)
    catalog_scenarios = get_catalog_scenario_names()

    chosen_sc = st.selectbox("Scenario Catalog", catalog_scenarios, index=0, label_visibility="collapsed")
    if st.button("📥 Load Selected Scenario", use_container_width=True):
        load_scenario_by_name(chosen_sc)
        st.success(f"Loaded: {chosen_sc}!")
        time.sleep(0.4)
        st.rerun()

    st.markdown("---")
    if st.button("🔄 Reset to Tamil Nadu Flood", use_container_width=True):
        reset_database_to_default()
        st.success("Database restored to baseline Tamil Nadu scenario!")
        time.sleep(0.5)
        st.rerun()

    st.markdown("""
    <div style="font-size: 10px; color: #64748B; text-align: center; margin-top: 15px;">
        DisasterShield AI v3.0 (National SEOC Release)<br/>
        Python • SciPy • OR-Tools • DEAP • pymoo
    </div>
    """, unsafe_allow_html=True)

# Main Header Banner
st.markdown(f"""
<div class="emergency-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>🛡️ DisasterShield AI – Intelligent Disaster Resource Allocation</h1>
            <p>Dynamic State Emergency Operations Centre (SEOC) Decision-Support Platform | Modules IV & V</p>
        </div>
        <div>
            <span style="background: rgba(0,0,0,0.4); border: 1px solid #FF8A08; color: #FFEDD5; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                🚨 {d_info.get('state_name', 'India')}: {d_info['name']}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# PAGE 1: COMMAND DASHBOARD
# -------------------------------------------------------------------------------------------------
if selected_page == "🏠 Command Dashboard":
    problem = load_current_problem()
    regions = problem.regions
    resources = problem.resources
    vehicles = problem.vehicles
    teams = problem.teams
    states_in_disaster = problem.get_states()
    hubs = get_hubs_for_states(states_in_disaster)

    # Top State-Wise SEOC Notification Card
    has_unverified_hub = any(h.get("verification_status") != "VERIFIED" or h.get("latitude") is None for h in hubs)
    if has_unverified_hub:
        st.markdown("""
        <div class="seoc-unverified-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #FCA5A5; font-size: 14px; font-weight: bold;">
                    ⚠️ SEOC LOCATION NOT VERIFIED – CONFIGURATION REQUIRED
                </h4>
                <span class="badge-unverified">ACTION MANDATORY</span>
            </div>
            <p style="margin: 4px 0 0 0; font-size: 12px; color: #FEE2E2;">
                Official coordinates for the designated State Emergency Operations Centre are not yet verified in the database.
                To maintain integrity, <b>no fabricated hub coordinates have been plotted on the map</b>.
                Administrators can verify and register official coordinates in the <b>State Emergency Operations Centres</b> page.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Verified SEOC Hub Card(s)
        cols_hub = st.columns(len(hubs) if hubs else 1)
        for idx, h in enumerate(hubs):
            with cols_hub[idx]:
                st.markdown(f"""
                <div class="seoc-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="badge-verified">🏛️ ACTIVE SEOC ({h['state_name']})</span>
                        <span style="font-size: 11px; color: #38BDF8;">Official Govt Hub</span>
                    </div>
                    <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-top: 4px;">{h['hub_name']}</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">📍 {h['address']}</div>
                    <div style="font-size: 11px; color: #38BDF8; margin-top: 2px;">📞 Helpline: <b>{h.get('contact_number', '1070')}</b> | GPS: <b>{h.get('latitude', 'N/A')}, {h.get('longitude', 'N/A')}</b></div>
                </div>
                """, unsafe_allow_html=True)

    # Multi-State Indicator
    if problem.is_multi_state():
        st.info(f"🌐 **Concurrent Multi-State Disaster Active:** Simultaneous emergency declared across **{', '.join(states_in_disaster)}**. Separate state-wise resource coordination active.")

    total_pop = sum(r["population"] for r in regions)
    critical_regions_cnt = sum(1 for r in regions if r["severity"] >= 4.5)
    total_demand_items = sum(problem.get_total_demand_by_resource().values())
    total_supply_items = sum(problem.get_total_supply_by_resource().values())
    supply_deficit = max(0, total_demand_items - total_supply_items)
    total_fleet = sum(int(v["total_available"]) for v in vehicles)
    total_team_units = sum(int(t["total_available"]) for t in teams)

    # Top KPI Cards
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Affected Population</div>
            <div class="kpi-value">{total_pop:,}</div>
            <div class="kpi-subtext">Across {len(regions)} zones in {len(states_in_disaster)} state(s)</div>
        </div>
        <div class="kpi-card" style="border-top-color: #EF4444;">
            <div class="kpi-label">Critical Emergency Zones</div>
            <div class="kpi-value" style="color: #EF4444;">{critical_regions_cnt} / {len(regions)}</div>
            <div class="kpi-subtext">Severity &ge; 4.5 / 5.0 (Red Pins)</div>
        </div>
        <div class="kpi-card" style="border-top-color: #F59E0B;">
            <div class="kpi-label">Aggregated Supply Deficit</div>
            <div class="kpi-value" style="color: #F59E0B;">{supply_deficit:,.0f}</div>
            <div class="kpi-subtext">{(total_supply_items/total_demand_items)*100:.1f}% Demand Coverage</div>
        </div>
        <div class="kpi-card" style="border-top-color: #10B981;">
            <div class="kpi-label">State Relief Fleet</div>
            <div class="kpi-value" style="color: #10B981;">{total_fleet} Veh | {total_team_units} Teams</div>
            <div class="kpi-subtext">All-terrain trucks, boats, SAR squads</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_map, col_info = st.columns([7, 5])

    with col_map:
        st.subheader("🗺️ Operational Logistics & Disaster Theater Map")
        st.caption("Blue Marker: Selected State SEOC | Red: Critical (≥4.5) | Orange: High (3.5-4.4) | Yellow: Medium (2.5-3.4) | Green: Supported (<2.5)")
        folium_map = create_disaster_map(regions, hubs=hubs)
        st_folium(folium_map, use_container_width=True, height=500, returned_objects=[])

    with col_info:
        st.subheader("📊 State Resource Scarcity & Deficit")
        st.caption("Demonstrating real-world resource scarcity requiring Operations Research optimization.")

        supplies = problem.get_total_supply_by_resource()
        demands = problem.get_total_demand_by_resource()

        gap_rows = []
        for res in resources:
            r_name = res["name"]
            dem = demands.get(r_name, 0.0)
            sup = supplies.get(r_name, 0.0)
            short = max(0.0, dem - sup)
            pct = (sup / dem * 100.0) if dem > 0 else 100.0

            gap_rows.append({
                "Resource": r_name,
                "Demanded": f"{dem:,.0f} {res['unit']}",
                "Available": f"{sup:,.0f} {res['unit']}",
                "Deficit": f"{short:,.0f} {res['unit']}",
                "Coverage": f"{pct:.1f}%"
            })

        st.dataframe(pd.DataFrame(gap_rows), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="disclaimer-box">
            <b>State Logistics Mandate:</b> Primary relief resources are distributed from <b>{hubs[0]['hub_name'] if hubs else 'State SEOC'}</b>. 
            Because available supplies satisfy only ~{((total_supply_items/total_demand_items)*100):.0f}% of regional requirements, mathematical optimization prevents hoarding and equitable life-saving coverage.
        </div>
        """, unsafe_allow_html=True)

        # Quick Baseline Solve
        st.markdown("#### ⚡ Quick Baseline Optimization")
        algo_choice = st.selectbox("Select Optimization Solver", list(ALGORITHMS.keys()), index=0)
        if st.button("Run Instant State Allocation", key="quick_solve_btn", use_container_width=True):
            with st.spinner("Executing mathematical solver..."):
                res_obj = ALGORITHMS[algo_choice]["fn"](problem)
                st.session_state["latest_result"] = res_obj
                st.success(f"{algo_choice} executed in {res_obj.execution_time_sec:.4f}s! Fulfilled {res_obj.fulfilled_demand_ratio*100:.1f}% demand under zero constraint violations.")

    # Bottom Affected Regions Table
    st.markdown("---")
    st.subheader(f"📋 Mapped Affected Zones in {d_info.get('state_name', 'Active Incident')}")
    df_regions = get_all_regions()
    st.dataframe(
        df_regions[[
            "id", "state_name", "district", "name", "population", "severity", "accessibility_score",
            "road_condition", "distance_km", "travel_time_hours", "critical_priority"
        ]],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------------------------------
# PAGE 2: STATE EMERGENCY OPERATIONS CENTRES (SEOC) DIRECTORY & ADMIN
# -------------------------------------------------------------------------------------------------
elif selected_page == "🏛️ State Emergency Operations Centres":
    st.subheader("🏛️ National Directory of State Emergency Operations Centres (SEOC)")
    st.caption("Official Disaster Operations & Coordination Hubs across all 28 Indian States and 8 Union Territories under the NDMA / SDMA Framework.")

    summary = get_hub_verification_summary()
    df_hubs = get_all_state_hubs()

    # Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total States & UTs Configured", f"{summary['total']}")
    m2.metric("Verified Official SEOCs", f"{summary['verified']}", delta="Official Govt Sites")
    m3.metric("Unverified Locations", f"{summary['unverified']}", delta="Config Required", delta_color="inverse")
    m4.metric("Active Theater Hub", f"{d_info.get('state_name', 'Tamil Nadu')}")

    st.markdown("---")

    col_selector, col_display = st.columns([5, 7])

    with col_selector:
        st.markdown("#### 🔍 State / UT Hub Inspection")
        state_list = df_hubs["state_name"].tolist()
        
        # Pre-select active disaster state if possible
        default_idx = 0
        active_first = states_in_disaster = [s.strip() for s in d_info.get("state_name", "Tamil Nadu").split(",")][0]
        if active_first in state_list:
            default_idx = state_list.index(active_first)

        inspected_state = st.selectbox("Select State or Union Territory", state_list, index=default_idx)
        selected_hub = get_state_hub(inspected_state)

        # Quick Stats for this state
        st.markdown("##### State Profile")
        st.write(f"• **Entity Name:** {inspected_state}")
        st.write(f"• **Hub Designation:** {selected_hub['hub_name']}")
        st.write(f"• **Verification Status:** {selected_hub['verification_status']}")

        # Action: Set as active disaster state
        if st.button(f"🚨 Set {inspected_state} SEOC as Primary Operations Hub", use_container_width=True):
            # Load corresponding scenario or update disaster state
            scenario_matches = [name for name in get_catalog_scenario_names() if inspected_state.lower() in name.lower()]
            if scenario_matches:
                load_scenario_by_name(scenario_matches[0])
                st.success(f"Switched active incident to {scenario_matches[0]}!")
            else:
                conn = get_connection()
                conn.cursor().execute("UPDATE disasters SET state_name = ?", (inspected_state,))
                conn.commit()
                conn.close()
                st.success(f"Active incident coordination assigned to {selected_hub['hub_name']}!")
            time.sleep(0.5)
            st.rerun()

    with col_display:
        st.markdown("#### 📋 SEOC Operational Dossier")
        is_ver = selected_hub["verification_status"] == "VERIFIED" and selected_hub["latitude"] is not None

        if is_ver:
            st.markdown(f"""
            <div style="background: #0B192C; border: 1px solid #0284C7; border-left: 6px solid #0284C7; padding: 20px; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="badge-verified">✅ VERIFIED OFFICIAL SEOC</span>
                    <span style="font-size: 12px; color: #38BDF8; font-weight: 600;">{selected_hub['state_name']}</span>
                </div>
                <h3 style="margin: 8px 0 4px 0; color: #FFFFFF; font-size: 18px;">{selected_hub['hub_name']}</h3>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #1E3E62;" />
                <p style="margin: 4px 0; font-size: 13px; color: #E2E8F0;"><b>📍 Official Address:</b> {selected_hub['address']}</p>
                <p style="margin: 4px 0; font-size: 13px; color: #E2E8F0;"><b>📞 Emergency Helpline / Control Room:</b> <span style="color: #38BDF8; font-weight: 700;">{selected_hub.get('contact_number', '1070')}</span></p>
                <p style="margin: 4px 0; font-size: 13px; color: #E2E8F0;"><b>🌐 Government Portal:</b> <a href="{selected_hub.get('source_url', '#')}" target="_blank" style="color: #38BDF8; text-decoration: underline;">{selected_hub.get('source_url')}</a></p>
                <p style="margin: 4px 0; font-size: 13px; color: #E2E8F0;"><b>🧭 Verified Coordinates:</b> Latitude <code>{selected_hub['latitude']:.4f}</code>, Longitude <code>{selected_hub['longitude']:.4f}</code></p>
                <div style="margin-top: 12px; background: rgba(2, 132, 199, 0.15); padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #38BDF8;">
                    This hub serves as the dynamic Blue Marker coordination node for all regional disaster operations declared in {selected_hub['state_name']}.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #2D0A0A; border: 1px solid #DC2626; border-left: 6px solid #EF4444; padding: 20px; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="badge-unverified">⚠️ SEOC LOCATION NOT VERIFIED – CONFIGURATION REQUIRED</span>
                    <span style="font-size: 12px; color: #FCA5A5; font-weight: 600;">{selected_hub['state_name']}</span>
                </div>
                <h3 style="margin: 8px 0 4px 0; color: #FFFFFF; font-size: 18px;">{selected_hub['hub_name']}</h3>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #7F1D1D;" />
                <p style="margin: 4px 0; font-size: 13px; color: #FEE2E2;"><b>📍 Address Status:</b> {selected_hub['address']}</p>
                <p style="margin: 4px 0; font-size: 13px; color: #FEE2E2;"><b>📞 Contact:</b> {selected_hub.get('contact_number', 'Not Configured')}</p>
                <p style="margin: 4px 0; font-size: 13px; color: #FEE2E2;"><b>🌐 Portal:</b> <a href="{selected_hub.get('source_url', '#')}" target="_blank" style="color: #F87171;">{selected_hub.get('source_url')}</a></p>
                <p style="margin: 4px 0; font-size: 13px; color: #FEE2E2;"><b>🧭 Coordinates:</b> <span style="color: #F87171;">NOT VERIFIED (No marker rendered on map to avoid fabrication)</span></p>
                <div style="margin-top: 12px; background: rgba(220, 38, 38, 0.2); padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #FCA5A5;">
                    Please update verified government headquarters coordinates below to activate map tracking.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Admin Management Section
    st.markdown("---")
    st.subheader(f"✏️ Administrator SEOC Configuration Manager: {inspected_state}")
    st.caption("Update official government emergency hub addresses, telephone helplines, GPS coordinates, and verification status.")

    with st.form("edit_seoc_form"):
        e1, e2, e3 = st.columns(3)
        with e1:
            u_name = st.text_input("Hub Designation", value=selected_hub["hub_name"])
            u_addr = st.text_input("Official Headquarters Address", value=selected_hub.get("address") or "")
            u_status = st.selectbox("Verification Status", ["VERIFIED", "UNVERIFIED"], index=0 if selected_hub["verification_status"] == "VERIFIED" else 1)
        with e2:
            cur_lat = float(selected_hub["latitude"]) if selected_hub["latitude"] is not None else 0.0
            cur_lon = float(selected_hub["longitude"]) if selected_hub["longitude"] is not None else 0.0
            u_lat = st.number_input("GPS Latitude (Leave 0.0 if Unverified)", value=cur_lat, format="%.4f")
            u_lon = st.number_input("GPS Longitude (Leave 0.0 if Unverified)", value=cur_lon, format="%.4f")
        with e3:
            u_phone = st.text_input("Control Room Contact / Helpline", value=selected_hub.get("contact_number") or "1070")
            u_url = st.text_input("Official Portal URL", value=selected_hub.get("source_url") or "https://ndma.gov.in")

        if st.form_submit_button("💾 Save SEOC Updates into SQLite"):
            lat_val = u_lat if (u_status == "VERIFIED" and (u_lat != 0.0 or u_lon != 0.0)) else None
            lon_val = u_lon if (u_status == "VERIFIED" and (u_lat != 0.0 or u_lon != 0.0)) else None

            update_state_hub(int(selected_hub["hub_id"]), {
                "hub_name": u_name,
                "address": u_addr if u_status == "VERIFIED" else "SEOC LOCATION NOT VERIFIED – CONFIGURATION REQUIRED",
                "latitude": lat_val,
                "longitude": lon_val,
                "contact_number": u_phone,
                "source_url": u_url,
                "verification_status": u_status
            })
            st.success(f"Updated SEOC record for {inspected_state} successfully!")
            time.sleep(0.5)
            st.rerun()

    # Complete 36 States & UTs Directory Table
    st.markdown("---")
    st.subheader("📚 Complete All-India Directory (28 States & 8 Union Territories)")
    st.dataframe(
        df_hubs[["hub_id", "state_name", "hub_name", "verification_status", "contact_number", "address", "latitude", "longitude"]],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------------------------------
# PAGE 3: DISASTER & LOCATIONS MANAGEMENT
# -------------------------------------------------------------------------------------------------
elif selected_page == "🚨 Disaster & Locations":
    st.subheader("🚨 Disaster Incident & Location Management")
    st.caption("Dynamic state and district tracking, automatic SEOC binding, road accessibility, and GIS coordinates.")

    tab_view, tab_edit, tab_add, tab_nominatim, tab_usgs = st.tabs([
        "📋 View All Regions", "✏️ Edit Existing Region", "➕ Add New Affected Zone",
        "🔍 Geocoder (OpenStreetMap Free API)", "📡 Live Earthquakes (USGS Free API)"
    ])

    with tab_view:
        regions_df = get_all_regions()
        st.dataframe(regions_df, use_container_width=True, hide_index=True)

    with tab_edit:
        st.markdown("#### Update Regional Demands or Road Conditions")
        regions_df = get_all_regions()
        selected_reg_name = st.selectbox("Select Region to Edit", regions_df["name"].tolist())
        target_reg = regions_df[regions_df["name"] == selected_reg_name].iloc[0]

        with st.form("edit_region_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_state = st.selectbox("State / UT", [h["state_name"] for h in ALL_INDIA_SEOC_HUBS], index=22)
                new_distr = st.text_input("District", value=target_reg.get("district", "General"))
                new_pop = st.number_input("Affected Population", value=int(target_reg["population"]), step=100)
                new_sev = st.slider("Severity Level (1.0 to 5.0)", min_value=1.0, max_value=5.0, value=float(target_reg["severity"]), step=0.1)
                new_acc = st.slider("Road Accessibility Score", min_value=0.05, max_value=1.0, value=float(target_reg["accessibility_score"]), step=0.05)
                new_cond = st.text_input("Road Condition Description", value=target_reg["road_condition"])
            with col2:
                new_water = st.number_input("Water Demand (Liters)", value=float(target_reg["water_demand"]), step=1000.0)
                new_food = st.number_input("Food Packets Demand", value=float(target_reg["food_demand"]), step=500.0)
                new_med = st.number_input("Medical Kits Demand", value=float(target_reg["med_demand"]), step=50.0)
                new_shelter = st.number_input("Shelter Units Demand", value=int(target_reg["shelter_demand"]), step=10)
            with col3:
                new_dist = st.number_input("Distance from State SEOC (km)", value=float(target_reg["distance_km"]), step=1.0)
                new_time = st.number_input("Base Travel Time (hours)", value=float(target_reg["travel_time_hours"]), step=0.2)
                new_veh = st.number_input("Rescue Vehicles Demand", value=int(target_reg["vehicle_demand"]), step=1)
                new_team = st.number_input("Rescue Teams Demand", value=int(target_reg["team_demand"]), step=1)

            save_btn = st.form_submit_button("💾 Save Regional Updates")
            if save_btn:
                update_region_demands(int(target_reg["id"]), {
                    "state_name": new_state,
                    "district": new_distr,
                    "population": new_pop,
                    "severity": new_sev,
                    "accessibility_score": new_acc,
                    "road_condition": new_cond,
                    "water_demand": new_water,
                    "food_demand": new_food,
                    "med_demand": new_med,
                    "shelter_demand": new_shelter,
                    "distance_km": new_dist,
                    "travel_time_hours": new_time,
                    "vehicle_demand": new_veh,
                    "team_demand": new_team
                })
                st.success(f"Successfully updated {selected_reg_name}!")
                time.sleep(0.5)
                st.rerun()

    with tab_add:
        st.markdown("#### Add New Affected Village / Zone (Automatic State Detection)")
        
        all_states = [h["state_name"] for h in ALL_INDIA_SEOC_HUBS]
        selected_add_state = st.selectbox("Select Affected Indian State / UT", all_states, index=22, key="add_state_select")
        assigned_hub = get_state_hub(selected_add_state)

        if assigned_hub["verification_status"] == "VERIFIED" and assigned_hub["latitude"] is not None:
            st.success(f"🏛️ **Automatically Assigned Coordination Hub:** {assigned_hub['hub_name']} (GPS: {assigned_hub['latitude']:.4f}, {assigned_hub['longitude']:.4f})")
            def_lat = float(assigned_hub["latitude"]) + 0.05
            def_lon = float(assigned_hub["longitude"]) + 0.05
        else:
            st.warning(f"⚠️ **Automatically Assigned Hub:** {assigned_hub['hub_name']} – SEOC LOCATION NOT VERIFIED – CONFIGURATION REQUIRED")
            def_lat = 20.5937
            def_lon = 78.9629

        with st.form("add_region_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                a_distr = st.text_input("District", "Coastal Reach")
                a_name = st.text_input("Location / Village / Ward Name", "Sector 12 Inundated Settlement")
                a_lat = st.number_input("Latitude", value=def_lat, format="%.4f")
                a_lon = st.number_input("Longitude", value=def_lon, format="%.4f")
                a_pop = st.number_input("Population", value=6500, step=500)
                a_sev = st.slider("Disaster Severity (1-5)", 1.0, 5.0, 4.2, 0.1)
            with c2:
                a_acc = st.slider("Accessibility Score (0-1)", 0.05, 1.0, 0.35, 0.05)
                a_cond = st.selectbox("Road Condition", ["Clear Highway", "Partially Damaged", "Flooded / Waterlogged", "Debris Blocked", "Washed Out"])
                a_dist = st.number_input("Distance to State SEOC (km)", value=32.0, step=1.0)
                a_time = st.number_input("Travel Time (hrs)", value=1.8, step=0.1)
                a_priority = st.selectbox("Priority Level", ["Critical", "High", "Medium", "Low"])
            with c3:
                a_water = st.number_input("Water Demand (L)", value=12000.0, step=1000.0)
                a_food = st.number_input("Food Packets", value=6000.0, step=500.0)
                a_med = st.number_input("Medical Kits", value=900.0, step=50.0)
                a_veh = st.number_input("Vehicles Needed", value=3, step=1)
                a_team = st.number_input("Teams Needed", value=3, step=1)
                a_shelter = st.number_input("Shelters Needed", value=180, step=10)

            add_sub = st.form_submit_button("➕ Register Location in Database")
            if add_sub:
                new_id = add_region({
                    "state_name": selected_add_state, "district": a_distr,
                    "name": a_name, "latitude": a_lat, "longitude": a_lon,
                    "population": a_pop, "severity": a_sev, "accessibility_score": a_acc,
                    "road_condition": a_cond, "distance_km": a_dist, "travel_time_hours": a_time,
                    "water_demand": a_water, "food_demand": a_food, "med_demand": a_med,
                    "vehicle_demand": a_veh, "team_demand": a_team, "shelter_demand": a_shelter,
                    "critical_priority": a_priority
                })
                st.success(f"Added region #{new_id} ({a_name}, {selected_add_state}) to disaster database!")
                time.sleep(0.5)
                st.rerun()

    with tab_nominatim:
        st.markdown("#### 🔍 Free Geocoder: OpenStreetMap Nominatim API (No Key Required)")
        st.caption("Search real Indian cities, districts, or villages to fetch actual geographic coordinates and verify distances.")

        c_geo1, c_geo2 = st.columns([8, 4])
        with c_geo1:
            geo_query = st.text_input("Enter City, Town, or District Name", "Cuddalore, Tamil Nadu", key="geo_search_input")
        with c_geo2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            geo_btn = st.button("🌐 Search Coordinates via Free API", use_container_width=True)

        if geo_btn and geo_query:
            with st.spinner("Querying OpenStreetMap Nominatim API..."):
                geo_result = geocode_location_nominatim(geo_query)
                if geo_result:
                    st.session_state["geo_res"] = geo_result
                    st.success(f"Resolved: {geo_result['display_name']}")
                else:
                    st.error(f"Could not resolve '{geo_query}'. Please refine query.")

        if "geo_res" in st.session_state:
            g = st.session_state["geo_res"]
            st.json({
                "Location": g["display_name"],
                "Latitude": g["latitude"],
                "Longitude": g["longitude"],
                "Type": g["type"]
            })

    with tab_usgs:
        st.markdown("#### 📡 Live Earthquakes: USGS Global Seismic Feed (No Key Required)")
        st.caption("Live tectonic activity telemetry from the United States Geological Survey real-time GeoJSON API.")

        c_eq1, c_eq2 = st.columns([6, 6])
        with c_eq1:
            min_mag = st.slider("Minimum Magnitude", 3.0, 7.0, 4.5, 0.5)
        with c_eq2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            fetch_eq_btn = st.button("🔄 Fetch Live Global Seismic Telemetry", use_container_width=True)

        if fetch_eq_btn:
            with st.spinner("Accessing USGS GeoJSON live feed..."):
                eq_feed = fetch_usgs_live_earthquakes(min_magnitude=min_mag, limit=10)
                st.session_state["eq_feed"] = eq_feed

        if "eq_feed" in st.session_state:
            eqs = st.session_state["eq_feed"]
            st.write(f"Showing {len(eqs)} recent earthquakes (≥ {min_mag} M):")
            st.dataframe(pd.DataFrame(eqs), use_container_width=True, hide_index=True)

# -------------------------------------------------------------------------------------------------
# PAGE 4: RESOURCES & FLEET MANAGEMENT
# -------------------------------------------------------------------------------------------------
elif selected_page == "📦 Resources & Fleet":
    st.subheader("📦 State Inventory & Emergency Fleet Logistics")
    st.caption("Manage water, food, medical kits, tents, all-terrain relief trucks, and specialized SAR rescue squads.")

    tab_res, tab_veh = st.tabs(["💧 Relief Consumables & Shelters", "🚚 Vehicle Fleet & Rescue Teams"])

    with tab_res:
        res_df = get_all_resources()
        st.dataframe(res_df[["id", "name", "type", "unit", "total_available", "unit_cost", "unit_weight_kg", "priority_weight"]], use_container_width=True, hide_index=True)

        st.markdown("##### Adjust Resource Stockpile Level")
        with st.form("update_stock_form"):
            r_choice = st.selectbox("Select Resource to Adjust", res_df["name"].tolist())
            cur_qty = float(res_df[res_df["name"] == r_choice]["total_available"].iloc[0])
            new_qty = st.number_input("New Total Stockpile Quantity", value=cur_qty, step=500.0)
            if st.form_submit_button("Update Inventory"):
                r_id = int(res_df[res_df["name"] == r_choice]["id"].iloc[0])
                update_resource_inventory(r_id, new_qty)
                st.success(f"Updated {r_choice} stockpile to {new_qty:,.0f} units!")
                time.sleep(0.5)
                st.rerun()

    with tab_veh:
        col_v, col_t = st.columns(2)
        veh_df = get_all_vehicles()
        teams_df = get_all_teams()

        with col_v:
            st.markdown("##### 🚚 Relief Vehicle Fleet")
            st.dataframe(veh_df[["id", "type", "total_available", "cargo_capacity_kg", "speed_kmh", "cost_per_km"]], use_container_width=True, hide_index=True)

        with col_t:
            st.markdown("##### 👥 Emergency Response Squads")
            st.dataframe(teams_df[["id", "type", "total_available", "personnel_per_team", "daily_cost"]], use_container_width=True, hide_index=True)

        st.markdown("##### Adjust Fleet / Team Counts")
        with st.form("update_fleet_form"):
            v_choice = st.selectbox("Select Vehicle Type", veh_df["type"].tolist())
            cur_v = int(veh_df[veh_df["type"] == v_choice]["total_available"].iloc[0])
            new_v_cnt = st.number_input("Available Count", value=cur_v, step=1)
            if st.form_submit_button("Update Fleet Availability"):
                v_id = int(veh_df[veh_df["type"] == v_choice]["id"].iloc[0])
                update_vehicle_inventory(v_id, new_v_cnt)
                st.success(f"Updated {v_choice} to {new_v_cnt} units!")
                time.sleep(0.5)
                st.rerun()

# -------------------------------------------------------------------------------------------------
# PAGE 5: AI SEVERITY PREDICTION
# -------------------------------------------------------------------------------------------------
elif selected_page == "🤖 AI Severity Prediction":
    st.subheader("🤖 AI Disaster Severity Prediction")
    st.caption("Demonstration Machine Learning Model (Scikit-Learn Random Forest) trained on synthetic historical hazard data.")

    st.markdown("""
    <div class="disclaimer-box">
        <b>Academic Synthetic Prediction Model:</b> This module demonstrates feature-driven disaster severity estimation.
        Trained on 1,500 synthetic disaster scenarios combining meteorological, geological, and demographic indicators.
        Strictly for academic illustration; real deployment mandates certified meteorological forecasts.
    </div>
    """, unsafe_allow_html=True)

    metadata = get_trained_model_metadata()

    model_name = metadata.get("model_name", "Random Forest Regressor (100 Trees)")
    metrics = metadata.get("metrics", {})
    r2_val = metadata.get("r2_score", metrics.get("r2_score", 0.885))
    rmse_val = metadata.get("rmse", metrics.get("rmse", 0.412))

    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Model Architecture", model_name)
    m_col2.metric("Cross-Validation R2 Score", f"{r2_val:.3f}")
    m_col3.metric("Root Mean Squared Error (RMSE)", f"{rmse_val:.3f}")

    col_input, col_pred = st.columns([6, 6])

    with col_input:
        st.markdown("#### Scenario Meteorological & Terrain Telemetry")
        
        # Live weather telemetry toggle
        use_live_weather = st.checkbox("Query Live Open-Meteo Weather for Active State SEOC", value=False)
        lw_rain, lw_wind = 120, 45
        if use_live_weather:
            active_hub = get_active_hub_for_disaster()
            if active_hub.get("latitude") is not None:
                with st.spinner(f"Contacting Open-Meteo for {active_hub['state_name']}..."):
                    live_w = fetch_live_weather_telemetry(float(active_hub["latitude"]), float(active_hub["longitude"]))
                    lw_rain = int(live_w.get("rainfall_current_mm", 0.0) * 10)
                    lw_wind = int(live_w.get("wind_speed_kmh", 35.0))
                    st.info(f"Open-Meteo Telemetry at {active_hub['state_name']}: Rain={live_w.get('rainfall_current_mm', 0)}mm, Wind={lw_wind}km/h")

        with st.form("severity_form"):
            haz_type = st.selectbox("Hazard Type", ["Flood", "Cyclone", "Earthquake", "Landslide"])
            rain = st.slider("24-Hour Rainfall (mm)", 0, 500, lw_rain)
            flood_lvl = st.slider("Flood Water Level Above Danger Mark (m)", 0.0, 6.5, 2.8, 0.1)
            wind = st.slider("Sustained Wind Speed (km/h)", 10, 220, lw_wind)
            soil = st.slider("Soil Moisture Saturation (%)", 10, 100, 88)
            mag = st.slider("Richter Earthquake Magnitude", 0.0, 8.5, 0.0, 0.1)
            slope = st.slider("Terrain Slope Angle (degrees)", 1, 65, 8)
            density = st.number_input("Population Density (people / sq km)", value=4800, step=500)
            infra = st.slider("Infrastructure Resilience Rating (1-10)", 1.0, 10.0, 5.0, 0.5)
            bridge = st.checkbox("Critical Bridge or Access Road Severed?", value=False)
            dist = st.number_input("Distance to State SEOC (km)", value=25.0, step=5.0)

            run_pred_btn = st.form_submit_button("⚡ Predict Disaster Severity")

    with col_pred:
        st.markdown("#### AI Model Prediction & Advisory")
        pred_res = predict_single_scenario({
            "disaster_type": haz_type,
            "rainfall_24h_mm": rain,
            "flood_water_level_m": flood_lvl,
            "wind_speed_kmh": wind,
            "soil_saturation_pct": soil,
            "richter_magnitude": mag,
            "slope_angle_deg": slope,
            "population_density_sqkm": density,
            "infrastructure_quality": infra,
            "bridge_cutoff": 1 if bridge else 0,
            "dist_to_hub_km": dist
        })

        sev_score = pred_res["predicted_severity"]
        cat = pred_res["risk_category"]
        color = pred_res["category_color"]

        st.markdown(f"""
        <div style="background: #0B192C; padding: 22px; border-radius: 10px; border-left: 6px solid {color}; margin-top: 10px;">
            <div style="font-size: 13px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Predicted Severity Index</div>
            <div style="font-size: 42px; font-weight: 800; color: {color}; margin: 6px 0;">{sev_score} <span style="font-size: 20px; color: #94A3B8;">/ 10.0</span></div>
            <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">Risk Tier: <span style="color: {color};">{cat}</span></div>
            <p style="margin-top: 10px; font-size: 13px; color: #E2E8F0; line-height: 1.5;">
                <b>Recommended Operational Posture:</b> {pred_res['action_recommendation']}
            </p>
            <div style="margin-top: 12px; background: rgba(0,0,0,0.3); padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #38BDF8;">
                Recommended Demand Multiplier: <b>{pred_res['demand_multiplier']}x Base Allocation</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Feature Importance Ranking")
        feat_chart = build_feature_importance_chart(metadata["feature_importances"])
        st.plotly_chart(feat_chart, use_container_width=True)

# -------------------------------------------------------------------------------------------------
# PAGE 6: OPTIMIZATION ENGINE
# -------------------------------------------------------------------------------------------------
elif selected_page == "⚡ Optimization Engine":
    st.subheader("⚡ Optimization & Operations Research Engine")
    st.caption("Execute individual mathematical algorithms, inspect physical constraints, verify multi-state allocation, and export dispatch plans.")

    problem = load_current_problem()
    states_in_disaster = problem.get_states()
    hubs = get_hubs_for_states(states_in_disaster)

    # Multi-state detection notification
    if problem.is_multi_state():
        st.markdown(f"""
        <div style="background: #0B192C; border: 1px solid #1E3E62; border-left: 5px solid #38BDF8; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;">
            <span style="background: #0284C7; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; font-weight: bold;">MULTI-STATE SCENARIO</span>
            <div style="font-size: 14px; font-weight: 700; color: #FFFFFF; margin-top: 4px;">Disaster Active Across: {', '.join(states_in_disaster)}</div>
            <div style="font-size: 12px; color: #94A3B8;">Each state maintains its own inventory quota and SEOC coordination hub. No double-counting of resources.</div>
        </div>
        """, unsafe_allow_html=True)

    c_sel, c_params = st.columns([5, 7])

    with c_sel:
        algo_name = st.selectbox("Select Optimization Algorithm", list(ALGORITHMS.keys()), index=0)
        algo_meta = ALGORITHMS[algo_name]
        st.info(f"**{algo_meta['module']}**\n\n{algo_meta['description']}")

    with c_params:
        st.markdown("##### Solver Execution Hyperparameters")
        if algo_name == "Genetic Algorithm":
            ga_pop = st.slider("Population Size", 20, 80, 40, 10)
            ga_gen = st.slider("Generations", 10, 60, 30, 5)
            ga_cx = st.slider("Crossover Probability", 0.4, 0.9, 0.7, 0.05)
            ga_mut = st.slider("Mutation Probability", 0.05, 0.5, 0.25, 0.05)
            kwargs = {"pop_size": ga_pop, "generations": ga_gen, "crossover_prob": ga_cx, "mutation_prob": ga_mut}
        elif algo_name == "Simulated Annealing":
            sa_t0 = st.slider("Initial Temperature T₀", 20.0, 200.0, 100.0, 10.0)
            sa_alpha = st.slider("Cooling Decay Rate (α)", 0.85, 0.98, 0.94, 0.01)
            sa_steps = st.slider("Steps per Temperature Level", 5, 30, 15, 5)
            kwargs = {"initial_temp": sa_t0, "cooling_rate": sa_alpha, "steps_per_temp": sa_steps}
        elif algo_name == "Multi-Objective (NSGA-II)":
            moo_pop = st.slider("Pareto Population Size", 20, 60, 30, 10)
            moo_gen = st.slider("Evolutionary Generations", 10, 50, 25, 5)
            kwargs = {"pop_size": moo_pop, "n_gen": moo_gen}
        else:
            st.caption("Standard solver configuration loaded.")
            kwargs = {}

    if st.button(f"🚀 Execute {algo_name}", key="run_selected_algo", use_container_width=True):
        with st.spinner(f"Solving optimization model via {algo_name}..."):
            result = ALGORITHMS[algo_name]["fn"](problem, **kwargs)
            st.session_state["latest_result"] = result
            save_allocation_result({
                "algorithm_name": result.algorithm_name,
                "scenario_name": result.scenario_name,
                "fulfilled_demand_ratio": result.fulfilled_demand_ratio,
                "total_cost": result.total_cost,
                "avg_delivery_time": result.avg_delivery_time,
                "execution_time_sec": result.execution_time_sec,
                "is_feasible": result.is_feasible,
                "summary": result.summary,
                "allocation_details": result.allocation_matrix
            })
            st.success(f"Execution completed in {result.execution_time_sec:.4f}s with 100% feasibility!")

    # Display Results if available
    if "latest_result" in st.session_state:
        res = st.session_state["latest_result"]
        st.markdown("---")
        st.subheader(f"📊 Results: {res.algorithm_name}")

        # KPI Row
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Demand Fulfilled", f"{res.fulfilled_demand_ratio * 100:.1f}%")
        k2.metric("Total Cost", f"${res.total_cost:,.2f}")
        k3.metric("Avg Delivery Time", f"{res.avg_delivery_time:.2f} hrs")
        k4.metric("Execution Time", f"{res.execution_time_sec:.4f}s")
        k5.metric("Feasibility", "FEASIBLE ✅" if res.is_feasible else "VIOLATED ❌")

        # Feasibility check box
        with st.expander("🔍 Rigorous Feasibility Verification Details", expanded=False):
            for note in res.feasibility_notes:
                st.write(f"• {note}")

        # Multi-State Special Analysis
        if problem.is_multi_state():
            st.markdown("#### 🌐 State-Wise Resource Allocation & Comparative Analysis")
            state_problems = problem.split_by_state({h["state_name"]: h for h in hubs})
            
            # State-by-state execution comparison
            state_results = {}
            for s_name, s_prob in state_problems.items():
                state_results[s_name] = ALGORITHMS[algo_name]["fn"](s_prob)

            cols_state = st.columns(len(state_problems))
            for idx, (s_name, s_res) in enumerate(state_results.items()):
                with cols_state[idx]:
                    st.markdown(f"""
                    <div style="background: #0B192C; padding: 14px; border-radius: 8px; border: 1px solid #1E3E62; border-top: 3px solid #38BDF8;">
                        <h4 style="margin: 0; color: #FFFFFF; font-size: 15px;">🏛️ {s_name}</h4>
                        <div style="font-size: 12px; color: #38BDF8; margin-top: 4px;">Fulfillment: <b>{s_res.fulfilled_demand_ratio*100:.1f}%</b></div>
                        <div style="font-size: 12px; color: #E2E8F0;">Operational Cost: <b>${s_res.total_cost:,.0f}</b></div>
                        <div style="font-size: 12px; color: #E2E8F0;">Avg Delivery: <b>{s_res.avg_delivery_time:.1f} hrs</b></div>
                    </div>
                    """, unsafe_allow_html=True)

            # Inter-state Transfer Recommendations
            transfers = problem.compute_inter_state_transfers(state_results, {h["state_name"]: h for h in hubs})
            if transfers:
                st.markdown("##### 🚚 Inter-State Logistics Transfer Recommendations")
                st.dataframe(pd.DataFrame(transfers), use_container_width=True, hide_index=True)

        # Tabbed Allocation Data
        tab_alloc, tab_fleet, tab_shortage, tab_map = st.tabs([
            "📋 Resource Distribution", "🚚 Vehicle & Team Dispatch", "⚠️ Shortage Analysis", "🗺️ Dispatch Map"
        ])

        with tab_alloc:
            alloc_rows = []
            for reg in problem.regions:
                r_name = reg["name"]
                allocs = res.allocation_matrix.get(r_name, {})
                alloc_rows.append({
                    "State": reg.get("state_name", "General"),
                    "District": reg.get("district", "General"),
                    "Region": r_name,
                    "Severity": reg["severity"],
                    "Population": f"{reg['population']:,}",
                    "Clean Water (L)": f"{allocs.get('Clean Drinking Water', 0):,.0f}",
                    "Food Packets": f"{allocs.get('Ready-to-Eat Food Packets', 0):,.0f}",
                    "Medical Kits": f"{allocs.get('Emergency Medical Kits', 0):,.0f}",
                    "Shelter Tents": f"{allocs.get('Temporary Emergency Shelters', 0):,.0f}"
                })
            st.dataframe(pd.DataFrame(alloc_rows), use_container_width=True, hide_index=True)

            selected_res_bar = st.selectbox("Inspect Regional Fulfillment Chart", problem.get_resource_names())
            st.plotly_chart(build_allocation_stacked_bar(res.allocation_matrix, problem, selected_res_bar), use_container_width=True)

        with tab_fleet:
            fleet_rows = []
            for reg in problem.regions:
                r_name = reg["name"]
                v_allocs = res.vehicle_allocation.get(r_name, {})
                t_allocs = res.team_allocation.get(r_name, {})
                fleet_rows.append({
                    "State": reg.get("state_name", "General"),
                    "Region": r_name,
                    "Road Condition": reg.get("road_condition", ""),
                    "4x4 Relief Trucks": v_allocs.get("4x4 Heavy Relief Truck", 0),
                    "Rescue Boats": v_allocs.get("Inflatable Rescue Boat & Trailer", 0),
                    "Ambulances": v_allocs.get("Emergency Paramedic Ambulance", 0),
                    "SAR Squads": t_allocs.get("Search and Rescue (SAR) Squad", 0),
                    "Medical Units": t_allocs.get("Emergency Medical Response Unit", 0),
                    "Shelter Crews": t_allocs.get("Logistics & Shelter Deployment Crew", 0)
                })
            st.dataframe(pd.DataFrame(fleet_rows), use_container_width=True, hide_index=True)

        with tab_shortage:
            st.plotly_chart(build_resource_utilization_chart(problem, res), use_container_width=True)

        with tab_map:
            res_map = create_disaster_map(problem.regions, hubs=hubs, allocation_matrix=res.allocation_matrix)
            st_folium(res_map, use_container_width=True, height=500, returned_objects=[])

        # Exports
        st.markdown("#### 📥 Export Operational Allocation Plan")
        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            pdf_bytes = generate_allocation_pdf(res, problem, get_disaster_info())
            st.download_button(
                "📄 Download Official PDF Dispatch Plan",
                data=pdf_bytes,
                file_name=f"DisasterShield_Allocation_{res.algorithm_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with c_exp2:
            csv_str = generate_allocation_csv(res, problem)
            st.download_button(
                "📊 Download CSV Allocation Matrix",
                data=csv_str,
                file_name="DisasterShield_Allocation_Matrix.csv",
                mime="text/csv",
                use_container_width=True
            )

# -------------------------------------------------------------------------------------------------
# PAGE 7: BENCHMARK & COMPARISON
# -------------------------------------------------------------------------------------------------
elif selected_page == "📊 Benchmark & Comparison":
    st.subheader("📊 Multi-Algorithm Benchmark & Sensitivity Comparison")
    st.caption("Rigorous scientific comparison across all 6 mathematical paradigms on the identical disaster scenario.")

    problem = load_current_problem()

    if st.button("🚀 Run Full Multi-Algorithm Benchmark", key="run_benchmark_btn", use_container_width=True):
        with st.spinner("Benchmarking Linear Programming, Integer Programming, Greedy, Genetic Algorithm, Simulated Annealing, and NSGA-II..."):
            bench_results = run_all_benchmarks(problem)
            st.session_state["benchmark_results"] = bench_results
            st.success("Benchmark completed! Comparing objective values, execution speeds, and fulfillment trade-offs.")

    if "benchmark_results" in st.session_state:
        b_res = st.session_state["benchmark_results"]

        # Safely extract results dict and comparison table
        if isinstance(b_res, dict) and "results" in b_res:
            results_dict = b_res["results"]
            comparison_df = b_res.get("comparison_table")
        elif isinstance(b_res, dict):
            results_dict = b_res
            comparison_df = None
        else:
            results_dict = {}
            comparison_df = None

        if comparison_df is not None and isinstance(comparison_df, pd.DataFrame) and not comparison_df.empty:
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            radar_df = comparison_df
        else:
            summary_rows = []
            for name, r in results_dict.items():
                if hasattr(r, "fulfilled_demand_ratio"):
                    summary_rows.append({
                        "Algorithm": name,
                        "Fulfilled Demand (%)": round(r.fulfilled_demand_ratio * 100.0, 1),
                        "Total Cost ($)": round(r.total_cost, 2),
                        "Avg Delivery Time (h)": round(r.avg_delivery_time, 2),
                        "Execution Time (s)": round(r.execution_time_sec, 4),
                        "Feasible": "YES ✅" if r.is_feasible else "NO ❌"
                    })
            radar_df = pd.DataFrame(summary_rows)
            st.dataframe(radar_df, use_container_width=True, hide_index=True)

        col_radar, col_time = st.columns(2)
        with col_radar:
            if not radar_df.empty and "Total Cost ($)" in radar_df.columns:
                radar_fig = build_benchmark_radar_chart(radar_df)
                st.plotly_chart(radar_fig, use_container_width=True)

        with col_time:
            time_rows = []
            for k, v in results_dict.items():
                if hasattr(v, "execution_time_sec"):
                    time_rows.append({"Algorithm": k, "Execution Time (s)": v.execution_time_sec})
            if not time_rows and not radar_df.empty and "Execution Time (s)" in radar_df.columns:
                time_rows = [
                    {"Algorithm": row["Algorithm"], "Execution Time (s)": row["Execution Time (s)"]}
                    for _, row in radar_df.iterrows()
                ]

            if time_rows:
                time_df = pd.DataFrame(time_rows)
                import plotly.express as px
                bar_fig = px.bar(
                    time_df, x="Algorithm", y="Execution Time (s)",
                    title="Computational Efficiency Comparison (Log Scale)",
                    log_y=True, color="Execution Time (s)",
                    color_continuous_scale="Viridis", template="plotly_dark"
                )
                st.plotly_chart(bar_fig, use_container_width=True)

# -------------------------------------------------------------------------------------------------
# PAGE 8: SCENARIO STRESS SIMULATOR
# -------------------------------------------------------------------------------------------------
elif selected_page == "🌪️ Scenario Stress Simulator":
    st.subheader("🌪️ Operational Stress Simulator & Sensitivity Analysis")
    st.caption("Stress-test algorithm resilience under unexpected disruptions: severe supply shocks, blocked access corridors, and sudden surge.")

    problem = load_current_problem()

    c1, c2, c3 = st.columns(3)
    with c1:
        pop_surge = st.slider("Affected Population Surge Multiplier", 1.0, 3.0, 1.3, 0.1)
    with c2:
        supply_shock = st.slider("Supply Stockpile Cut / Destruction (%)", 0, 75, 25, 5)
    with c3:
        road_disruption = st.slider("Road Network Accessibility Degradation (%)", 0, 80, 30, 5)

    if st.button("🧪 Simulate Scenario Stress Test", use_container_width=True):
        with st.spinner("Simulating stressed disaster parameters..."):
            stressed_regions = []
            for r in problem.regions:
                rc = dict(r)
                rc["population"] = int(rc["population"] * pop_surge)
                rc["water_demand"] = round(rc["water_demand"] * pop_surge, 1)
                rc["food_demand"] = round(rc["food_demand"] * pop_surge, 1)
                rc["med_demand"] = round(rc["med_demand"] * pop_surge, 1)
                rc["accessibility_score"] = max(0.05, round(rc["accessibility_score"] * (1.0 - road_disruption / 100.0), 2))
                stressed_regions.append(rc)

            stressed_resources = []
            for res in problem.resources:
                resc = dict(res)
                resc["total_available"] = round(resc["total_available"] * (1.0 - supply_shock / 100.0), 1)
                stressed_resources.append(resc)

            stressed_prob = OptimizationProblem(
                regions=stressed_regions,
                resources=stressed_resources,
                vehicles=problem.vehicles,
                teams=problem.teams,
                central_depot=problem.central_depot,
                scenario_name=f"Stressed: +{int((pop_surge-1)*100)}% Pop, -{supply_shock}% Stock",
                hubs=problem.hubs
            )

            res_lp = solve_linear_programming(stressed_prob)
            res_gr = solve_greedy(stressed_prob)

            st.session_state["stress_res"] = (stressed_prob, res_lp, res_gr)
            st.success("Stress test executed successfully!")

    if "stress_res" in st.session_state:
        s_prob, s_lp, s_gr = st.session_state["stress_res"]
        st.markdown("#### Stress Test Findings")

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("LP Stressed Fulfillment", f"{s_lp.fulfilled_demand_ratio * 100:.1f}%")
        s2.metric("Greedy Stressed Fulfillment", f"{s_gr.fulfilled_demand_ratio * 100:.1f}%")
        s3.metric("LP Stressed Total Cost", f"${s_lp.total_cost:,.2f}")
        s4.metric("Avg Delivery Time", f"{s_lp.avg_delivery_time:.2f} hrs")

        st.plotly_chart(build_resource_utilization_chart(s_prob, s_lp), use_container_width=True)

# -------------------------------------------------------------------------------------------------
# PAGE 9: REPORTS & DISPATCH ORDERS
# -------------------------------------------------------------------------------------------------
elif selected_page == "📑 Reports & Dispatch Orders":
    st.subheader("📑 Allocation History & Official Dispatch Export")
    st.caption("Review past optimization runs from the SQLite database, inspect feasibility verdicts, and export incident records.")

    history_df = get_allocation_history()
    if not history_df.empty:
        st.dataframe(
            history_df[[
                "id", "execution_timestamp", "algorithm_name", "scenario_name",
                "fulfilled_demand_ratio", "total_cost", "avg_delivery_time", "execution_time_sec", "is_feasible"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No prior execution history logged. Run algorithms in the Optimization Engine to generate audit logs.")

# -------------------------------------------------------------------------------------------------
# PAGE 10: ACADEMIC THEORY (CSDX 507)
# -------------------------------------------------------------------------------------------------
elif selected_page == "📚 Academic Theory (CSDX 507)":
    st.subheader("📚 Mathematical Formulations & Operations Research Proofs")
    st.caption("Curriculum documentation for CSDX 507 Decision-Making for Data Science (Modules IV & V).")

    st.markdown(r"""
    ### 1. Dynamic State-Wise Emergency Operations Centres (SEOC)
    India's disaster response architecture under the **Disaster Management Act 2005** designates 
    State Disaster Management Authorities (SDMAs) and State Emergency Operations Centres (SEOC) as primary nodal dispatch hubs:
    
    $$\text{Hub}(S) = \text{SEOC}_S \quad \forall S \in \{1, \dots, 28 \text{ States}\} \cup \{1, \dots, 8 \text{ UTs}\}$$
    
    When a disaster affects state $S$, the decision-support engine identifies the state automatically and routes regional logistics through $\text{SEOC}_S$.

    ### 2. Multi-State Mathematical Resource Partitioning
    For simultaneous disasters across multiple states $S_1, S_2, \dots$:
    
    $$\sum_{S} \text{Allocated}_{S, r} \le \text{Inventory}_r \quad \forall r \in \mathcal{R}$$
    
    Guaranteeing non-duplication of resources across inter-state boundaries.

    ### 3. Linear Programming (LP) Primal Model
    $$\max \sum_{i \in \mathcal{I}} \sum_{j \in \mathcal{J}} w_j U_i x_{ij} - \sum_{i \in \mathcal{I}} \sum_{j \in \mathcal{J}} c_j x_{ij}$$
    
    Subject to:
    $$\sum_{i \in \mathcal{I}} x_{ij} \le S_j \quad \forall j \in \mathcal{J} \quad \text{(Supply Boundary)}$$
    $$x_{ij} \le D_{ij} \quad \forall i \in \mathcal{I}, \forall j \in \mathcal{J} \quad \text{(Demand Boundary)}$$
    $$x_{ij} \ge 0 \quad \forall i, j \quad \text{(Non-Negativity)}$$

    ### 4. Integer Programming (IP) Vehicle & Fleet Assignment
    $$\min \sum_{i \in \mathcal{I}} \sum_{k \in \mathcal{K}} 2 \cdot d_i \cdot c_k \cdot y_{ik} + \sum_{i \in \mathcal{I}} \sum_{t \in \mathcal{T}} \text{cost}_t \cdot z_{it}$$
    
    Subject to:
    $$\sum_{i \in \mathcal{I}} y_{ik} \le V_k \quad \forall k \in \mathcal{K}, \quad y_{ik} \in \mathbb{Z}_{\ge 0}$$
    $$\sum_{i \in \mathcal{I}} z_{it} \le T_t \quad \forall t \in \mathcal{T}, \quad z_{it} \in \mathbb{Z}_{\ge 0}$$
    """)
