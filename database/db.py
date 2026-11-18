"""
Database management module for DisasterShield AI using SQLite.
Handles table creation, CRUD operations, scenario persistence,
State Emergency Operations Centres (SEOC) for India, and loading structured baseline data.
"""

import sqlite3
import os
import json
from typing import List, Dict, Any, Optional
import pandas as pd

from data.default_data import (
    ALL_INDIA_SEOC_HUBS,
    get_seoc_for_state,
    CENTRAL_DEPOT,
    DEFAULT_DISASTER,
    DEFAULT_REGIONS,
    DEFAULT_RESOURCES,
    DEFAULT_VEHICLES,
    DEFAULT_TEAMS
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "disastershield.db")

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = DB_PATH, force_reset: bool = False):
    """Initializes tables, migrates columns, and seeds default data and SEOC hubs."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    if force_reset:
        cursor.execute("DROP TABLE IF EXISTS allocation_results")
        cursor.execute("DROP TABLE IF EXISTS affected_regions")
        cursor.execute("DROP TABLE IF EXISTS resources")
        cursor.execute("DROP TABLE IF EXISTS vehicles")
        cursor.execute("DROP TABLE IF EXISTS teams")
        cursor.execute("DROP TABLE IF EXISTS disasters")
        cursor.execute("DROP TABLE IF EXISTS scenarios")
        cursor.execute("DROP TABLE IF EXISTS state_emergency_hubs")

    # 1. State Emergency Operations Centres (SEOC) Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS state_emergency_hubs (
        hub_id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_name TEXT NOT NULL UNIQUE,
        hub_name TEXT NOT NULL,
        address TEXT,
        latitude REAL,
        longitude REAL,
        contact_number TEXT,
        source_url TEXT,
        verification_status TEXT NOT NULL
    )
    """)

    # 2. Disasters Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disasters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        state_name TEXT NOT NULL DEFAULT 'Tamil Nadu',
        declaration_date TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT
    )
    """)

    # Migration check for state_name column in disasters
    cursor.execute("PRAGMA table_info(disasters)")
    d_cols = [row[1] for row in cursor.fetchall()]
    if "state_name" not in d_cols:
        cursor.execute("ALTER TABLE disasters ADD COLUMN state_name TEXT NOT NULL DEFAULT 'Tamil Nadu'")

    # 3. Affected Regions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS affected_regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disaster_id INTEGER,
        state_name TEXT NOT NULL DEFAULT 'Tamil Nadu',
        district TEXT NOT NULL DEFAULT 'General',
        name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        population INTEGER NOT NULL,
        severity REAL NOT NULL,
        accessibility_score REAL NOT NULL,
        road_condition TEXT NOT NULL,
        distance_km REAL NOT NULL,
        travel_time_hours REAL NOT NULL,
        water_demand REAL NOT NULL,
        food_demand REAL NOT NULL,
        med_demand REAL NOT NULL,
        vehicle_demand INTEGER NOT NULL,
        team_demand INTEGER NOT NULL,
        shelter_demand INTEGER NOT NULL,
        critical_priority TEXT NOT NULL,
        FOREIGN KEY(disaster_id) REFERENCES disasters(id)
    )
    """)

    # Migration check for state_name and district in affected_regions
    cursor.execute("PRAGMA table_info(affected_regions)")
    r_cols = [row[1] for row in cursor.fetchall()]
    if "state_name" not in r_cols:
        cursor.execute("ALTER TABLE affected_regions ADD COLUMN state_name TEXT NOT NULL DEFAULT 'Tamil Nadu'")
    if "district" not in r_cols:
        cursor.execute("ALTER TABLE affected_regions ADD COLUMN district TEXT NOT NULL DEFAULT 'General'")

    # 4. Resources Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        unit TEXT NOT NULL,
        total_available REAL NOT NULL,
        unit_cost REAL NOT NULL,
        unit_weight_kg REAL NOT NULL,
        priority_weight REAL NOT NULL,
        description TEXT
    )
    """)

    # 5. Vehicles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        total_available INTEGER NOT NULL,
        cargo_capacity_kg REAL NOT NULL,
        speed_kmh REAL NOT NULL,
        cost_per_km REAL NOT NULL,
        can_handle_rough_terrain INTEGER NOT NULL,
        can_handle_waterlogged INTEGER NOT NULL
    )
    """)

    # 6. Teams Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        total_available INTEGER NOT NULL,
        personnel_per_team INTEGER NOT NULL,
        specialization TEXT NOT NULL,
        daily_cost REAL NOT NULL
    )
    """)

    # 7. Allocation Results Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allocation_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        algorithm_name TEXT NOT NULL,
        execution_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        scenario_name TEXT NOT NULL,
        fulfilled_demand_ratio REAL NOT NULL,
        total_cost REAL NOT NULL,
        avg_delivery_time REAL NOT NULL,
        execution_time_sec REAL NOT NULL,
        is_feasible INTEGER NOT NULL,
        summary_json TEXT NOT NULL,
        allocation_details_json TEXT NOT NULL
    )
    """)

    # 8. Scenarios Metadata Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        disaster_type TEXT NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed All-India SEOC Hubs (always keep up to date)
    seed_state_emergency_hubs(conn)

    # Check if empty, then seed default scenario
    cursor.execute("SELECT COUNT(*) FROM disasters")
    if cursor.fetchone()[0] == 0:
        seed_default_data(conn)

    conn.close()

