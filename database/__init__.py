"""Database package initialization."""
from database.db import (
    init_db,
    get_connection,
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
    DB_PATH
)

__all__ = [
    "init_db",
    "get_connection",
    "get_all_regions",
    "get_all_resources",
    "get_all_vehicles",
    "get_all_teams",
    "get_disaster_info",
    "update_region_demands",
    "add_region",
    "delete_region",
    "update_resource_inventory",
    "update_vehicle_inventory",
    "update_team_inventory",
    "reset_database_to_default",
    "save_allocation_result",
    "get_allocation_history",
    "get_catalog_scenario_names",
    "load_scenario_by_name",
    "DB_PATH"
]
