"""
Interactive Plotly Chart Builder for DisasterShield AI.
Includes Pareto fronts, convergence plots, stacked fulfillment bars,
shortage waterfalls, algorithm comparison radars, and feature importances.
Styled with a sleek dark navy & emergency orange aesthetic.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any

# Dark Navy & Emergency Orange Theme Palette
THEME_BG = "#0B192C"
PAPER_BG = "#1E3E62"
TEXT_COLOR = "#F8FAFC"
GRID_COLOR = "#334155"
ORANGE_PRIMARY = "#FF6500"
ORANGE_SECONDARY = "#FF8A08"
CYAN_ACCENT = "#38BDF8"
GREEN_SUCCESS = "#10B981"
RED_CRITICAL = "#EF4444"

def apply_chart_theme(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    """Applies unified dark command-center aesthetic to a Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter, sans-serif", size=16, color=TEXT_COLOR)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(family="Inter, sans-serif", color=TEXT_COLOR),
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="#475569",
            borderwidth=1,
            font=dict(size=11, color=TEXT_COLOR)
        )
    )
    return fig

def build_allocation_stacked_bar(
    allocation_matrix: Dict[str, Dict[str, float]],
    problem: Any,
    resource_name: str = "Clean Drinking Water"
) -> go.Figure:
    """Stacked bar chart comparing Allocated vs Shortage per region for a resource."""
    demand_mapping = {
        "Clean Drinking Water": "water_demand",
        "Ready-to-Eat Food Packets": "food_demand",
        "Emergency Medical Kits": "med_demand",
        "Temporary Emergency Shelters": "shelter_demand"
    }
    key = demand_mapping.get(resource_name, "water_demand")

    regions = [r["name"] for r in problem.regions]
    allocated = []
    shortage = []

    for reg in problem.regions:
        r_name = reg["name"]
        dem = float(reg.get(key, 0.0))
        alloc = allocation_matrix.get(r_name, {}).get(resource_name, 0.0)
        short = max(0.0, dem - alloc)
        allocated.append(alloc)
        shortage.append(short)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=regions,
        y=allocated,
        name="Allocated Units",
        marker_color=CYAN_ACCENT,
        opacity=0.9
    ))
    fig.add_trace(go.Bar(
        x=regions,
        y=shortage,
        name="Unmet Shortage",
        marker_color=RED_CRITICAL,
        opacity=0.75
    ))

    fig.update_layout(barmode="stack")
    return apply_chart_theme(fig, f"Demand Fulfillment & Shortage: {resource_name}", height=380)

def build_resource_utilization_chart(problem: Any, result: Any) -> go.Figure:
    """Grouped bar chart showing Total Available, Allocated, and Shortage across resources."""
    supplies = problem.get_total_supply_by_resource()
    demands = problem.get_total_demand_by_resource()

    res_names = list(supplies.keys())
    avail_vals = [supplies[r] for r in res_names]
    dem_vals = [demands.get(r, 0.0) for r in res_names]
    
    alloc_vals = []
    for r in res_names:
        tot_alloc = sum(result.allocation_matrix.get(reg["name"], {}).get(r, 0.0) for reg in problem.regions)
        alloc_vals.append(tot_alloc)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Total Demand", x=res_names, y=dem_vals, marker_color="#94A3B8"))
    fig.add_trace(go.Bar(name="Available Inventory", x=res_names, y=avail_vals, marker_color=ORANGE_SECONDARY))
    fig.add_trace(go.Bar(name="Optimally Allocated", x=res_names, y=alloc_vals, marker_color=GREEN_SUCCESS))

    fig.update_layout(barmode="group")
    return apply_chart_theme(fig, "Resource Supply vs Demand vs Optimized Allocation", height=380)

def build_pareto_front_plot(pareto_solutions: List[Dict[str, Any]]) -> go.Figure:
    """Plots the Multi-Objective NSGA-II Pareto trade-off curve."""
    df = pd.DataFrame(pareto_solutions)
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="total_cost_usd",
        y="delivery_latency_hrs",
        size="unmet_shortage_units",
        color="unmet_shortage_units",
        hover_data=["solution_id", "delivery_latency_hrs", "total_cost_usd", "unmet_shortage_units"],
        color_continuous_scale="Turbo",
        labels={
            "total_cost_usd": "Operational Cost ($)",
            "delivery_latency_hrs": "Delivery Latency (Weighted Hours)",
            "unmet_shortage_units": "Resource Shortage (Units)"
        }
    )

    # Highlight compromise knee point
    knee = df[df["is_compromise_knee_point"] == True]
    if not knee.empty:
        fig.add_trace(go.Scatter(
            x=knee["total_cost_usd"],
            y=knee["delivery_latency_hrs"],
            mode="markers+text",
            text=["★ BEST COMPROMISE (KNEE)"],
            textposition="top center",
            marker=dict(size=18, color="#F59E0B", symbol="star", line=dict(color="#FFFFFF", width=2)),
            name="Compromise Knee Point"
        ))

    return apply_chart_theme(fig, "NSGA-II Pareto Front Trade-off (Cost vs Latency vs Shortage)", height=450)