def seed_state_emergency_hubs(conn: sqlite3.Connection):
    """Seeds or refreshes all 28 states and 8 union territories SEOC hubs."""
    cursor = conn.cursor()
    for hub in ALL_INDIA_SEOC_HUBS:
        cursor.execute("""
            INSERT INTO state_emergency_hubs (
                hub_id, state_name, hub_name, address, latitude, longitude,
                contact_number, source_url, verification_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(hub_id) DO UPDATE SET
                state_name = excluded.state_name,
                hub_name = excluded.hub_name,
                address = excluded.address,
                latitude = excluded.latitude,
                longitude = excluded.longitude,
                contact_number = excluded.contact_number,
                source_url = excluded.source_url,
                verification_status = excluded.verification_status
        """, (
            hub["hub_id"], hub["state_name"], hub["hub_name"], hub["address"],
            hub["latitude"], hub["longitude"], hub.get("contact_number"),
            hub.get("source_url"), hub["verification_status"]
        ))
    conn.commit()

def seed_default_data(conn: sqlite3.Connection):
    """Seeds the default scenario data into the database."""
    cursor = conn.cursor()

    # Seed Disaster
    cursor.execute("""
        INSERT INTO disasters (id, name, type, state_name, declaration_date, status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        DEFAULT_DISASTER["id"],
        DEFAULT_DISASTER["name"],
        DEFAULT_DISASTER["type"],
        DEFAULT_DISASTER.get("state_name", "Tamil Nadu"),
        DEFAULT_DISASTER["declaration_date"],
        DEFAULT_DISASTER["status"],
        DEFAULT_DISASTER["description"]
    ))

    # Seed Regions
    for r in DEFAULT_REGIONS:
        cursor.execute("""
            INSERT INTO affected_regions (
                id, disaster_id, state_name, district, name, latitude, longitude, population, severity,
                accessibility_score, road_condition, distance_km, travel_time_hours,
                water_demand, food_demand, med_demand, vehicle_demand, team_demand,
                shelter_demand, critical_priority
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["id"], DEFAULT_DISASTER["id"], r.get("state_name", "Tamil Nadu"),
            r.get("district", "General"), r["name"], r["latitude"], r["longitude"],
            r["population"], r["severity"], r["accessibility_score"], r["road_condition"],
            r["distance_km"], r["travel_time_hours"], r["water_demand"], r["food_demand"],
            r["med_demand"], r["vehicle_demand"], r["team_demand"], r["shelter_demand"],
            r["critical_priority"]
        ))

    # Seed Resources
    for res in DEFAULT_RESOURCES:
        cursor.execute("""
            INSERT INTO resources (
                id, name, type, unit, total_available, unit_cost, unit_weight_kg,
                priority_weight, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            res["id"], res["name"], res["type"], res["unit"], res["total_available"],
            res["unit_cost"], res["unit_weight_kg"], res["priority_weight"], res["description"]
        ))

    # Seed Vehicles
    for v in DEFAULT_VEHICLES:
        cursor.execute("""
            INSERT INTO vehicles (
                id, type, total_available, cargo_capacity_kg, speed_kmh, cost_per_km,
                can_handle_rough_terrain, can_handle_waterlogged
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            v["id"], v["type"], v["total_available"], v["cargo_capacity_kg"],
            v["speed_kmh"], v["cost_per_km"], v["can_handle_rough_terrain"],
            v["can_handle_waterlogged"]
        ))

    # Seed Teams
    for t in DEFAULT_TEAMS:
        cursor.execute("""
            INSERT INTO teams (
                id, type, total_available, personnel_per_team, specialization, daily_cost
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            t["id"], t["type"], t["total_available"], t["personnel_per_team"],
            t["specialization"], t["daily_cost"]
        ))

    # Seed Default Scenario catalog entry
    cursor.execute("""
        INSERT OR IGNORE INTO scenarios (name, disaster_type, description)
        VALUES (?, ?, ?)
    """, (
        "Tamil Nadu Flood & Coastal Surge",
        "Flood",
        "Demonstrates automatic SEOC identification for Tamil Nadu and localized coastal resource distribution."
    ))

    conn.commit()

# --- State Emergency Operations Centres (SEOC) Queries & Updates ---

def get_all_state_hubs(db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns all 36 Indian states and union territories SEOC hubs."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM state_emergency_hubs ORDER BY state_name ASC", conn)
    conn.close()
    return df

def get_state_hub(state_name: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Returns the SEOC hub for a specific state or UT."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM state_emergency_hubs WHERE LOWER(state_name) = LOWER(?)", (state_name.strip(),))
    row = cursor.fetchone()
    if not row:
        # Fuzzy match
        cursor.execute("SELECT * FROM state_emergency_hubs WHERE LOWER(state_name) LIKE LOWER(?)", (f"%{state_name.strip()}%",))
        row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return get_seoc_for_state(state_name)

def get_hubs_for_states(state_names: List[str], db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Retrieves SEOC hubs for a list of states (e.g. for multi-state disasters)."""
    hubs = []
    seen = set()
    for s in state_names:
        h = get_state_hub(s, db_path=db_path)
        if h and h["state_name"] not in seen:
            seen.add(h["state_name"])
            hubs.append(h)
    return hubs

def update_state_hub(hub_id: int, updates: Dict[str, Any], db_path: str = DB_PATH):
    """Updates SEOC hub details such as address, coordinates, or verification status."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [hub_id]
    cursor.execute(f"UPDATE state_emergency_hubs SET {fields} WHERE hub_id = ?", values)
    conn.commit()
    conn.close()

def add_state_hub(hub_data: Dict[str, Any], db_path: str = DB_PATH) -> int:
    """Adds a new state or regional emergency hub."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO state_emergency_hubs (
            state_name, hub_name, address, latitude, longitude, contact_number,
            source_url, verification_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        hub_data["state_name"], hub_data["hub_name"], hub_data.get("address"),
        hub_data.get("latitude"), hub_data.get("longitude"), hub_data.get("contact_number"),
        hub_data.get("source_url"), hub_data.get("verification_status", "VERIFIED")
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_hub_verification_summary(db_path: str = DB_PATH) -> Dict[str, int]:
    """Returns total, verified, and unverified hub counts."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM state_emergency_hubs")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM state_emergency_hubs WHERE verification_status = 'VERIFIED'")
    verified = cursor.fetchone()[0]
    unverified = total - verified
    conn.close()
    return {"total": total, "verified": verified, "unverified": unverified}

def get_active_hub_for_disaster(db_path: str = DB_PATH) -> Dict[str, Any]:
    """
    Dynamically retrieves the SEOC coordination hub for the active disaster.
    If multiple states are affected, returns the primary state hub.
    """
    d_info = get_disaster_info(db_path=db_path)
    state_field = d_info.get("state_name", "Tamil Nadu")
    primary_state = [s.strip() for s in state_field.split(",")][0]
    hub = get_state_hub(primary_state, db_path=db_path)
    if hub:
        return hub
    return CENTRAL_DEPOT

# --- Query & CRUD Helpers for Disasters and Regions ---

def get_all_regions(db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns all affected regions as a pandas DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM affected_regions ORDER BY id ASC", conn)
    conn.close()
    return df

def get_regions_by_state(state_name: Optional[str] = None, db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns regions filtered by state."""
    conn = get_connection(db_path)
    if state_name:
        df = pd.read_sql_query(
            "SELECT * FROM affected_regions WHERE LOWER(state_name) = LOWER(?) ORDER BY id ASC",
            conn, params=(state_name.strip(),)
        )
    else:
        df = pd.read_sql_query("SELECT * FROM affected_regions ORDER BY id ASC", conn)
    conn.close()
    return df

def get_all_resources(db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns all resources as a pandas DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM resources ORDER BY id ASC", conn)
    conn.close()
    return df

def get_all_vehicles(db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns all vehicle fleets as a pandas DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM vehicles ORDER BY id ASC", conn)
    conn.close()
    return df

def get_all_teams(db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns all rescue teams as a pandas DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM teams ORDER BY id ASC", conn)
    conn.close()
    return df

def get_disaster_info(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Returns the primary active disaster info."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disasters ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return DEFAULT_DISASTER

def update_region_demands(region_id: int, updates: Dict[str, Any], db_path: str = DB_PATH):
    """Updates specific fields of an affected region."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [region_id]
    cursor.execute(f"UPDATE affected_regions SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()

def add_region(region_data: Dict[str, Any], db_path: str = DB_PATH) -> int:
    """Inserts a new region and returns its generated id."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO affected_regions (
            disaster_id, state_name, district, name, latitude, longitude, population, severity,
            accessibility_score, road_condition, distance_km, travel_time_hours,
            water_demand, food_demand, med_demand, vehicle_demand, team_demand,
            shelter_demand, critical_priority
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        region_data.get("disaster_id", 1),
        region_data.get("state_name", "Tamil Nadu"),
        region_data.get("district", "General"),
        region_data["name"],
        region_data["latitude"],
        region_data["longitude"],
        region_data["population"],
        region_data["severity"],
        region_data["accessibility_score"],
        region_data.get("road_condition", "Partially Damaged"),
        region_data["distance_km"],
        region_data["travel_time_hours"],
        region_data["water_demand"],
        region_data["food_demand"],
        region_data["med_demand"],
        region_data["vehicle_demand"],
        region_data["team_demand"],
        region_data["shelter_demand"],
        region_data.get("critical_priority", "Medium")
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def delete_region(region_id: int, db_path: str = DB_PATH):
    """Deletes a region by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM affected_regions WHERE id = ?", (region_id,))
    conn.commit()
    conn.close()

def update_resource_inventory(resource_id: int, new_quantity: float, db_path: str = DB_PATH):
    """Updates available inventory of a resource."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE resources SET total_available = ? WHERE id = ?", (new_quantity, resource_id))
    conn.commit()
    conn.close()

def update_vehicle_inventory(vehicle_id: int, new_quantity: int, db_path: str = DB_PATH):
    """Updates vehicle count."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE vehicles SET total_available = ? WHERE id = ?", (new_quantity, vehicle_id))
    conn.commit()
    conn.close()

def update_team_inventory(team_id: int, new_quantity: int, db_path: str = DB_PATH):
    """Updates team count."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE teams SET total_available = ? WHERE id = ?", (new_quantity, team_id))
    conn.commit()
    conn.close()

def save_allocation_result(result_data: Dict[str, Any], db_path: str = DB_PATH) -> int:
    """Persists an algorithm run result to SQLite."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO allocation_results (
            algorithm_name, scenario_name, fulfilled_demand_ratio, total_cost,
            avg_delivery_time, execution_time_sec, is_feasible, summary_json, allocation_details_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result_data["algorithm_name"],
        result_data.get("scenario_name", "Standard Baseline"),
        result_data["fulfilled_demand_ratio"],
        result_data["total_cost"],
        result_data["avg_delivery_time"],
        result_data["execution_time_sec"],
        1 if result_data["is_feasible"] else 0,
        json.dumps(result_data.get("summary", {})),
        json.dumps(result_data.get("allocation_details", []))
    ))
    res_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return res_id

def get_allocation_history(db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns past algorithm benchmark runs."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM allocation_results ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    return df

def reset_database_to_default(db_path: str = DB_PATH):
    """Resets the entire database to the default pristine sample state."""
    init_db(db_path=db_path, force_reset=True)

def get_catalog_scenario_names() -> List[str]:
    """Returns the names of all pre-configured multi-hazard scenarios."""
    from data.default_data import SCENARIOS_CATALOG
    return list(SCENARIOS_CATALOG.keys())

def load_scenario_by_name(scenario_name: str, db_path: str = DB_PATH) -> bool:
    """
    Clears current active disaster tables and seeds a full scenario from the catalog,
    automatically updating the state, regions, and linking to its designated SEOC hub.
    """
    from data.default_data import SCENARIOS_CATALOG
    if scenario_name not in SCENARIOS_CATALOG:
        return False

    sc_data = SCENARIOS_CATALOG[scenario_name]
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM affected_regions")
    cursor.execute("DELETE FROM resources")
    cursor.execute("DELETE FROM vehicles")
    cursor.execute("DELETE FROM teams")
    cursor.execute("DELETE FROM disasters")

    # Disaster
    d = sc_data["disaster"]
    cursor.execute("""
        INSERT INTO disasters (id, name, type, state_name, declaration_date, status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        d["id"], d["name"], d["type"], d.get("state_name", "Tamil Nadu"),
        d["declaration_date"], d["status"], d["description"]
    ))

    # Regions
    for r in sc_data["regions"]:
        cursor.execute("""
            INSERT INTO affected_regions (
                id, disaster_id, state_name, district, name, latitude, longitude, population, severity,
                accessibility_score, road_condition, distance_km, travel_time_hours,
                water_demand, food_demand, med_demand, vehicle_demand, team_demand,
                shelter_demand, critical_priority
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["id"], d["id"], r.get("state_name", d.get("state_name", "Tamil Nadu")),
            r.get("district", "General"), r["name"], r["latitude"], r["longitude"],
            r["population"], r["severity"], r["accessibility_score"], r["road_condition"],
            r["distance_km"], r["travel_time_hours"], r["water_demand"], r["food_demand"],
            r["med_demand"], r["vehicle_demand"], r["team_demand"], r["shelter_demand"],
            r["critical_priority"]
        ))

    # Resources
    for res in sc_data["resources"]:
        cursor.execute("""
            INSERT INTO resources (
                id, name, type, unit, total_available, unit_cost, unit_weight_kg,
                priority_weight, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            res["id"], res["name"], res["type"], res["unit"], res["total_available"],
            res["unit_cost"], res["unit_weight_kg"], res["priority_weight"], res["description"]
        ))

    # Vehicles
    for v in sc_data["vehicles"]:
        cursor.execute("""
            INSERT INTO vehicles (
                id, type, total_available, cargo_capacity_kg, speed_kmh, cost_per_km,
                can_handle_rough_terrain, can_handle_waterlogged
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            v["id"], v["type"], v["total_available"], v["cargo_capacity_kg"],
            v["speed_kmh"], v["cost_per_km"], v["can_handle_rough_terrain"],
            v["can_handle_waterlogged"]
        ))

    # Teams
    for t in sc_data["teams"]:
        cursor.execute("""
            INSERT INTO teams (
                id, type, total_available, personnel_per_team, specialization, daily_cost
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            t["id"], t["type"], t["total_available"], t["personnel_per_team"],
            t["specialization"], t["daily_cost"]
        ))

    conn.commit()
    conn.close()
    return True
