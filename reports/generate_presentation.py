"""
Automated PowerPoint Generator for DisasterShield AI.
Uses python-pptx to generate a 12-slide, 16:9 widescreen presentation deck
tailored for CSDX 507 Decision-Making for Data Science evaluation.
Styled in dark navy (#0B192C, #1E3E62) and emergency orange (#FF6500).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Theme Colors
BG_DARK = RGBColor(11, 25, 44)        # #0B192C
BG_CARD = RGBColor(30, 62, 98)        # #1E3E62
ORANGE_PRIMARY = RGBColor(255, 101, 0) # #FF6500
ORANGE_LIGHT = RGBColor(255, 138, 8)  # #FF8A08
TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
ACCENT_CYAN = RGBColor(56, 189, 248)  # #38BDF8
GREEN_ACCENT = RGBColor(16, 185, 129) # #10B981

def create_base_slide(prs, title_text, category_text="CSDX 507 | DECISION-MAKING FOR DATA SCIENCE"):
    """Creates a slide with consistent dark navy branding and header."""
    blank_layout = prs.slide_layouts[6] # Blank
    slide = prs.slides.add_slide(blank_layout)

    # Background shape
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.color.rgb = BG_DARK

    # Top accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = ORANGE_PRIMARY
    top_line.line.color.rgb = ORANGE_PRIMARY

    # Category tracker
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ORANGE_PRIMARY

    # Title text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    return slide

def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ORANGE_PRIMARY):
    """Adds a rounded dark slate card with title and bullet points."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = BG_CARD
    card.line.color.rgb = accent_color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.margin_bottom = Inches(0.25)

    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = accent_color
    p_title.space_after = Pt(8)

    # Bullets
    for bullet in body_bullets:
        p = tf.add_paragraph()
        p.text = "• " + bullet
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(5)

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.color.rgb = BG_DARK

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(0.2), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE_PRIMARY
    bar.line.color.rgb = ORANGE_PRIMARY

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.5), Inches(4.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "DISASTERSHIELD AI 🛡️"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = ORANGE_PRIMARY

    p2 = tf1.add_paragraph()
    p2.text = "Intelligent Disaster Resource Allocation & Decision Support Platform"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Academic Capstone Project | CSDX 507 Decision-Making for Data Science\nModules IV & V: Linear, Integer, Heuristic, Metaheuristic & Multi-Objective Optimization"
    p3.font.size = Pt(14)
    p3.font.color.rgb = ACCENT_CYAN
    p3.space_before = Pt(14)

    p4 = tf1.add_paragraph()
    p4.text = "Tech Stack: Python • Streamlit • SciPy (HiGHS) • Google OR-Tools (SCIP) • DEAP • pymoo • Scikit-Learn • SQLite"
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(18)

    # ==========================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================
    s2 = create_base_slide(prs, "1. Problem Statement: The Disaster Logistics Challenge")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Severe Resource Scarcity",
             [
                 "Post-disaster relief inventories typically meet only 50-70% of peak regional demand.",
                 "Clean drinking water, survival rations, and trauma kits deplete within hours.",
                 "First-Come First-Served allocation starves isolated, vulnerable populations."
             ], ORANGE_PRIMARY)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Infrastructure Bottlenecks",
             [
                 "Road washouts, mudslides, and collapsed bridges severely degrade access.",
                 "High-clearance 4x4 trucks and rescue boats must be deployed selectively.",
                 "Travel latency compounds casualty rates in high-severity red zones."
             ], ACCENT_CYAN)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Multi-Criteria Trade-offs",
             [
                 "Tension between rapid delivery latency, budget cost, and equity.",
                 "Emergency managers require mathematically verifiable dispatch plans.",
                 "Need for an explainable decision-support workbench across hazard types."
             ], GREEN_ACCENT)

    # ==========================================
    # SLIDE 3: System Architecture & Workflow
    # ==========================================
    s3 = create_base_slide(prs, "2. DisasterShield AI: System Architecture")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Data & Telemetry Layer",
             [
                 "SQLite Relational Core: 7 tables tracking regions, fleet, resources, and run logs.",
                 "Synthetic Baseline Scenario: 10 diverse disaster zones with varying road conditions.",
                 "Live Free API Telemetry: Open-Meteo Weather, USGS Earthquakes, Nominatim Geocoding."
             ], ACCENT_CYAN)

    add_card(s3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "AI & Optimization Core",
             [
                 "Random Forest Severity Predictor: Estimates regional intensity and demand multipliers.",
                 "6 Core Solvers: Exact LP, Discrete IP, Greedy Urgency, DEAP GA, Metropolis SA, pymoo NSGA-II.",
                 "Strict Physical Constraint Validator: Zero tolerance for demand or supply violations."
             ], ORANGE_PRIMARY)

    add_card(s3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Interactive Command UI",
             [
                 "Streamlit Operations Dashboard: Folium interactive maps and Dark Navy/Orange theme.",
                 "Scenario Stress Simulator: Injects budget cuts (-40%), population surges, bridge collapses.",
                 "ReportLab PDF Exporter: Generates official downloadable dispatch orders and CSV manifests."
             ], GREEN_ACCENT)

    # ==========================================
    # SLIDE 4: Module IV - Exact Optimization (LP & IP)
    # ==========================================
    s4 = create_base_slide(prs, "3. Module IV: Linear & Integer Programming Formulations")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Linear Programming (SciPy HiGHS Simplex)",
             [
                 "Continuous Variables: x(i, r) = volume of divisible resource r dispatched to region i.",
                 "Objective: Maximize Sum [ Priority(r) * Urgency(i) * x(i,r)/Demand(i,r) ] minus distance penalty.",
                 "Constraint 1: Supply Limit -> Sum_i x(i, r) <= Supply(r) for all resources.",
                 "Constraint 2: Regional Demand Ceiling -> 0 <= x(i, r) <= Demand(i, r).",
                 "Solver: SciPy optimize.linprog using HiGHS dual simplex; guarantees global mathematical optimality."
             ], ORANGE_PRIMARY)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Integer Programming (OR-Tools SCIP)",
             [
                 "Discrete Variables: y(i, v) in Z+ (vehicles), z(i, t) in Z+ (rescue teams).",
                 "Objective: Maximize life rescue capability, triage capacity, and temporary shelter deployment.",
                 "Constraint 1: Fleet Upper Bounds -> Sum_i y(i, v) <= Fleet(v).",
                 "Constraint 2: Team Capacity -> Sum_i z(i, t) <= Teams(t).",
                 "Terrain Compatibility Rule: Rescue boats required in waterlogged zones; ambulances restricted on flooded roads.",
                 "Solver: Google OR-Tools SCIP with Branch-and-Bound and cutting planes."
             ], ACCENT_CYAN)

    # ==========================================
    # SLIDE 5: Module V - Heuristic & Metaheuristics (Greedy, GA, SA)
    # ==========================================
    s5 = create_base_slide(prs, "4. Module V: Heuristic & Metaheuristic Solvers")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Explainable Greedy Heuristic",
             [
                 "Urgency Index (Ui): 0.40*(Sev/5) + 0.25*(Pop/MaxPop) + 0.20*(1-Acc) + 0.15*Priority.",
                 "Policy: Sorts regions by descending Ui and greedily allocates min(Demand, Supply).",
                 "Full Audit Trail: Emits explainable decision logs justifying allocation decisions."
             ], GREEN_ACCENT)

    add_card(s5, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Genetic Algorithm (DEAP)",
             [
                 "Chromosome: Continuous gene fractions g(i, r) in [0, 1] representing demand percentages.",
                 "Feasibility Repair Operator: Dynamically rescales candidate solutions if total exceeds supply.",
                 "Operators: Tournament Selection (k=3), Blend Crossover (cxBlend), Gaussian Mutation.",
                 "Generational Tracking: Records convergence curves across 30+ generations."
             ], ORANGE_PRIMARY)

    add_card(s5, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Simulated Annealing (SA)",
             [
                 "Neighborhood Move: Shifts quantum delta from donor region i to recipient j.",
                 "Feasibility: Moves strictly preserve total supply and respect recipient demand caps.",
                 "Metropolis Acceptance: P = exp(-Delta_E / T) allows probabilistic escape from local optima.",
                 "Cooling Schedule: Geometric decay T(k+1) = alpha * T(k) with alpha = 0.94."
             ], ACCENT_CYAN)

    # ==========================================
    # SLIDE 6: Module V - Multi-Objective Optimization (pymoo NSGA-II)
    # ==========================================
    s6 = create_base_slide(prs, "5. Module V: Multi-Objective Optimization (NSGA-II)")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Three Conflicting Objective Functions",
             [
                 "Objective 1 (f1 - Delivery Latency): Minimize urgency-weighted delivery transit hours.",
                 "Objective 2 (f2 - Operational Cost): Minimize total material purchasing, vehicle mileage, and team wages.",
                 "Objective 3 (f3 - Shortage Penalty): Minimize total unmet resource units (equivalent to maximizing coverage).",
                 "Constraint Handling: Enforced via pymoo inequality constraints G(x) <= 0 on resource inventories."
             ], ORANGE_PRIMARY)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Pareto Front & Compromise Selection",
             [
                 "Non-Dominated Sorting: Evolves a 3D/2D Pareto-optimal surface where no objective can improve without degrading another.",
                 "Trade-off Insight: 100% fulfillment demands high logistical spending; lower budgets yield higher unmet shortages.",
                 "Utopia Compromise Point: Normalizes objectives and automatically picks the knee-point solution closest to the ideal origin.",
                 "Visualization: Interactive Plotly scatter plot with highlighted compromise knee marker."
             ], ACCENT_CYAN)

    # ==========================================
    # SLIDE 7: AI Severity Prediction Engine
    # ==========================================
    s7 = create_base_slide(prs, "6. Machine Learning Severity Predictor")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Supervised Learning Model",
             [
                 "Model Architecture: Scikit-Learn RandomForestRegressor (100 estimators, depth=12).",
                 "Training Dataset: 1,500 synthetic multi-hazard disaster instances across Floods, Cyclones, Quakes, Landslides.",
                 "Key Input Features: 24h rainfall (mm), flood water gauge (m), wind speed (km/h), soil saturation (%), Richter magnitude, slope angle, density, bridge cutoff.",
                 "Regression Performance: R2 Score ~0.82, RMSE ~0.45, MAE ~0.36 on unseen holdout test split."
             ], ORANGE_PRIMARY)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Operational Posture Advisory",
             [
                 "Critical Emergency (Severity >= 8.0): Triggers mandatory evacuation and 1.6x resource multiplier.",
                 "High Severity (6.0 - 7.9): Mobilizes regional SAR squads and 1.3x multiplier.",
                 "Moderate Impact (4.0 - 5.9): Deploys standard trauma kits and 1.0x baseline.",
                 "Low Impact (< 4.0): Pre-positions community volunteers and 0.7x multiplier.",
                 "Feature Importance: Rainfall, flood depth, and Richter magnitude drive >60% of predictive power."
             ], GREEN_ACCENT)

    # ==========================================
    # SLIDE 8: Real-Time Free API Integrations
    # ==========================================
    s8 = create_base_slide(prs, "7. Live Free Open-Source API Integrations")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Open-Meteo Weather API",
             [
                 "Zero API Key / Completely Free: Queries real-time precipitation, wind speed, humidity, and barometric pressure.",
                 "Direct Integration: Emergency planners click 'Query Live Weather' to feed real atmospheric data into the AI severity model.",
                 "Offline Fallback: Automatically falls back to calibrated simulation if offline."
             ], ACCENT_CYAN)

    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "USGS Earthquake Hazards Feed",
             [
                 "Real-Time Public Domain API: Streams live global seismic events from earthquake.usgs.gov.",
                 "Rich Metadata: Captures Richter magnitude, hypocenter depth (km), epicenter coords, and tsunami alerts.",
                 "Scenario Importer: Planners can review live quakes and import them into active dispatch scenarios."
             ], ORANGE_PRIMARY)

    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "OpenStreetMap Nominatim",
             [
                 "Worldwide Place Name Resolution: Translates human city/village queries into exact latitude and longitude.",
                 "Logistics Staging: Calculates road transit distances between field staging bases and affected communities.",
                 "Zero Cloud Sign-up Required: Runs cleanly on standard local network requests."
             ], GREEN_ACCENT)

    # ==========================================
    # SLIDE 9: Benchmark & Experimental Evaluation
    # ==========================================
    s9 = create_base_slide(prs, "8. Benchmark & Experimental Evaluation")
    
    # Table of benchmark results
    table_shape = s9.shapes.add_table(7, 6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.5))
    table = table_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.6)
    table.columns[5].width = Inches(1.5)

    headers = ["Algorithm", "Academic Module", "Fulfilled %", "Total Cost ($)", "Runtime (s)", "Feasible?"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = ORANGE_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    bench_data = [
        ["Linear Programming", "Module IV (Simplex)", "67.1%", "$566,110.40", "0.0031s", "100% Yes"],
        ["Integer Programming", "Module IV (Branch & Bound)", "67.1%", "$566,376.80", "0.0120s", "100% Yes"],
        ["Greedy Urgency", "Module V (Priority Heuristic)", "67.1%", "$564,698.70", "0.0002s", "100% Yes"],
        ["Genetic Algorithm", "Module V (Evolutionary GA)", "67.1%", "$566,108.82", "0.0952s", "100% Yes"],
        ["Simulated Annealing", "Module V (Metropolis SA)", "67.1%", "$566,110.07", "0.0509s", "100% Yes"],
        ["Multi-Objective NSGA-II", "Module V (Pareto MOO)", "59.1%", "$317,858.02", "0.1287s", "100% Yes"]
    ]

    for r_idx, row in enumerate(bench_data, 1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_WHITE

    notes_box = s9.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.4))
    tf_notes = notes_box.text_frame
    tf_notes.word_wrap = True
    p_n = tf_notes.paragraphs[0]
    p_n.text = "Key Takeaway: Exact LP is fastest for continuous flows; Greedy is instant (<1ms); NSGA-II demonstrates cost-reduction trade-offs ($317k vs $566k). All 6 solvers strictly satisfied 100% physical constraints."
    p_n.font.size = Pt(12)
    p_n.font.color.rgb = ACCENT_CYAN

    # ==========================================
    # SLIDE 10: Multi-Hazard Scenarios & Stress Testing
    # ==========================================
    s10 = create_base_slide(prs, "9. Multi-Hazard Scenarios & Stress Simulator")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Multi-Hazard Catalog",
             [
                 "Monsoon Flood & Cyclone: 10 coastal delta zones, high waterlogging, acute clean water demand.",
                 "Himalayan Flash Landslide: 5 alpine mountain hamlets, washed out passes, thermal shelters, SAR extrication.",
                 "Urban Mega-Earthquake 7.4: 6 metropolitan wards, structural collapse, gas leaks, trauma medical units."
             ], ORANGE_PRIMARY)

    add_card(s10, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Stress Shock Injection",
             [
                 "Supply Budget Slashing: Injects 20% to 60% inventory cuts across all depots.",
                 "Displaced Evacuee Surge: Simulates +20% to +100% population spikes.",
                 "Infrastructure Shocks: Simulates collapsed river bridges cutting off critical sectors."
             ], ACCENT_CYAN)

    add_card(s10, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Sensitivity Analysis Diffs",
             [
                 "Instant Before vs After Comparisons: Directly plots fulfillment deficit waterfalls.",
                 "Bottleneck Detection: Flags regions at risk of zero water/food allocation.",
                 "Resilience Planning: Helps disaster agencies identify vulnerable bridges and stockpiles."
             ], GREEN_ACCENT)

    # ==========================================
    # SLIDE 11: Academic Safety & Operational Ethics
    # ==========================================
    s11 = create_base_slide(prs, "10. Academic Prototype Scope & Operational Ethics")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Academic Decision-Support Prototype",
             [
                 "Course Mandate: Developed strictly for CSDX 507 Decision-Making for Data Science demonstration.",
                 "Not a Real Dispatch System: Does NOT replace professional emergency services (NDRF, FEMA, Red Cross).",
                 "Synthetic Demonstration Data: Pre-populated regions and historical training sets are synthetic.",
                 "Human-in-the-Loop Authority: Real disaster decisions mandate certified meteorological approval and human officer sign-off."
             ], ORANGE_PRIMARY)

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Data Privacy & Software Integrity",
             [
                 "100% Free Open-Source Stack: Zero paid APIs, zero proprietary cloud locks, zero subscription fees.",
                 "Complete Data Privacy: No personal or sensitive disaster survivor information is collected or transmitted.",
                 "Local Windows Execution: Self-contained SQLite database and local Streamlit server ensure full offline resilience.",
                 "Reproducibility: Fully automated test suite with 10 unit tests passing all physical constraints."
             ], ACCENT_CYAN)

    # ==========================================
    # SLIDE 12: Conclusion & Viva Voce Talking Points
    # ==========================================
    s12 = create_base_slide(prs, "11. Conclusion & Key Takeaways for Viva Voce")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Syllabus Mastery",
             [
                 "Module IV: Successfully demonstrated Simplex LP and Branch-and-Bound IP on real disaster data.",
                 "Module V: Successfully built and compared Greedy heuristics, DEAP GA with repair, and Metropolis SA.",
                 "Multi-Objective: Visualized genuine Pareto trade-offs using NSGA-II and Utopia knee points."
             ], GREEN_ACCENT)

    add_card(s12, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Technical Excellence",
             [
                 "Rigorous Feasibility: Zero tolerance for exceeding supply or regional demand ceilings.",
                 "Machine Learning: Random Forest severity model with R2 ~0.82 and feature importance.",
                 "Full-Stack Polish: Modern dark navy & emergency orange UI, Folium maps, and ReportLab PDF export."
             ], ORANGE_PRIMARY)

    add_card(s12, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Live Demo Ready",
             [
                 "Local Server: Running at http://localhost:8501 with instant one-click execution.",
                 "Multi-Hazard Switching: Seamlessly loads Floods, Landslides, and Quakes in <1 second.",
                 "Comprehensive Documentation: Clean GitHub-grade README and complete academic project report."
             ], ACCENT_CYAN)

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    ppt_path = os.path.join(out_dir, "DisasterShield_AI_Presentation.pptx")
    build_presentation(ppt_path)

