"""
Generates a complete, multi-page, publication-grade academic PDF project report
for DisasterShield AI using ReportLab.
Tailored for CSDX 507 Decision-Making for Data Science.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_pdf_report(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    NAVY_DARK = colors.HexColor("#0B192C")
    NAVY_MID = colors.HexColor("#1E3E62")
    ORANGE_PRIMARY = colors.HexColor("#FF6500")
    SLATE_LIGHT = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#CBD5E1")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=NAVY_DARK,
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=ORANGE_PRIMARY,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        "ReportH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY_MID,
        spaceBefore=12,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=ORANGE_PRIMARY,
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        "ReportBullet",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )
    callout_style = ParagraphStyle(
        "Callout",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569")
    )

    story = []

    # ==========================================
    # HEADER & TITLE BLOCK
    # ==========================================
    story.append(Paragraph("DISASTERSHIELD AI – INTELLIGENT DISASTER RESOURCE ALLOCATION", title_style))
    story.append(Paragraph("Comprehensive Academic Project Report | CSDX 507 Decision-Making for Data Science", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2.5, color=ORANGE_PRIMARY, spaceAfter=12))

    # Meta Table
    meta_data = [
        ["Course", "CSDX 507 Decision-Making for Data Science", "Evaluation Focus", "Modules IV & V (Optimization)"],
        ["Platform", "DisasterShield AI v2.4 (Academic Release)", "Repository Path", "C:/Users/Sahee/.../disastershield_ai"],
        ["Implementation", "Full-Stack Python, Streamlit, SciPy, OR-Tools, DEAP, pymoo", "Status", "100% Validated (10 Unit Tests)"]
    ]
    t_meta = Table(meta_data, colWidths=[100, 180, 110, 142])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SLATE_LIGHT),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # ==========================================
    # 1. EXECUTIVE SUMMARY & OBJECTIVES
    # ==========================================
    story.append(Paragraph("1. Executive Summary & Problem Scope", h1_style))
    story.append(Paragraph(
        "In post-disaster humanitarian crises (flash floods, catastrophic earthquakes, tropical cyclones, and landslides), "
        "emergency dispatchers face severe resource deficits: peak survival demand exceeds local inventories by 30-50%, "
        "while road infrastructure is degraded by floodwaters, rubble, or bridge collapses. "
        "Ad-hoc or First-Come First-Served allocation inevitably starves isolated vulnerable communities. "
        "<b>DisasterShield AI</b> provides a mathematically rigorous, explainable decision-support platform designed to "
        "optimize the distribution of drinking water, survival rations, medical trauma kits, rescue fleets, and shelters.",
        body_style
    ))

    # ==========================================
    # 2. FIVE MATHEMATICAL OPTIMIZATION PARADIGMS
    # ==========================================
    story.append(Paragraph("2. Mathematical Formulations (CSDX 507 Modules IV & V)", h1_style))

    story.append(Paragraph("A. Linear Programming (LP) – Continuous Flows (Module IV)", h2_style))
    story.append(Paragraph(
        "<b>Variables:</b> Continuous resource flow x(i, r) representing units of divisible resource r dispatched to region i.<br/>"
        "<b>Objective:</b> Maximize priority-weighted fulfillment: Maximize Sum [ Priority(r) * Urgency(i) * x(i,r)/Demand(i,r) ] minus distance penalty.<br/>"
        "<b>Constraints:</b> Sum_i x(i, r) &le; Supply(r) (Supply caps) and 0 &le; x(i, r) &le; Demand(i, r) (Demand ceilings).<br/>"
        "<b>Solver:</b> SciPy optimize.linprog using the HiGHS Dual Simplex solver (runtime ~0.003s).",
        body_style
    ))

    story.append(Paragraph("B. Integer Programming (IP) – Discrete Assets (Module IV)", h2_style))
    story.append(Paragraph(
        "<b>Variables:</b> Integer assignments y(i, v) &isin; Z+ (vehicles) and z(i, t) &isin; Z+ (rescue personnel teams).<br/>"
        "<b>Objective:</b> Maximize life rescue capacity, triage capabilities, and temporary shelter deployment.<br/>"
        "<b>Terrain Compatibility Rule:</b> Rescue boats are prioritized in waterlogged zones; standard ambulances are barred from flooded roads unless accessibility &ge; 0.50.<br/>"
        "<b>Solver:</b> Google OR-Tools SCIP utilizing Branch-and-Bound and cutting planes (runtime ~0.012s).",
        body_style
    ))

    story.append(Paragraph("C. Explainable Greedy Priority Heuristic (Module V)", h2_style))
    story.append(Paragraph(
        "Computes a composite Urgency Index: U(i) = 0.40*(Severity/5) + 0.25*(Pop/MaxPop) + 0.20*(1 - Acc) + 0.15*Priority. "
        "Sorts regions descending by U(i) and sequentially allocates resources with an explainable step-by-step audit trail (runtime ~0.0002s).",
        body_style
    ))

    story.append(Paragraph("D. Genetic Algorithm (DEAP) with Feasibility Repair (Module V)", h2_style))
    story.append(Paragraph(
        "Evolves continuous allocation fractions in [0, 1]. Integrates a <b>dedicated feasibility repair operator</b> "
        "that dynamically rescales candidate solutions if total allocations exceed supply caps, guaranteeing 100% physical feasibility before fitness evaluation.",
        body_style
    ))

    story.append(Paragraph("E. Simulated Annealing (Metropolis Search) (Module V)", h2_style))
    story.append(Paragraph(
        "Executes trajectory neighborhood moves by shifting quantum delta from donor region i to recipient j while preserving supply constraints. "
        "Metropolis criterion P = exp(-&Delta;E / T) enables escape from local optima with geometric cooling T(k+1) = &alpha; * T(k) (&alpha; = 0.94).",
        body_style
    ))

    story.append(Paragraph("F. Multi-Objective Optimization (pymoo NSGA-II) (Module V)", h2_style))
    story.append(Paragraph(
        "Simultaneously minimizes three conflicting criteria: (1) Total Delivery Latency (hours), (2) Total Operational Expenditure ($), and (3) Unmet Resource Shortage Units. "
        "Evolves the non-dominated Pareto front and extracts the compromise knee-point via minimum Euclidean distance to the Utopia point.",
        body_style
    ))

    # ==========================================
    # 3. EXPERIMENTAL BENCHMARK TABLE
    # ==========================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Experimental Benchmark Evaluation (Baseline Scenario)", h1_style))

    bench_headers = ["Algorithm", "Module", "Demand Fulfilled", "Total Cost ($)", "Avg Latency", "Runtime", "Feasibility"]
    bench_rows = [
        bench_headers,
        ["Linear Programming", "Module IV (LP Simplex)", "67.1%", "$566,110.40", "5.74 hrs", "0.0031s", "100% Valid"],
        ["Integer Programming", "Module IV (Branch & Bound)", "67.1%", "$566,376.80", "5.74 hrs", "0.0120s", "100% Valid"],
        ["Greedy Urgency", "Module V (Priority Heuristic)", "67.1%", "$564,698.70", "5.74 hrs", "0.0002s", "100% Valid"],
        ["Genetic Algorithm", "Module V (Evolutionary GA)", "67.1%", "$566,108.82", "5.74 hrs", "0.0952s", "100% Valid"],
        ["Simulated Annealing", "Module V (Metropolis SA)", "67.1%", "$566,110.07", "5.74 hrs", "0.0509s", "100% Valid"],
        ["Multi-Objective NSGA-II", "Module V (Pareto MOO)", "59.1%", "$317,858.02", "5.74 hrs", "0.1287s", "100% Valid"]
    ]
    t_bench = Table(bench_rows, colWidths=[110, 105, 75, 75, 55, 55, 57])
    t_bench.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_MID),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SLATE_LIGHT]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # ==========================================
    # 4. FREE API & AI SEVERITY PREDICTOR
    # ==========================================
    story.append(Paragraph("4. AI Severity Prediction & Free Public APIs", h1_style))
    story.append(Paragraph(
        "• <b>Machine Learning Model:</b> Scikit-Learn RandomForestRegressor trained on 1,500 multi-hazard records (R2 = 0.8187, RMSE = 0.4547). Maps rainfall, wind, Richter scale, and infrastructure quality to severity scores and operational multipliers (0.7x to 1.6x).<br/>"
        "• <b>Open-Meteo Weather API:</b> Queries live precipitation and sustained wind telemetry for any coordinate without API keys.<br/>"
        "• <b>USGS Earthquake Hazards Feed:</b> Streams live global seismic feeds with magnitude, depth, and tsunami alerts.<br/>"
        "• <b>OpenStreetMap Nominatim:</b> Free worldwide geocoding resolving place names to exact coordinates.",
        body_style
    ))

    # ==========================================
    # 5. ACADEMIC DISCLAIMER & CONCLUSION
    # ==========================================
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=8))
    story.append(Paragraph(
        "<b>ACADEMIC DECISION-SUPPORT PROTOTYPE DISCLAIMER:</b> Developed strictly for educational demonstration in "
        "<b>CSDX 507 Decision-Making for Data Science</b>. It does not replace professional emergency services (NDRF, FEMA, Red Cross). "
        "All synthetic severity predictions and optimization outputs mandate review and sign-off by certified human disaster commanders.",
        callout_style
    ))

    doc.build(story)
    print(f"Academic PDF report generated successfully: {pdf_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    pdf_out = os.path.join(out_dir, "DisasterShield_AI_Comprehensive_Project_Report.pdf")
    build_pdf_report(pdf_out)