def build_ga_convergence_plot(convergence_history: List[Dict[str, Any]]) -> go.Figure:
    """Plots Genetic Algorithm generational fitness progression."""
    df = pd.DataFrame(convergence_history)
    fig = go.Figure()

    if not df.empty:
        fig.add_trace(go.Scatter(
            x=df["generation"], y=df["best_fitness"],
            name="Best Fitness", mode="lines+markers",
            line=dict(color=ORANGE_PRIMARY, width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df["generation"], y=df["avg_fitness"],
            name="Population Average", mode="lines",
            line=dict(color=CYAN_ACCENT, width=2, dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=df["generation"], y=df["min_fitness"],
            name="Worst Fitness", mode="lines",
            line=dict(color="#64748B", width=1)
        ))

    return apply_chart_theme(fig, "Genetic Algorithm Convergence Curve Across Generations", height=380)

def build_sa_cooling_plot(cooling_history: List[Dict[str, Any]]) -> go.Figure:
    """Plots Simulated Annealing energy progression and cooling schedule."""
    df = pd.DataFrame(cooling_history)
    fig = go.Figure()

    if not df.empty:
        fig.add_trace(go.Scatter(
            x=df["iteration"], y=df["best_energy"],
            name="Best Energy (Minimized)", mode="lines",
            line=dict(color=GREEN_SUCCESS, width=2.5)
        ))
        fig.add_trace(go.Scatter(
            x=df["iteration"], y=df["energy"],
            name="Current State Energy", mode="lines",
            line=dict(color="#94A3B8", width=1, dash="dot"),
            opacity=0.6
        ))

    return apply_chart_theme(fig, "Simulated Annealing Metropolis Energy Landscape", height=380)

def build_benchmark_radar_chart(comparison_df: pd.DataFrame) -> go.Figure:
    """Radar chart comparing algorithms across standardized performance dimensions."""
    categories = [
        "Demand Fulfillment",
        "Cost Efficiency",
        "Execution Speed",
        "Delivery Quickness"
    ]

    fig = go.Figure()

    # Normalize metrics to 0-100 scale for fair radar visualization
    max_cost = comparison_df["Total Cost ($)"].max() if comparison_df["Total Cost ($)"].max() > 0 else 1.0
    max_time = comparison_df["Avg Delivery Time (h)"].max() if comparison_df["Avg Delivery Time (h)"].max() > 0 else 1.0
    max_exec = comparison_df["Execution Time (s)"].max() if comparison_df["Execution Time (s)"].max() > 0 else 1.0

    colors = [ORANGE_PRIMARY, CYAN_ACCENT, GREEN_SUCCESS, "#F59E0B", "#EC4899", "#A855F7"]

    for idx, row in comparison_df.iterrows():
        algo = row["Algorithm"]
        f_score = float(row["Fulfilled Demand (%)"])
        # Cost efficiency: lower cost -> higher score
        cost_score = (1.0 - (float(row["Total Cost ($)"]) / max_cost)) * 100.0 if max_cost > 0 else 50.0
        # Speed: lower execution time -> higher score
        exec_score = (1.0 - (float(row["Execution Time (s)"]) / max_exec)) * 100.0 if max_exec > 0 else 50.0
        # Delivery: lower delivery time -> higher score
        deliv_score = (1.0 - (float(row["Avg Delivery Time (h)"]) / max_time)) * 100.0 if max_time > 0 else 50.0

        r_values = [f_score, max(10, cost_score), max(10, exec_score), max(10, deliv_score)]
        r_values.append(r_values[0])  # close radar polygon

        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=categories + [categories[0]],
            name=algo,
            line=dict(color=colors[idx % len(colors)], width=2),
            fill="toself",
            opacity=0.25
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=GRID_COLOR, color=TEXT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
            bgcolor="rgba(15, 23, 42, 0.6)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_COLOR),
        height=480,
        margin=dict(l=40, r=40, t=50, b=40),
        title=dict(text="Multi-Dimensional Algorithm Performance Radar", font=dict(size=16, color=TEXT_COLOR))
    )
    return fig

def build_feature_importance_chart(feature_importances: List[Tuple[str, float]]) -> go.Figure:
    """Horizontal bar chart for AI Severity Model feature importances."""
    labels = [item[0].replace("_", " ").title() for item in feature_importances[:10]]
    values = [item[1] for item in feature_importances[:10]]

    # Invert so highest is at the top
    labels.reverse()
    values.reverse()

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(
            color=values,
            colorscale="Viridis",
            line=dict(color="#38BDF8", width=1)
        )
    ))

    return apply_chart_theme(fig, "Random Forest Feature Importance Weights", height=380)
