"""
Interactive Folium Map Visualizer for DisasterShield AI.
Renders state-wise and multi-state emergency logistics maps with:
- Blue marker: State Emergency Operations Centre (SEOC)
- Red markers: Critical affected areas (severity >= 4.5)
- Orange markers: High-priority affected areas (3.5 <= severity < 4.5)
- Yellow markers: Medium-priority affected areas (2.5 <= severity < 3.5)
- Green markers: Safe / adequately supported areas (severity < 2.5)
- Polyline dispatch corridors from matching SEOC to affected zones
- Graceful omission of fabricated markers for UNVERIFIED hubs
"""

import folium
from folium import plugins
from typing import List, Dict, Any, Optional, Union

def create_disaster_map(
    regions: List[Dict[str, Any]],
    central_depot: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    hubs: Optional[List[Dict[str, Any]]] = None,
    allocation_matrix: Optional[Dict[str, Dict[str, float]]] = None,
    zoom_start: int = 8
) -> folium.Map:
    """
    Builds a dynamic interactive Folium map centered on the selected state(s)
    and their corresponding State Emergency Operations Centres (SEOC).
    """
    # Normalize hubs list
    hub_list: List[Dict[str, Any]] = []
    if hubs:
        hub_list = hubs
    elif central_depot:
        if isinstance(central_depot, list):
            hub_list = central_depot
        elif isinstance(central_depot, dict):
            hub_list = [central_depot]

    # Map state name to verified hub object for corridor routing
    state_to_hub: Dict[str, Dict[str, Any]] = {}
    verified_hubs: List[Dict[str, Any]] = []

    for h in hub_list:
        s_name = h.get("state_name", "").strip().lower()
        is_verified = (h.get("verification_status") == "VERIFIED") and (h.get("latitude") is not None) and (h.get("longitude") is not None)
        if is_verified:
            verified_hubs.append(h)
            if s_name:
                state_to_hub[s_name] = h

    # Gather all coordinates to compute dynamic bounding box
    all_coords = []
    for h in verified_hubs:
        all_coords.append((float(h["latitude"]), float(h["longitude"])))
    for r in regions:
        if r.get("latitude") is not None and r.get("longitude") is not None:
            all_coords.append((float(r["latitude"]), float(r["longitude"])))

    # Determine initial center
    if all_coords:
        avg_lat = sum(c[0] for c in all_coords) / len(all_coords)
        avg_lon = sum(c[1] for c in all_coords) / len(all_coords)
    elif verified_hubs:
        avg_lat = float(verified_hubs[0]["latitude"])
        avg_lon = float(verified_hubs[0]["longitude"])
    else:
        # Default all-India center if no coordinates
        avg_lat, avg_lon = 20.5937, 78.9629
        zoom_start = 5

    # Base Folium Map
    m = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=zoom_start,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # 1. Render Blue Markers for Verified SEOCs (DO NOT render unverified or fabricated markers)
    for h in verified_hubs:
        h_lat = float(h["latitude"])
        h_lon = float(h["longitude"])
        h_name = h.get("hub_name", "State Emergency Operations Centre")
        s_name = h.get("state_name", "India")
        addr = h.get("address", "Official Government Complex")
        contact = h.get("contact_number", "1070 Emergency Helpline")
        source = h.get("source_url", "https://ndma.gov.in")

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 280px; color: #0F172A;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="background: #0284C7; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; text-transform: uppercase;">
                    🏛️ VERIFIED SEOC
                </span>
                <span style="font-size: 11px; font-weight: 700; color: #1E3E62;">{s_name}</span>
            </div>
            <h4 style="margin: 4px 0; color: #0369A1; font-weight: bold; font-size: 13px; line-height: 1.3;">
                {h_name}
            </h4>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #E2E8F0;" />
            <p style="margin: 3px 0; font-size: 11px; color: #334155;"><b>📍 Address:</b> {addr}</p>
            <p style="margin: 3px 0; font-size: 11px; color: #334155;"><b>📞 Contact:</b> <span style="color: #0369A1; font-weight: 600;">{contact}</span></p>
            <p style="margin: 3px 0; font-size: 11px; color: #334155;"><b>🌐 Portal:</b> <a href="{source}" target="_blank" style="color: #0284C7; text-decoration: underline;">{source}</a></p>
            <div style="margin-top: 6px; padding: 4px; background: #F0F9FF; border-left: 3px solid #0284C7; font-size: 10px; color: #0369A1;">
                Primary Operations & Logistics Command Hub for this disaster theater.
            </div>
        </div>
        """

        folium.Marker(
            location=[h_lat, h_lon],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"🏛️ {h_name} ({s_name}) - VERIFIED SEOC",
            icon=folium.Icon(color="blue", icon="shield", prefix="fa")
        ).add_to(m)

        # Tactical staging perimeter circle
        folium.Circle(
            location=[h_lat, h_lon],
            radius=2500,
            color="#0284C7",
            fill=True,
            fill_color="#38BDF8",
            fill_opacity=0.15,
            weight=2
        ).add_to(m)

    # 2. Regional Affected Markers & Dispatch Routes
    for reg in regions:
        r_name = reg["name"]
        reg_state = reg.get("state_name", "").strip().lower()
        district = reg.get("district", "General")
        lat = float(reg["latitude"])
        lon = float(reg["longitude"])
        sev = float(reg["severity"])
        pop = int(reg["population"])
        acc = float(reg["accessibility_score"])
        road_cond = reg.get("road_condition", "Partially Damaged")
        dist_km = float(reg.get("distance_km", 20.0))
        travel_hrs = float(reg.get("travel_time_hours", 1.5))
        priority = reg.get("critical_priority", "Medium")

        # Color coding strictly based on user specification:
        # Red: Critical (>= 4.5)
        # Orange: High Priority (3.5 - 4.4)
        # Yellow: Medium Priority (2.5 - 3.4)
        # Green: Safe / Low Priority (< 2.5)
        if sev >= 4.5:
            color = "red"
            circle_color = "#EF4444"
            badge = "CRITICAL EMERGENCY"
            status_text = "Severe Impact / Critical Deficit"
        elif sev >= 3.5:
            color = "orange"
            circle_color = "#F97316"
            badge = "HIGH PRIORITY"
            status_text = "High Damage / Urgent Deployment"
        elif sev >= 2.5:
            color = "beige"  # Folium yellow equivalent
            circle_color = "#FBBF24"
            badge = "MEDIUM PRIORITY"
            status_text = "Moderate Inundation / Monitored"
        else:
            color = "green"
            circle_color = "#10B981"
            badge = "SAFE / SUPPORTED"
            status_text = "Stable / Adequately Stocked"

        # Allocation table snippet if available
        alloc_html = ""
        if allocation_matrix and r_name in allocation_matrix:
            allocs = allocation_matrix[r_name]
            alloc_html = "<div style='margin-top: 6px; padding: 4px; background: #F1F5F9; border-radius: 4px; font-size: 11px;'>"
            alloc_html += "<b>Dispatched Supplies:</b><br/>"
            for res_name, qty in allocs.items():
                alloc_html += f"• {res_name}: {qty:,.0f}<br/>"
            alloc_html += "</div>"

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 260px; color: #111;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #0F172A; font-weight: bold; font-size: 13px;">{r_name}</h4>
                <span style="background: {circle_color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold;">
                    {badge}
                </span>
            </div>
            <div style="font-size: 11px; color: #64748B; margin-top: 2px;">District: <b>{district}</b> | State: <b>{reg.get('state_name', 'General')}</b></div>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #E2E8F0;" />
            <p style="margin: 2px 0; font-size: 11px;"><b>Status:</b> {status_text}</p>
            <p style="margin: 2px 0; font-size: 11px;"><b>Severity:</b> {sev:.1f} / 5.0 | <b>Priority:</b> {priority}</p>
            <p style="margin: 2px 0; font-size: 11px;"><b>Affected Population:</b> {pop:,}</p>
            <p style="margin: 2px 0; font-size: 11px;"><b>Distance from SEOC:</b> {dist_km:.1f} km ({travel_hrs:.1f}h)</p>
            <p style="margin: 2px 0; font-size: 11px;"><b>Road Access:</b> {road_cond} ({acc*100:.0f}%)</p>
            {alloc_html}
        </div>
        """

        # Marker Pin
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{r_name} [{district}] (Sev: {sev:.1f}, Pop: {pop:,})",
            icon=folium.Icon(color=color, icon="exclamation-triangle", prefix="fa")
        ).add_to(m)

        # Population impact radius circle
        circle_radius = max(400, int(pop / 15.0))
        folium.Circle(
            location=[lat, lon],
            radius=circle_radius,
            color=circle_color,
            fill=True,
            fill_color=circle_color,
            fill_opacity=0.25,
            weight=1.5
        ).add_to(m)

        # Dispatch corridor line connecting to the matching state's SEOC (if verified)
        target_hub = state_to_hub.get(reg_state)
        if not target_hub and verified_hubs:
            target_hub = verified_hubs[0]

        if target_hub and target_hub.get("latitude") is not None:
            h_lat = float(target_hub["latitude"])
            h_lon = float(target_hub["longitude"])
            hub_title = target_hub.get("hub_name", "SEOC")

            line_color = "#38BDF8" if acc >= 0.5 else ("#F97316" if acc >= 0.3 else "#EF4444")
            line_dash = "4, 6" if acc < 0.4 else None

            folium.PolyLine(
                locations=[[h_lat, h_lon], [lat, lon]],
                color=line_color,
                weight=2.5 if acc >= 0.5 else 1.8,
                dash_array=line_dash,
                opacity=0.75,
                tooltip=f"Relief Corridor: {hub_title} -> {r_name} ({dist_km:.1f} km, {road_cond})"
            ).add_to(m)

    # 3. Fit bounds if multiple points exist to smoothly frame the state theater
    if len(all_coords) >= 2:
        min_lat = min(c[0] for c in all_coords)
        max_lat = max(c[0] for c in all_coords)
        min_lon = min(c[1] for c in all_coords)
        max_lon = max(c[1] for c in all_coords)
        m.fit_bounds([[min_lat - 0.1, min_lon - 0.1], [max_lat + 0.1, max_lon + 0.1]])

    # Fullscreen control
    plugins.Fullscreen(position="topright").add_to(m)

    return m
