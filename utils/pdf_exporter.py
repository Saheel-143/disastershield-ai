"""
PDF and CSV Report Generator for DisasterShield AI.
Uses ReportLab to compile clean, publication-ready emergency logistics
plans and algorithm benchmark evaluations with academic disclaimers.
"""

import io
import pandas as pd
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_allocation_pdf(
    result: Any,
    problem: Any,
    scenario_info: Dict[str, Any]
) -> bytes:
    """
    Generates a professional disaster dispatch PDF report as raw bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0B192C")
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#FF6500")
    )
    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1E3E62")
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748B")
    )

    story = []

    # Title & Header
    story.append(Paragraph("DISASTERSHIELD AI – EMERGENCY RESOURCE ALLOCATION PLAN", title_style))
    story.append(Paragraph("CSDX 507 Decision-Making for Data Science | Operations Research & AI Decision Support", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#FF6500"), spaceAfter=12))

    # Scenario Overview
    disaster_name = scenario_info.get("name", "Active Emergency Scenario")
    d_type = scenario_info.get("type", "Multi-Hazard")
    story.append(Paragraph(f"<b>Disaster Incident:</b> {disaster_name} ({d_type})", body_style))
    story.append(Paragraph(f"<b>Optimization Engine:</b> {result.algorithm_name}", body_style))
    story.append(Paragraph(f"<b>Runtime Duration:</b> {result.execution_time_sec:.4f} seconds | <b>Constraint Feasibility:</b> {'100% FEASIBLE' if result.is_feasible else 'VIOLATION DETECTED'}", body_style))
    story.append(Spacer(1, 10))

    # Executive KPIs Table
    story.append(Paragraph("1. Executive Allocation Summary", section_style))
    story.append(Spacer(1, 4))

    summary_data = [
        ["Metric", "Value", "Metric", "Value"],
        ["Fulfilled Demand Ratio", f"{result.fulfilled_demand_ratio * 100:.1f}%", "Total Estimated Cost", f"${result.total_cost:,.2f}"],
        ["Avg Delivery Travel Time", f"{result.avg_delivery_time:.2f} hrs", "Max Delivery Travel Time", f"{result.max_delivery_time:.2f} hrs"],
        ["Affected Regions Covered", f"{len(problem.regions)} Regions", "Status", "OPTIMIZED (Academic Run)"]
    ]
    t_summary = Table(summary_data, colWidths=[130, 130, 140, 140])
    t_summary.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B192C")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 14))

    # Regional Allocations Table
    story.append(Paragraph("2. Regional Resource Distribution Matrix", section_style))
    story.append(Spacer(1, 4))

    reg_table_data = [["Region", "Severity", "Pop", "Water (L)", "Food (Pkts)", "Med Kits", "Vehicles", "Teams"]]
    for reg in problem.regions:
        r_name = reg["name"]
        allocs = result.allocation_matrix.get(r_name, {})
        v_allocs = result.vehicle_allocation.get(r_name, {})
        t_allocs = result.team_allocation.get(r_name, {})

        water_qty = f"{allocs.get('Clean Drinking Water', 0):,.0f}"
        food_qty = f"{allocs.get('Ready-to-Eat Food Packets', 0):,.0f}"
        med_qty = f"{allocs.get('Emergency Medical Kits', 0):,.0f}"
        tot_veh = sum(v_allocs.values())
        tot_teams = sum(t_allocs.values())

        reg_table_data.append([
            r_name[:18],
            f"{reg['severity']:.1f}",
            f"{reg['population']:,}",
            water_qty,
            food_qty,
            med_qty,
            str(tot_veh),
            str(tot_teams)
        ])

    t_reg = Table(reg_table_data, colWidths=[110, 45, 55, 75, 75, 60, 55, 55])
    t_reg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3E62")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 14))

    # Shortage & Unmet Demand Breakdown
    story.append(Paragraph("3. Unmet Resource Deficits & Shortages", section_style))
    story.append(Spacer(1, 4))

    shortage_data = [["Resource Item", "Total Demanded", "Total Allocated", "Remaining Deficit", "Fulfillment %"]]
    demands = problem.get_total_demand_by_resource()
    for res in problem.resources:
        r_name = res["name"]
        dem = demands.get(r_name, 0.0)
        unmet = result.unmet_demand.get(r_name, 0.0)
        alloc = max(0.0, dem - unmet)
        pct = (alloc / dem * 100.0) if dem > 0 else 100.0
        shortage_data.append([
            r_name,
            f"{dem:,.0f} {res['unit']}",
            f"{alloc:,.0f} {res['unit']}",
            f"{unmet:,.0f} {res['unit']}",
            f"{pct:.1f}%"
        ])

    t_short = Table(shortage_data, colWidths=[140, 100, 100, 100, 100])
    t_short.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FEF2F2")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_short)
    story.append(Spacer(1, 16))

    # Safety Disclaimer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94A3B8"), spaceAfter=6))
    story.append(Paragraph(
        "<b>ACADEMIC DECISION-SUPPORT PROTOTYPE DISCLAIMER:</b> This report is generated by an academic optimization "
        "framework developed for CSDX 507 Decision-Making for Data Science. It does not replace certified emergency "
        "services (NDRF / FEMA). All allocations are model demonstrations and require formal review by human disaster "
        "coordinators before real-world operational execution.",
        disclaimer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_allocation_csv(result: Any, problem: Any) -> str:
    """Generates CSV string of the regional allocation table."""
    rows = []
    for reg in problem.regions:
        r_name = reg["name"]
        allocs = result.allocation_matrix.get(r_name, {})
        v_allocs = result.vehicle_allocation.get(r_name, {})
        t_allocs = result.team_allocation.get(r_name, {})

        row = {
            "Region": r_name,
            "Severity": reg["severity"],
            "Population": reg["population"],
            "Distance_km": reg["distance_km"],
            "Accessibility_Score": reg["accessibility_score"],
            "Road_Condition": reg.get("road_condition", ""),
            "Water_Allocated_Liters": allocs.get("Clean Drinking Water", 0.0),
            "Food_Allocated_Packets": allocs.get("Ready-to-Eat Food Packets", 0.0),
            "MedKits_Allocated": allocs.get("Emergency Medical Kits", 0.0),
            "Shelters_Allocated": allocs.get("Temporary Emergency Shelters", 0.0),
            "Vehicles_Total": sum(v_allocs.values()),
            "Teams_Total": sum(t_allocs.values())
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    return df.to_csv(index=False)
