"""
Default realistic synthetic dataset for DisasterShield AI.
Includes State Emergency Operations Centres (SEOC) for all 28 Indian States and 8 Union Territories,
dynamic state disaster detection, multi-state disaster scenarios, and balanced test datasets.
"""

from typing import List, Dict, Any, Optional

# -------------------------------------------------------------------------------------------------
# ALL 28 INDIAN STATES & 8 UNION TERRITORIES: STATE EMERGENCY OPERATIONS CENTRES (SEOC)
# Sources: National Disaster Management Authority (NDMA), Ministry of Home Affairs (MHA),
# State Disaster Management Authorities (SDMA / SEOC official portals).
# -------------------------------------------------------------------------------------------------

ALL_INDIA_SEOC_HUBS: List[Dict[str, Any]] = [
    # 28 STATES
    {
        "hub_id": 1,
        "state_name": "Andhra Pradesh",
        "hub_name": "Andhra Pradesh State Disaster Management Authority (APSDMA) SEOC",
        "address": "APSDMA Campus, Kunchanapalli, Tadepalle, Guntur / Vijayawada - 522501",
        "latitude": 16.4862,
        "longitude": 80.6062,
        "contact_number": "1070 / 0863-2377118",
        "source_url": "https://apsdma.ap.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 2,
        "state_name": "Arunachal Pradesh",
        "hub_name": "Arunachal Pradesh State Emergency Operations Centre",
        "address": "Directorate of Disaster Management, Papum Pare, Civil Secretariat, Itanagar - 791111",
        "latitude": 27.0844,
        "longitude": 93.6053,
        "contact_number": "1070 / 0360-2212222",
        "source_url": "https://itanagar.nic.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 3,
        "state_name": "Assam",
        "hub_name": "Assam State Disaster Management Authority (ASDMA) SEOC",
        "address": "State Emergency Operation Centre, Assam Secretariat Complex, Dispur, Guwahati - 781006",
        "latitude": 26.1445,
        "longitude": 91.7898,
        "contact_number": "1070 / 0361-2237221",
        "source_url": "https://asdma.assam.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 4,
        "state_name": "Bihar",
        "hub_name": "Bihar State Disaster Management Authority (BSDMA) SEOC",
        "address": "Sardar Patel Bhawan, 2nd Floor, Bailey Road, Patna, Bihar - 800023",
        "latitude": 25.6093,
        "longitude": 85.1235,
        "contact_number": "1070 / 0612-2547232",
        "source_url": "https://bsdma.org",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 5,
        "state_name": "Chhattisgarh",
        "hub_name": "Chhattisgarh State Emergency Operations Centre",
        "address": "Revenue & Disaster Management Dept, Mahanadi Bhawan, Mantralaya, Nawa Raipur - 492002",
        "latitude": 21.1610,
        "longitude": 81.7876,
        "contact_number": "1070 / 0771-2223471",
        "source_url": "https://revenue.cg.nic.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 6,
        "state_name": "Goa",
        "hub_name": "Goa State Emergency Operations Centre",
        "address": "Collectorate Building, Panaji, North Goa, Goa - 403001",
        "latitude": 15.4989,
        "longitude": 73.8278,
        "contact_number": "1070 / 0832-2419550",
        "source_url": "https://goasdma.goa.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 7,
        "state_name": "Gujarat",
        "hub_name": "Gujarat State Disaster Management Authority (GSDMA) SEOC",
        "address": "Block No. 11, 5th Floor, New Sachivalaya, Sector 10, Gandhinagar, Gujarat - 382010",
        "latitude": 23.2230,
        "longitude": 72.6500,
        "contact_number": "1070 / 079-23251900",
        "source_url": "https://gsdma.org",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 8,
        "state_name": "Haryana",
        "hub_name": "Haryana State Emergency Operations Centre",
        "address": "Revenue & Disaster Management Department, Haryana Civil Secretariat, Sector 17, Chandigarh - 160017",
        "latitude": 30.7415,
        "longitude": 76.7794,
        "contact_number": "1070 / 0172-2740390",
        "source_url": "https://revenueharyana.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 9,
        "state_name": "Himachal Pradesh",
        "hub_name": "Himachal Pradesh State Disaster Management Authority (HPSDMA) SEOC",
        "address": "HP Secretariat, Armsdale Building, Chotta Shimla, Shimla - 171002",
        "latitude": 31.1048,
        "longitude": 77.1734,
        "contact_number": "1070 / 0177-2812344",
        "source_url": "https://hpsdma.nic.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 10,
        "state_name": "Jharkhand",
        "hub_name": "Jharkhand State Disaster Management Authority (JSDMA) SEOC",
        "address": "Project Building, Sector 4, Dhurwa, Ranchi, Jharkhand - 834004",
        "latitude": 23.3150,
        "longitude": 85.3120,
        "contact_number": "1070 / 0651-2446970",
        "source_url": "https://disastermgmt.jharkhand.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 11,
        "state_name": "Karnataka",
        "hub_name": "Karnataka State Disaster Management Authority (KSDMA) SEOC",
        "address": "MS Building, Dr. B.R. Ambedkar Veedhi, Bengaluru, Karnataka - 560001",
        "latitude": 12.9790,
        "longitude": 77.5913,
        "contact_number": "1070 / 080-22340676",
        "source_url": "https://ksdma.karnataka.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 12,
        "state_name": "Kerala",
        "hub_name": "Kerala State Emergency Operations Centre (KSEOC)",
        "address": "Institute of Land and Disaster Management (ILDM) Campus, PTP Nagar, Thiruvananthapuram - 695038",
        "latitude": 8.5060,
        "longitude": 76.9740,
        "contact_number": "1070 / 0471-2364424",
        "source_url": "https://sdma.kerala.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 13,
        "state_name": "Madhya Pradesh",
        "hub_name": "Madhya Pradesh State Disaster Management Authority (MPSDMA) SEOC",
        "address": "Vallabh Bhawan, Mantralaya, Bhopal, Madhya Pradesh - 462004",
        "latitude": 23.2332,
        "longitude": 77.4350,
        "contact_number": "1070 / 0755-2441419",
        "source_url": "https://mpsdma.mp.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 14,
        "state_name": "Maharashtra",
        "hub_name": "Maharashtra State Emergency Operations Centre (SEOC)",
        "address": "Relief & Rehabilitation Department, Mantralaya Control Room, Madame Cama Road, Nariman Point, Mumbai - 400032",
        "latitude": 18.9280,
        "longitude": 72.8284,
        "contact_number": "1070 / 022-22027990",
        "source_url": "https://rfd.maharashtra.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 15,
        "state_name": "Manipur",
        "hub_name": "Manipur State Emergency Operations Centre",
        "address": "Directorate of Relief & Disaster Management, Babupara, Imphal - 795001",
        "latitude": 24.8080,
        "longitude": 93.9442,
        "contact_number": "1070 / 0385-2443441",
        "source_url": "https://manipur.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 16,
        "state_name": "Meghalaya",
        "hub_name": "Meghalaya State Disaster Management Authority (MSDMA) SEOC",
        "address": "Lower Lachumiere, Shillong, Meghalaya - 793001",
        "latitude": 25.5788,
        "longitude": 91.8933,
        "contact_number": "1070 / 0364-2502098",
        "source_url": "https://msdma.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 17,
        "state_name": "Mizoram",
        "hub_name": "Mizoram State Emergency Operations Centre",
        "address": "Disaster Management & Rehabilitation Department, Chaltlang, Aizawl - 796012",
        "latitude": 23.7307,
        "longitude": 92.7173,
        "contact_number": "1070 / 0389-2395350",
        "source_url": "https://dmr.mizoram.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 18,
        "state_name": "Nagaland",
        "hub_name": "Nagaland State Disaster Management Authority (NSDMA) SEOC",
        "address": "Civil Secretariat Complex, Kohima, Nagaland - 797004",
        "latitude": 25.6751,
        "longitude": 94.1086,
        "contact_number": "1070 / 0370-2270050",
        "source_url": "https://nsdma.nagaland.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 19,
        "state_name": "Odisha",
        "hub_name": "Odisha State Disaster Management Authority (OSDMA) SEOC",
        "address": "Rajiv Bhawan, Ground Floor, Unit-5, Bhubaneswar, Odisha - 751001",
        "latitude": 20.2706,
        "longitude": 85.8334,
        "contact_number": "1070 / 0674-2395398",
        "source_url": "https://osdma.org",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 20,
        "state_name": "Punjab",
        "hub_name": "Punjab State Emergency Operations Centre",
        "address": "Department of Disaster Management, Punjab Civil Secretariat-2, Sector 9, Chandigarh - 160009",
        "latitude": 30.7588,
        "longitude": 76.8041,
        "contact_number": "1070 / 0172-2740854",
        "source_url": "https://revenue.punjab.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 21,
        "state_name": "Rajasthan",
        "hub_name": "Rajasthan State Disaster Management Authority (RSDMA) SEOC",
        "address": "Food & Civil Supplies Building, Government Secretariat, Jaipur, Rajasthan - 302005",
        "latitude": 26.8920,
        "longitude": 75.8050,
        "contact_number": "1070 / 0141-2227296",
        "source_url": "https://dmr.rajasthan.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 22,
        "state_name": "Sikkim",
        "hub_name": "Sikkim State Disaster Management Authority (SSDMA) SEOC",
        "address": "Tashiling Secretariat, Gangtok, Sikkim - 737101",
        "latitude": 27.3314,
        "longitude": 88.6138,
        "contact_number": "1070 / 03592-201075",
        "source_url": "https://ssdma.nic.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 23,
        "state_name": "Tamil Nadu",
        "hub_name": "Tamil Nadu State Emergency Operations Centre (TN SEOC)",
        "address": "Disaster Management Department, Ezhilagam Building, Chepauk, Chennai - 600005",
        "latitude": 13.0645,
        "longitude": 80.2810,
        "contact_number": "1070 / 044-28593990",
        "source_url": "https://tnsdma.tn.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 24,
        "state_name": "Telangana",
        "hub_name": "Telangana State Emergency Operations Centre (TSEOC)",
        "address": "BRKR Bhavan / Dr. B.R. Ambedkar Secretariat, Tank Bund Road, Hyderabad - 500022",
        "latitude": 17.4065,
        "longitude": 78.4691,
        "contact_number": "1070 / 040-23450624",
        "source_url": "https://disastermanagement.telangana.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 25,
        "state_name": "Tripura",
        "hub_name": "Tripura State Disaster Management Authority (TSDMA) SEOC",
        "address": "New Capital Complex, Secretariat, Agartala, Tripura - 799010",
        "latitude": 23.8315,
        "longitude": 91.2868,
        "contact_number": "1070 / 0381-2416045",
        "source_url": "https://revenue.tripura.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 26,
        "state_name": "Uttar Pradesh",
        "hub_name": "Uttar Pradesh State Disaster Management Authority (UPSDMA) SEOC",
        "address": "B-2, PICUP Bhawan, Vibhuti Khand, Gomti Nagar, Lucknow, Uttar Pradesh - 226010",
        "latitude": 26.8654,
        "longitude": 80.9983,
        "contact_number": "1070 / 0522-2720828",
        "source_url": "https://upsdma.up.nic.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 27,
        "state_name": "Uttarakhand",
        "hub_name": "Uttarakhand State Emergency Operations Centre (USDMA)",
        "address": "USDMA Building, IT Park, Sahastradhara Road, Dehradun, Uttarakhand - 248013",
        "latitude": 30.3620,
        "longitude": 78.0792,
        "contact_number": "1070 / 0135-2710334",
        "source_url": "https://usdma.uk.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 28,
        "state_name": "West Bengal",
        "hub_name": "West Bengal State Emergency Operations Centre",
        "address": "Department of Disaster Management, Nabanna (2nd Floor), 325 Sarat Chatterjee Road, Howrah - 711102",
        "latitude": 22.5574,
        "longitude": 88.3129,
        "contact_number": "1070 / 033-22143526",
        "source_url": "https://wbdmd.gov.in",
        "verification_status": "VERIFIED"
    },

    # 8 UNION TERRITORIES
    {
        "hub_id": 29,
        "state_name": "Andaman and Nicobar Islands",
        "hub_name": "Andaman & Nicobar Emergency Operations Centre",
        "address": "Directorate of Disaster Management, Port Blair, South Andaman - 744101",
        "latitude": 11.6669,
        "longitude": 92.7417,
        "contact_number": "1070 / 03192-238880",
        "source_url": "https://dm.andaman.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 30,
        "state_name": "Chandigarh",
        "hub_name": "Chandigarh Disaster Management Authority (CDMA) Control Room",
        "address": "Additional Deluxe Building, Sector 9D, Chandigarh - 160009",
        "latitude": 30.7490,
        "longitude": 76.7915,
        "contact_number": "1077 / 0172-2740405",
        "source_url": "https://chandigarh.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 31,
        "state_name": "Dadra and Nagar Haveli and Daman and Diu",
        "hub_name": "DNHDD State Emergency Operations Centre",
        "address": "Collectorate Complex, Dholar, Moti Daman - 396220",
        "latitude": 20.4078,
        "longitude": 72.8397,
        "contact_number": "1077 / 0260-2230099",
        "source_url": "https://daman.nic.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 32,
        "state_name": "Delhi",
        "hub_name": "Delhi State Emergency Operations Centre (DSEOC)",
        "address": "Revenue Department, Government of NCT of Delhi, 5 Sham Nath Marg, Civil Lines, Delhi - 110054",
        "latitude": 28.6702,
        "longitude": 77.2228,
        "contact_number": "1077 / 011-23831077",
        "source_url": "https://delhi.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 33,
        "state_name": "Jammu and Kashmir",
        "hub_name": "Jammu & Kashmir State Emergency Operations Centre",
        "address": "Relief & Rehabilitation Dept, Civil Secretariat, Jammu / Srinagar - 180001",
        "latitude": 32.7330,
        "longitude": 74.8640,
        "contact_number": "1070 / 0191-2565656",
        "source_url": "https://jksdma.jk.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 34,
        "state_name": "Ladakh",
        "hub_name": "UT Ladakh Disaster Management Authority Control Centre",
        "address": "UT Secretariat, Disaster Management Cell, Leh, Ladakh - 194101",
        "latitude": 34.1526,
        "longitude": 77.5771,
        "contact_number": "1077 / 01982-255560",
        "source_url": "https://ladakh.gov.in",
        "verification_status": "VERIFIED"
    },
    {
        "hub_id": 35,
        "state_name": "Lakshadweep",
        "hub_name": "UT of Lakshadweep Emergency Operations Centre",
        "address": "SEOC LOCATION NOT VERIFIED – CONFIGURATION REQUIRED",
        "latitude": None,
        "longitude": None,
        "contact_number": "04896-262258",
        "source_url": "https://lakshadweep.gov.in",
        "verification_status": "UNVERIFIED"
    },
    {
        "hub_id": 36,
        "state_name": "Puducherry",
        "hub_name": "Puducherry State Emergency Operations Centre",
        "address": "Department of Revenue & Disaster Management, Kamaraj Salai, Saram, Puducherry - 605013",
        "latitude": 11.9416,
        "longitude": 79.8083,
        "contact_number": "1070 / 1077 / 0413-2244414",
        "source_url": "https://disaster.py.gov.in",
        "verification_status": "VERIFIED"
    }
]

def get_seoc_for_state(state_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves the official State Emergency Operations Centre for any given state."""
    normalized = state_name.strip().lower()
    for h in ALL_INDIA_SEOC_HUBS:
        if h["state_name"].lower() == normalized:
            return h
    # Fuzzy fallback for abbreviations or partial matches
    for h in ALL_INDIA_SEOC_HUBS:
        if normalized in h["state_name"].lower() or h["state_name"].lower() in normalized:
            return h
    return None

# Default Active State Hub (Tamil Nadu SEOC - dynamic, replaces hardcoded CEOH)
CENTRAL_DEPOT = ALL_INDIA_SEOC_HUBS[22]  # Tamil Nadu SEOC

DEFAULT_DISASTER = {
    "id": 1,
    "name": "Cyclone Michaung & Coastal Flood Surge",
    "type": "Flood",  # Flood, Earthquake, Cyclone, Landslide
    "state_name": "Tamil Nadu",
    "declaration_date": "2026-11-01",
    "status": "Active Response",
    "description": "Severe cyclonic surge and heavy monsoon rainfall triggering widespread urban and deltaic inundation across Tamil Nadu."
}

DEFAULT_REGIONS = [
    {
        "id": 1,
        "state_name": "Tamil Nadu",
        "district": "Chennai",
        "name": "Chennai Marina & Foreshore Basin",
        "latitude": 13.0480,
        "longitude": 80.2780,
        "population": 28500,
        "severity": 4.8,
        "accessibility_score": 0.35,
        "road_condition": "Flooded / 4x4 & Boats Only",
        "distance_km": 4.5,
        "travel_time_hours": 0.8,
        "water_demand": 35000,
        "food_demand": 18000,
        "med_demand": 2400,
        "vehicle_demand": 6,
        "team_demand": 7,
        "shelter_demand": 450,
        "critical_priority": "Critical"
    },
    {
        "id": 2,
        "state_name": "Tamil Nadu",
        "district": "Chennai",
        "name": "Tambaram - Mudichur Lowlands",
        "latitude": 12.9249,
        "longitude": 80.1000,
        "population": 19500,
        "severity": 4.6,
        "accessibility_score": 0.30,
        "road_condition": "Waterlogged Highway / Detour",
        "distance_km": 26.0,
        "travel_time_hours": 1.6,
        "water_demand": 24000,
        "food_demand": 12500,
        "med_demand": 1600,
        "vehicle_demand": 4,
        "team_demand": 5,
        "shelter_demand": 320,
        "critical_priority": "High"
    },
    {
        "id": 3,
        "state_name": "Tamil Nadu",
        "district": "Cuddalore",
        "name": "Cuddalore Gadilam Delta Enclave",
        "latitude": 11.7480,
        "longitude": 79.7714,
        "population": 22000,
        "severity": 5.0,
        "accessibility_score": 0.20,
        "road_condition": "Submerged Embankment / Boats Only",
        "distance_km": 165.0,
        "travel_time_hours": 3.8,
        "water_demand": 32000,
        "food_demand": 16000,
        "med_demand": 2200,
        "vehicle_demand": 6,
        "team_demand": 6,
        "shelter_demand": 400,
        "critical_priority": "Critical"
    },
    {
        "id": 4,
        "state_name": "Tamil Nadu",
        "district": "Nagapattinam",
        "name": "Nagapattinam Coastal Fishery Ward",
        "latitude": 10.7672,
        "longitude": 79.8449,
        "population": 16000,
        "severity": 4.3,
        "accessibility_score": 0.40,
        "road_condition": "Seawater Intrusion / Damaged Bridge",
        "distance_km": 285.0,
        "travel_time_hours": 5.5,
        "water_demand": 21000,
        "food_demand": 11000,
        "med_demand": 1400,
        "vehicle_demand": 4,
        "team_demand": 4,
        "shelter_demand": 260,
        "critical_priority": "High"
    },
    {
        "id": 5,
        "state_name": "Tamil Nadu",
        "district": "Thoothukudi",
        "name": "Thoothukudi Saltpan Harbor Colony",
        "latitude": 8.7642,
        "longitude": 78.1348,
        "population": 14000,
        "severity": 4.7,
        "accessibility_score": 0.25,
        "road_condition": "Inundated Railway Subway",
        "distance_km": 560.0,
        "travel_time_hours": 9.2,
        "water_demand": 20000,
        "food_demand": 10000,
        "med_demand": 1500,
        "vehicle_demand": 5,
        "team_demand": 5,
        "shelter_demand": 280,
        "critical_priority": "Critical"
    },
    {
        "id": 6,
        "state_name": "Tamil Nadu",
        "district": "Tiruvallur",
        "name": "Tiruvallur Kosasthalaiyar Overflow",
        "latitude": 13.1432,
        "longitude": 79.9076,
        "population": 12500,
        "severity": 3.8,
        "accessibility_score": 0.55,
        "road_condition": "Partially Flooded Rural Arterial",
        "distance_km": 48.0,
        "travel_time_hours": 1.5,
        "water_demand": 15000,
        "food_demand": 7500,
        "med_demand": 900,
        "vehicle_demand": 3,
        "team_demand": 3,
        "shelter_demand": 180,
        "critical_priority": "Medium"
    },
    {
        "id": 7,
        "state_name": "Tamil Nadu",
        "district": "Kanchipuram",
        "name": "Kanchipuram Palar Basin Ward",
        "latitude": 12.8342,
        "longitude": 79.7036,
        "population": 15000,
        "severity": 3.5,
        "accessibility_score": 0.65,
        "road_condition": "Paved Road Open with Minor Debris",
        "distance_km": 74.0,
        "travel_time_hours": 1.8,
        "water_demand": 18000,
        "food_demand": 9000,
        "med_demand": 1100,
        "vehicle_demand": 3,
        "team_demand": 3,
        "shelter_demand": 210,
        "critical_priority": "Medium"
    },
    {
        "id": 8,
        "state_name": "Tamil Nadu",
        "district": "Chengalpattu",
        "name": "Chengalpattu Lake Overflow Belt",
        "latitude": 12.6819,
        "longitude": 79.9888,
        "population": 11000,
        "severity": 3.2,
        "accessibility_score": 0.70,
        "road_condition": "Waterlogged Shoulders",
        "distance_km": 60.0,
        "travel_time_hours": 1.4,
        "water_demand": 13000,
        "food_demand": 6500,
        "med_demand": 800,
        "vehicle_demand": 2,
        "team_demand": 2,
        "shelter_demand": 150,
        "critical_priority": "Medium"
    },
    {
        "id": 9,
        "state_name": "Tamil Nadu",
        "district": "Villupuram",
        "name": "Villupuram Lowland Agricultural Strip",
        "latitude": 11.9401,
        "longitude": 79.4861,
        "population": 8500,
        "severity": 2.8,
        "accessibility_score": 0.80,
        "road_condition": "Clear Highway Access",
        "distance_km": 145.0,
        "travel_time_hours": 2.8,
        "water_demand": 9500,
        "food_demand": 4800,
        "med_demand": 600,
        "vehicle_demand": 2,
        "team_demand": 2,
        "shelter_demand": 110,
        "critical_priority": "Low"
    },
    {
        "id": 10,
        "state_name": "Tamil Nadu",
        "district": "Mayiladuthurai",
        "name": "Poompuhar Coastal Estuary Village",
        "latitude": 11.1460,
        "longitude": 79.8510,
        "population": 9200,
        "severity": 4.1,
        "accessibility_score": 0.45,
        "road_condition": "Breached Canal Road",
        "distance_km": 250.0,
        "travel_time_hours": 4.8,
        "water_demand": 12000,
        "food_demand": 6200,
        "med_demand": 800,
        "vehicle_demand": 3,
        "team_demand": 3,
        "shelter_demand": 140,
        "critical_priority": "High"
    }
]

DEFAULT_RESOURCES = [
    {
        "id": 1,
        "name": "Clean Drinking Water",
        "type": "Divisible",
        "unit": "Liters",
        "total_available": 140000,
        "unit_cost": 0.85,
        "unit_weight_kg": 1.0,
        "priority_weight": 1.5,
        "description": "Purified 20L canisters and emergency drinking water sachets."
    },
    {
        "id": 2,
        "name": "Ready-to-Eat Food Packets",
        "type": "Divisible",
        "unit": "Packets",
        "total_available": 70000,
        "unit_cost": 2.50,
        "unit_weight_kg": 0.6,
        "priority_weight": 1.3,
        "description": "High-calorie survival rations and instant meal packages."
    },
    {
        "id": 3,
        "name": "Emergency Medical Kits",
        "type": "Divisible",
        "unit": "Kits",
        "total_available": 8500,
        "unit_cost": 15.00,
        "unit_weight_kg": 2.2,
        "priority_weight": 2.0,
        "description": "First-aid trauma packs, antibiotics, anti-venom, water purification tabs."
    },
    {
        "id": 4,
        "name": "Temporary Emergency Shelters",
        "type": "Indivisible",
        "unit": "Tents",
        "total_available": 1600,
        "unit_cost": 120.00,
        "unit_weight_kg": 15.0,
        "priority_weight": 1.2,
        "description": "Weatherproof all-season family relief tents with tarpaulins."
    }
]

DEFAULT_VEHICLES = [
    {
        "id": 1,
        "type": "4x4 Heavy Relief Truck",
        "total_available": 14,
        "cargo_capacity_kg": 4000,
        "speed_kmh": 45,
        "cost_per_km": 3.5,
        "can_handle_rough_terrain": 1,
        "can_handle_waterlogged": 0
    },
    {
        "id": 2,
        "type": "Inflatable Rescue Boat & Trailer",
        "total_available": 8,
        "cargo_capacity_kg": 1200,
        "speed_kmh": 25,
        "cost_per_km": 5.0,
        "can_handle_rough_terrain": 0,
        "can_handle_waterlogged": 1
    },
    {
        "id": 3,
        "type": "Emergency Paramedic Ambulance",
        "total_available": 10,
        "cargo_capacity_kg": 800,
        "speed_kmh": 60,
        "cost_per_km": 2.8,
        "can_handle_rough_terrain": 0,
        "can_handle_waterlogged": 0
    }
]

DEFAULT_TEAMS = [
    {
        "id": 1,
        "type": "Search and Rescue (SAR) Squad",
        "total_available": 12,
        "personnel_per_team": 6,
        "specialization": "Swift water and coastal flood extrication",
        "daily_cost": 650.0
    },
    {
        "id": 2,
        "type": "Emergency Medical Response Unit",
        "total_available": 10,
        "personnel_per_team": 4,
        "specialization": "Field triage, surgery, and stabilization",
        "daily_cost": 900.0
    },
    {
        "id": 3,
        "type": "Logistics & Shelter Deployment Crew",
        "total_available": 10,
        "personnel_per_team": 8,
        "specialization": "Shelter erection, food distribution, crowd control",
        "daily_cost": 450.0
    }
]

# -------------------------------------------------------------------------------------------------
# MULTI-HAZARD & STATE-WISE DISASTER CATALOG
# Demonstrates automatic SEOC selection, multi-state disaster coordination, and unverified handling.
# -------------------------------------------------------------------------------------------------

SCENARIOS_CATALOG: Dict[str, Dict[str, Any]] = {
    # 1. TAMIL NADU FLOOD (Tamil Nadu SEOC)
    "Tamil Nadu Flood & Coastal Surge": {
        "disaster": DEFAULT_DISASTER,
        "hub": ALL_INDIA_SEOC_HUBS[22], # TN SEOC, Chennai
        "regions": DEFAULT_REGIONS,
        "resources": DEFAULT_RESOURCES,
        "vehicles": DEFAULT_VEHICLES,
        "teams": DEFAULT_TEAMS
    },

    # 2. ODISHA CYCLONE (Odisha SEOC - OSDMA Bhubaneswar)
    "Odisha Cyclone Dana (Bay of Bengal)": {
        "disaster": {
            "id": 2,
            "name": "Severe Cyclonic Storm Dana Landfall",
            "type": "Cyclone",
            "state_name": "Odisha",
            "declaration_date": "2026-10-24",
            "status": "Red Alert",
            "description": "Extremely severe cyclonic storm with 130 km/h gusts causing storm surges and coastal breaches across Odisha."
        },
        "hub": ALL_INDIA_SEOC_HUBS[18], # Odisha SEOC, Bhubaneswar
        "regions": [
            {
                "id": 1, "state_name": "Odisha", "district": "Puri",
                "name": "Puri Jagannath Shoreline Sector", "latitude": 19.8135, "longitude": 85.8312,
                "population": 26000, "severity": 4.9, "accessibility_score": 0.25,
                "road_condition": "Storm Surge Inundation / Fallen Trees", "distance_km": 62.0, "travel_time_hours": 2.1,
                "water_demand": 38000, "food_demand": 19000, "med_demand": 2600, "vehicle_demand": 6, "team_demand": 7, "shelter_demand": 480,
                "critical_priority": "Critical"
            },
            {
                "id": 2, "state_name": "Odisha", "district": "Jagatsinghpur",
                "name": "Paradip Port Logistics Ward", "latitude": 20.3164, "longitude": 86.6111,
                "population": 22500, "severity": 5.0, "accessibility_score": 0.20,
                "road_condition": "High Tide Breach / 4x4 & Boats", "distance_km": 98.0, "travel_time_hours": 2.9,
                "water_demand": 34000, "food_demand": 17500, "med_demand": 2400, "vehicle_demand": 6, "team_demand": 6, "shelter_demand": 420,
                "critical_priority": "Critical"
            },
            {
                "id": 3, "state_name": "Odisha", "district": "Balasore",
                "name": "Chandipur Seafront Enclave", "latitude": 21.4934, "longitude": 86.9135,
                "population": 18000, "severity": 4.4, "accessibility_score": 0.40,
                "road_condition": "Coastal Highway Waterlogged", "distance_km": 195.0, "travel_time_hours": 4.2,
                "water_demand": 24000, "food_demand": 12000, "med_demand": 1500, "vehicle_demand": 4, "team_demand": 4, "shelter_demand": 260,
                "critical_priority": "High"
            },
            {
                "id": 4, "state_name": "Odisha", "district": "Kendrapara",
                "name": "Bhitarkanika Mangrove Boundary", "latitude": 20.5284, "longitude": 86.7228,
                "population": 14500, "severity": 4.7, "accessibility_score": 0.20,
                "road_condition": "Tidal Influx / Boats Only", "distance_km": 115.0, "travel_time_hours": 3.6,
                "water_demand": 22000, "food_demand": 11000, "med_demand": 1600, "vehicle_demand": 4, "team_demand": 5, "shelter_demand": 300,
                "critical_priority": "Critical"
            },
            {
                "id": 5, "state_name": "Odisha", "district": "Ganjam",
                "name": "Gopalpur Seacoast Village", "latitude": 19.2612, "longitude": 84.9084,
                "population": 13500, "severity": 3.9, "accessibility_score": 0.55,
                "road_condition": "Cleared National Highway", "distance_km": 165.0, "travel_time_hours": 3.2,
                "water_demand": 17000, "food_demand": 8500, "med_demand": 1100, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 200,
                "critical_priority": "High"
            },
            {
                "id": 6, "state_name": "Odisha", "district": "Bhadrak",
                "name": "Dhamra Port Fishery Base", "latitude": 20.7960, "longitude": 86.8480,
                "population": 15000, "severity": 4.2, "accessibility_score": 0.35,
                "road_condition": "Submerged Embankment", "distance_km": 142.0, "travel_time_hours": 3.5,
                "water_demand": 20000, "food_demand": 10000, "med_demand": 1300, "vehicle_demand": 3, "team_demand": 4, "shelter_demand": 240,
                "critical_priority": "High"
            }
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 115000, "unit_cost": 0.85, "unit_weight_kg": 1.0, "priority_weight": 1.5, "description": "Chlorinated bulk containers"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 58000, "unit_cost": 2.50, "unit_weight_kg": 0.6, "priority_weight": 1.4, "description": "Dry food & flattened rice chuda packs"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 7200, "unit_cost": 16.00, "unit_weight_kg": 2.2, "priority_weight": 2.0, "description": "Waterborne anti-cholera packs"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 1300, "unit_cost": 125.00, "unit_weight_kg": 15.0, "priority_weight": 1.3, "description": "Cyclone shelter tarpaulins"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 12, "cargo_capacity_kg": 4000, "speed_kmh": 40, "cost_per_km": 3.6, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 10, "cargo_capacity_kg": 1200, "speed_kmh": 22, "cost_per_km": 5.2, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 8, "cargo_capacity_kg": 800, "speed_kmh": 55, "cost_per_km": 2.9, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 14, "personnel_per_team": 6, "specialization": "ODRAF / NDRF coastal breach rescue", "daily_cost": 700.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 9, "personnel_per_team": 4, "specialization": "Mobile trauma & disease prevention", "daily_cost": 900.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 8, "personnel_per_team": 8, "specialization": "Cyclone shelter distribution", "daily_cost": 450.0}
        ]
    },

    # 3. KERALA LANDSLIDE (Kerala SEOC - Thiruvananthapuram)
    "Kerala Cloudburst & Wayanad Landslides": {
        "disaster": {
            "id": 3,
            "name": "Wayanad Cloudburst & Debris Flow Landslides",
            "type": "Landslide",
            "state_name": "Kerala",
            "declaration_date": "2026-10-28",
            "status": "State of Disaster",
            "description": "Massive catastrophic hill slope failures and mudflows sweeping through Chooralmala and Meppadi valleys in Wayanad."
        },
        "hub": ALL_INDIA_SEOC_HUBS[11], # Kerala SEOC, Thiruvananthapuram
        "regions": [
            {
                "id": 1, "state_name": "Kerala", "district": "Wayanad",
                "name": "Chooralmala Valley Sector", "latitude": 11.5360, "longitude": 76.1680,
                "population": 7200, "severity": 5.0, "accessibility_score": 0.15,
                "road_condition": "Bridge Collapsed / Bailey Bridge Only", "distance_km": 425.0, "travel_time_hours": 8.5,
                "water_demand": 14000, "food_demand": 8000, "med_demand": 1600, "vehicle_demand": 4, "team_demand": 6, "shelter_demand": 280,
                "critical_priority": "Critical"
            },
            {
                "id": 2, "state_name": "Kerala", "district": "Wayanad",
                "name": "Meppadi Tea Estate Ward", "latitude": 11.5510, "longitude": 76.1260,
                "population": 6500, "severity": 4.8, "accessibility_score": 0.25,
                "road_condition": "Mud Debris / 4x4 Only", "distance_km": 418.0, "travel_time_hours": 8.1,
                "water_demand": 12000, "food_demand": 7200, "med_demand": 1400, "vehicle_demand": 3, "team_demand": 5, "shelter_demand": 240,
                "critical_priority": "Critical"
            },
            {
                "id": 3, "state_name": "Kerala", "district": "Wayanad",
                "name": "Mundakkai Isolated Hamlet", "latitude": 11.5420, "longitude": 76.1820,
                "population": 4200, "severity": 5.0, "accessibility_score": 0.10,
                "road_condition": "Impassable / Zipline & Air Drops", "distance_km": 430.0, "travel_time_hours": 9.2,
                "water_demand": 9500, "food_demand": 5500, "med_demand": 1200, "vehicle_demand": 3, "team_demand": 5, "shelter_demand": 200,
                "critical_priority": "Critical"
            },
            {
                "id": 4, "state_name": "Kerala", "district": "Idukki",
                "name": "Munnar Gap Road Settlement", "latitude": 10.0889, "longitude": 77.0595,
                "population": 8800, "severity": 4.2, "accessibility_score": 0.35,
                "road_condition": "Rockfall Hazard / Light Vehicles", "distance_km": 240.0, "travel_time_hours": 5.2,
                "water_demand": 15000, "food_demand": 8200, "med_demand": 1100, "vehicle_demand": 3, "team_demand": 4, "shelter_demand": 220,
                "critical_priority": "High"
            },
            {
                "id": 5, "state_name": "Kerala", "district": "Kozhikode",
                "name": "Vilangad River Foothills", "latitude": 11.7100, "longitude": 75.8200,
                "population": 5800, "severity": 4.3, "accessibility_score": 0.30,
                "road_condition": "Road Eroded / Single Lane", "distance_km": 395.0, "travel_time_hours": 7.8,
                "water_demand": 11000, "food_demand": 6000, "med_demand": 850, "vehicle_demand": 2, "team_demand": 3, "shelter_demand": 160,
                "critical_priority": "High"
            },
            {
                "id": 6, "state_name": "Kerala", "district": "Ernakulam",
                "name": "Aluva Periyar Inundation Strip", "latitude": 10.1076, "longitude": 76.3516,
                "population": 16500, "severity": 3.6, "accessibility_score": 0.65,
                "road_condition": "Receding Flood Waters", "distance_km": 195.0, "travel_time_hours": 3.8,
                "water_demand": 22000, "food_demand": 11000, "med_demand": 1300, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 250,
                "critical_priority": "Medium"
            }
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 60000, "unit_cost": 0.90, "unit_weight_kg": 1.0, "priority_weight": 1.5, "description": "Highland canister packs"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 32000, "unit_cost": 2.80, "unit_weight_kg": 0.6, "priority_weight": 1.4, "description": "High-calorie survival rations"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 5200, "unit_cost": 18.00, "unit_weight_kg": 2.2, "priority_weight": 2.2, "description": "Crush trauma & alpine injury kits"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 950, "unit_cost": 135.00, "unit_weight_kg": 15.0, "priority_weight": 1.4, "description": "Waterproof terrain tents"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 8, "cargo_capacity_kg": 3500, "speed_kmh": 35, "cost_per_km": 4.0, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 3, "cargo_capacity_kg": 1000, "speed_kmh": 20, "cost_per_km": 5.5, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 7, "cargo_capacity_kg": 750, "speed_kmh": 45, "cost_per_km": 3.0, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 10, "personnel_per_team": 6, "specialization": "Mountain mud search & canine teams", "daily_cost": 750.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 8, "personnel_per_team": 4, "specialization": "Field amputation & critical resuscitation", "daily_cost": 950.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 6, "personnel_per_team": 6, "specialization": "Terrain camp erection", "daily_cost": 450.0}
        ]
    },

    # 4. GUJARAT EARTHQUAKE (Gujarat SEOC - GSDMA Gandhinagar)
    "Gujarat Kutch Fault Earthquake (M 7.1)": {
        "disaster": {
            "id": 4,
            "name": "Kutch Rift Fault Crustal Earthquake (M 7.1)",
            "type": "Earthquake",
            "state_name": "Gujarat",
            "declaration_date": "2026-10-29",
            "status": "State Disaster Emergency",
            "description": "Severe shallow crustal rupture along the Kutch Mainland Fault triggering extensive masonry collapse and structural damage."
        },
        "hub": ALL_INDIA_SEOC_HUBS[6], # Gujarat SEOC, Gandhinagar
        "regions": [
            {
                "id": 1, "state_name": "Gujarat", "district": "Kutch",
                "name": "Bhuj Historic Walled City", "latitude": 23.2420, "longitude": 69.6669,
                "population": 29000, "severity": 5.0, "accessibility_score": 0.20,
                "road_condition": "Rubble Blocked / Gas Line Fractures", "distance_km": 315.0, "travel_time_hours": 6.2,
                "water_demand": 42000, "food_demand": 22000, "med_demand": 3400, "vehicle_demand": 7, "team_demand": 8, "shelter_demand": 550,
                "critical_priority": "Critical"
            },
            {
                "id": 2, "state_name": "Gujarat", "district": "Kutch",
                "name": "Anjar Industrial Settlement", "latitude": 23.1140, "longitude": 70.0270,
                "population": 21000, "severity": 4.8, "accessibility_score": 0.30,
                "road_condition": "Fissures Across Highway", "distance_km": 290.0, "travel_time_hours": 5.5,
                "water_demand": 32000, "food_demand": 16000, "med_demand": 2500, "vehicle_demand": 5, "team_demand": 6, "shelter_demand": 420,
                "critical_priority": "Critical"
            },
            {
                "id": 3, "state_name": "Gujarat", "district": "Kutch",
                "name": "Gandhidham Cargo Terminal", "latitude": 23.0753, "longitude": 70.1337,
                "population": 24000, "severity": 4.3, "accessibility_score": 0.45,
                "road_condition": "Liquefaction Near Port Roads", "distance_km": 280.0, "travel_time_hours": 5.1,
                "water_demand": 35000, "food_demand": 17000, "med_demand": 2200, "vehicle_demand": 5, "team_demand": 5, "shelter_demand": 400,
                "critical_priority": "High"
            },
            {
                "id": 4, "state_name": "Gujarat", "district": "Morbi",
                "name": "Morbi Ceramic Hub Sector", "latitude": 22.8120, "longitude": 70.8380,
                "population": 18000, "severity": 4.1, "accessibility_score": 0.50,
                "road_condition": "Bridge Joint Dislocation", "distance_km": 190.0, "travel_time_hours": 3.4,
                "water_demand": 25000, "food_demand": 12500, "med_demand": 1800, "vehicle_demand": 4, "team_demand": 4, "shelter_demand": 300,
                "critical_priority": "High"
            },
            {
                "id": 5, "state_name": "Gujarat", "district": "Rajkot",
                "name": "Rajkot Ring Road Suburb", "latitude": 22.3039, "longitude": 70.8022,
                "population": 20000, "severity": 3.4, "accessibility_score": 0.75,
                "road_condition": "Clear Six-Lane Highway", "distance_km": 215.0, "travel_time_hours": 3.6,
                "water_demand": 26000, "food_demand": 13000, "med_demand": 1500, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 280,
                "critical_priority": "Medium"
            },
            {
                "id": 6, "state_name": "Gujarat", "district": "Jamnagar",
                "name": "Jamnagar Refinery Colony", "latitude": 22.4707, "longitude": 70.0577,
                "population": 15000, "severity": 3.7, "accessibility_score": 0.60,
                "road_condition": "Surface Cracks Cleared", "distance_km": 295.0, "travel_time_hours": 5.0,
                "water_demand": 21000, "food_demand": 10500, "med_demand": 1400, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 220,
                "critical_priority": "Medium"
            }
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 130000, "unit_cost": 0.85, "unit_weight_kg": 1.0, "priority_weight": 1.5, "description": "Water bowsers and sachets"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 65000, "unit_cost": 2.50, "unit_weight_kg": 0.6, "priority_weight": 1.3, "description": "Survival dry rations & energy bars"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 9000, "unit_cost": 17.00, "unit_weight_kg": 2.2, "priority_weight": 2.4, "description": "Orthopedic & trauma surgery packs"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 1500, "unit_cost": 130.00, "unit_weight_kg": 15.0, "priority_weight": 1.4, "description": "Rapid earthquake family shelters"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 15, "cargo_capacity_kg": 4000, "speed_kmh": 45, "cost_per_km": 3.5, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 2, "cargo_capacity_kg": 1000, "speed_kmh": 20, "cost_per_km": 5.0, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 12, "cargo_capacity_kg": 800, "speed_kmh": 60, "cost_per_km": 2.8, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 16, "personnel_per_team": 6, "specialization": "Collapsed building acoustic search & heavy concrete cutting", "daily_cost": 750.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 12, "personnel_per_team": 4, "specialization": "Crush injury & blood transfusion", "daily_cost": 950.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 9, "personnel_per_team": 8, "specialization": "Earthquake refugee camp management", "daily_cost": 450.0}
        ]
    },

    # 5. SIMULTANEOUS MULTI-STATE DISASTER (Tamil Nadu & Kerala)
    "South India Dual-State Flood (Tamil Nadu & Kerala)": {
        "disaster": {
            "id": 5,
            "name": "South India Dual-State Monsoon Crisis (Tamil Nadu & Kerala)",
            "type": "Flood",
            "state_name": "Tamil Nadu, Kerala",
            "declaration_date": "2026-11-02",
            "status": "Joint Emergency",
            "description": "Simultaneous cyclonic downpour and Western Ghats cloudburst triggering concurrent severe flooding across Tamil Nadu and Kerala."
        },
        "hubs": [
            ALL_INDIA_SEOC_HUBS[22], # Tamil Nadu SEOC, Chennai
            ALL_INDIA_SEOC_HUBS[11]  # Kerala SEOC, Thiruvananthapuram
        ],
        "hub": ALL_INDIA_SEOC_HUBS[22], # Primary coordinator
        "regions": [
            # Tamil Nadu Regions (5)
            {
                "id": 1, "state_name": "Tamil Nadu", "district": "Chennai",
                "name": "Chennai Adyar Basin", "latitude": 13.0012, "longitude": 80.2565,
                "population": 30000, "severity": 4.8, "accessibility_score": 0.35,
                "road_condition": "Flooded Arterial / Boats", "distance_km": 7.0, "travel_time_hours": 0.9,
                "water_demand": 38000, "food_demand": 19000, "med_demand": 2500, "vehicle_demand": 5, "team_demand": 6, "shelter_demand": 450,
                "critical_priority": "Critical"
            },
            {
                "id": 2, "state_name": "Tamil Nadu", "district": "Cuddalore",
                "name": "Cuddalore Coastal Reach", "latitude": 11.7500, "longitude": 79.7600,
                "population": 21000, "severity": 4.9, "accessibility_score": 0.20,
                "road_condition": "Submerged Embankment", "distance_km": 165.0, "travel_time_hours": 3.8,
                "water_demand": 30000, "food_demand": 15000, "med_demand": 2000, "vehicle_demand": 5, "team_demand": 5, "shelter_demand": 380,
                "critical_priority": "Critical"
            },
            {
                "id": 3, "state_name": "Tamil Nadu", "district": "Thoothukudi",
                "name": "Thoothukudi Harbor Ward", "latitude": 8.7800, "longitude": 78.1400,
                "population": 16000, "severity": 4.5, "accessibility_score": 0.30,
                "road_condition": "Waterlogged Rail Underpass", "distance_km": 560.0, "travel_time_hours": 9.2,
                "water_demand": 22000, "food_demand": 11000, "med_demand": 1500, "vehicle_demand": 4, "team_demand": 4, "shelter_demand": 280,
                "critical_priority": "High"
            },
            {
                "id": 4, "state_name": "Tamil Nadu", "district": "Kanchipuram",
                "name": "Kanchipuram Temple Lowlands", "latitude": 12.8300, "longitude": 79.7000,
                "population": 14000, "severity": 3.5, "accessibility_score": 0.65,
                "road_condition": "Highway Open / Minor Water", "distance_km": 72.0, "travel_time_hours": 1.7,
                "water_demand": 17000, "food_demand": 8500, "med_demand": 1000, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 200,
                "critical_priority": "Medium"
            },
            {
                "id": 5, "state_name": "Tamil Nadu", "district": "Tiruvallur",
                "name": "Tiruvallur Reservoir Delta", "latitude": 13.1400, "longitude": 79.9100,
                "population": 12000, "severity": 3.8, "accessibility_score": 0.50,
                "road_condition": "Canal Overflow", "distance_km": 46.0, "travel_time_hours": 1.4,
                "water_demand": 15000, "food_demand": 7500, "med_demand": 900, "vehicle_demand": 2, "team_demand": 3, "shelter_demand": 170,
                "critical_priority": "Medium"
            },
            # Kerala Regions (5)
            {
                "id": 6, "state_name": "Kerala", "district": "Wayanad",
                "name": "Wayanad Chooralmala Inundation", "latitude": 11.5360, "longitude": 76.1680,
                "population": 8000, "severity": 5.0, "accessibility_score": 0.15,
                "road_condition": "Mud Debris / 4x4 & Bailey Bridge", "distance_km": 425.0, "travel_time_hours": 8.5,
                "water_demand": 15000, "food_demand": 8500, "med_demand": 1700, "vehicle_demand": 4, "team_demand": 5, "shelter_demand": 290,
                "critical_priority": "Critical"
            },
            {
                "id": 7, "state_name": "Kerala", "district": "Idukki",
                "name": "Idukki Dam Catchment Hamlet", "latitude": 9.8500, "longitude": 76.9700,
                "population": 9500, "severity": 4.6, "accessibility_score": 0.25,
                "road_condition": "Landslide Threat / Single Lane", "distance_km": 180.0, "travel_time_hours": 4.2,
                "water_demand": 16000, "food_demand": 9000, "med_demand": 1300, "vehicle_demand": 3, "team_demand": 4, "shelter_demand": 240,
                "critical_priority": "High"
            },
            {
                "id": 8, "state_name": "Kerala", "district": "Ernakulam",
                "name": "Aluva Periyar Bank Ward", "latitude": 10.1100, "longitude": 76.3500,
                "population": 17000, "severity": 4.4, "accessibility_score": 0.45,
                "road_condition": "Waterlogged Paved Streets", "distance_km": 200.0, "travel_time_hours": 4.0,
                "water_demand": 24000, "food_demand": 12000, "med_demand": 1500, "vehicle_demand": 4, "team_demand": 4, "shelter_demand": 280,
                "critical_priority": "High"
            },
            {
                "id": 9, "state_name": "Kerala", "district": "Kozhikode",
                "name": "Kozhikode Chaliyar Floodplain", "latitude": 11.2500, "longitude": 75.8300,
                "population": 13500, "severity": 3.9, "accessibility_score": 0.55,
                "road_condition": "River Overflow / Detour", "distance_km": 370.0, "travel_time_hours": 7.2,
                "water_demand": 18000, "food_demand": 9000, "med_demand": 1100, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 200,
                "critical_priority": "Medium"
            },
            {
                "id": 10, "state_name": "Kerala", "district": "Alappuzha",
                "name": "Kuttanad Waterlogged Polder", "latitude": 9.4981, "longitude": 76.3388,
                "population": 15000, "severity": 4.7, "accessibility_score": 0.20,
                "road_condition": "Submerged Below Sea-Level / Boats", "distance_km": 150.0, "travel_time_hours": 3.5,
                "water_demand": 23000, "food_demand": 11500, "med_demand": 1600, "vehicle_demand": 4, "team_demand": 4, "shelter_demand": 270,
                "critical_priority": "Critical"
            }
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 160000, "unit_cost": 0.85, "unit_weight_kg": 1.0, "priority_weight": 1.5, "description": "Combined inter-state clean water reserve"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 80000, "unit_cost": 2.50, "unit_weight_kg": 0.6, "priority_weight": 1.3, "description": "Consolidated emergency rations"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 10500, "unit_cost": 15.00, "unit_weight_kg": 2.2, "priority_weight": 2.1, "description": "Multi-state medical stockpile"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 1900, "unit_cost": 120.00, "unit_weight_kg": 15.0, "priority_weight": 1.3, "description": "Rapid deploy shelters"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 18, "cargo_capacity_kg": 4000, "speed_kmh": 45, "cost_per_km": 3.5, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 14, "cargo_capacity_kg": 1200, "speed_kmh": 25, "cost_per_km": 5.0, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 14, "cargo_capacity_kg": 800, "speed_kmh": 60, "cost_per_km": 2.8, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 18, "personnel_per_team": 6, "specialization": "Inter-state NDRF & SDRF joint operations", "daily_cost": 700.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 14, "personnel_per_team": 4, "specialization": "Dual-state mobile triage squads", "daily_cost": 900.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 12, "personnel_per_team": 8, "specialization": "Inter-state supply corridor management", "daily_cost": 450.0}
        ]
    },

    # 6. UNVERIFIED SEOC SCENARIO (Lakshadweep)
    "Lakshadweep Archipelago Cyclone (Unverified SEOC)": {
        "disaster": {
            "id": 6,
            "name": "Lakshadweep Deep Depression & Marine Storm Surge",
            "type": "Cyclone",
            "state_name": "Lakshadweep",
            "declaration_date": "2026-11-03",
            "status": "Warning Alert",
            "description": "Marine gale force winds and high swell waves threatening remote island coral atolls."
        },
        "hub": ALL_INDIA_SEOC_HUBS[34], # Lakshadweep (UNVERIFIED)
        "regions": [
            {
                "id": 1, "state_name": "Lakshadweep", "district": "Kavaratti",
                "name": "Kavaratti Island Coastal Ward", "latitude": 10.5667, "longitude": 72.6369,
                "population": 11000, "severity": 4.6, "accessibility_score": 0.20,
                "road_condition": "Island Jetty Flooded / Marine Craft", "distance_km": 5.0, "travel_time_hours": 0.8,
                "water_demand": 16000, "food_demand": 8500, "med_demand": 1200, "vehicle_demand": 2, "team_demand": 3, "shelter_demand": 180,
                "critical_priority": "Critical"
            },
            {
                "id": 2, "state_name": "Lakshadweep", "district": "Agatti",
                "name": "Agatti Airstrip & Lagoon Ward", "latitude": 10.8533, "longitude": 72.1932,
                "population": 7500, "severity": 4.3, "accessibility_score": 0.30,
                "road_condition": "Runway Coral Debris", "distance_km": 60.0, "travel_time_hours": 2.5,
                "water_demand": 11000, "food_demand": 6000, "med_demand": 900, "vehicle_demand": 2, "team_demand": 2, "shelter_demand": 140,
                "critical_priority": "High"
            },
            {
                "id": 3, "state_name": "Lakshadweep", "district": "Andrott",
                "name": "Andrott Eastern Reef Settlement", "latitude": 10.8250, "longitude": 73.6800,
                "population": 9800, "severity": 4.7, "accessibility_score": 0.15,
                "road_condition": "Severe Surge / Boat Only", "distance_km": 120.0, "travel_time_hours": 4.5,
                "water_demand": 15000, "food_demand": 7500, "med_demand": 1100, "vehicle_demand": 2, "team_demand": 3, "shelter_demand": 170,
                "critical_priority": "Critical"
            }
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 30000, "unit_cost": 1.20, "unit_weight_kg": 1.0, "priority_weight": 1.6, "description": "Desalination stockpiles"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 16000, "unit_cost": 3.00, "unit_weight_kg": 0.6, "priority_weight": 1.4, "description": "Shelf-stable marine rations"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 2200, "unit_cost": 20.00, "unit_weight_kg": 2.2, "priority_weight": 2.2, "description": "Island primary health trauma packs"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 380, "unit_cost": 140.00, "unit_weight_kg": 15.0, "priority_weight": 1.3, "description": "Windproof shelters"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 3, "cargo_capacity_kg": 3000, "speed_kmh": 30, "cost_per_km": 4.5, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 6, "cargo_capacity_kg": 1200, "speed_kmh": 25, "cost_per_km": 6.0, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 2, "cargo_capacity_kg": 600, "speed_kmh": 40, "cost_per_km": 3.5, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 4, "personnel_per_team": 6, "specialization": "Island marine boat SAR", "daily_cost": 750.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 3, "personnel_per_team": 4, "specialization": "Lagoon triage & paramedic support", "daily_cost": 900.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 3, "personnel_per_team": 6, "specialization": "Atoll supply distribution", "daily_cost": 450.0}
        ]
    },

    # 7. DELHI NCT (Delhi SEOC)
    "Delhi-NCR Monsoon Overflow 2026": {
        "disaster": {
            "id": 7,
            "name": "Delhi-NCR Yamuna Monsoon River Overflow",
            "type": "Flood",
            "state_name": "Delhi",
            "declaration_date": "2026-10-20",
            "status": "Monitored",
            "description": "Monsoon discharge from Hathnikund barrage causing Yamuna riverbank overflow across Delhi NCR."
        },
        "hub": ALL_INDIA_SEOC_HUBS[31], # Delhi SEOC, Sham Nath Marg
        "regions": [
            {"id": 1, "state_name": "Delhi", "district": "North Delhi", "name": "Yamuna Bazaar Civil Lines", "latitude": 28.6650, "longitude": 77.2350, "population": 18000, "severity": 4.6, "accessibility_score": 0.40, "road_condition": "Flooded Ring Road", "distance_km": 2.5, "travel_time_hours": 0.4, "water_demand": 24000, "food_demand": 12000, "med_demand": 1600, "vehicle_demand": 4, "team_demand": 5, "shelter_demand": 320, "critical_priority": "High"},
            {"id": 2, "state_name": "Delhi", "district": "East Delhi", "name": "Mayur Vihar Floodplain", "latitude": 28.6050, "longitude": 77.2950, "population": 15000, "severity": 4.4, "accessibility_score": 0.45, "road_condition": "Submerged Embankment", "distance_km": 12.0, "travel_time_hours": 0.8, "water_demand": 20000, "food_demand": 10000, "med_demand": 1400, "vehicle_demand": 3, "team_demand": 4, "shelter_demand": 280, "critical_priority": "High"},
            {"id": 3, "state_name": "Delhi", "district": "South East Delhi", "name": "Okhla Barrage Lowlands", "latitude": 28.5350, "longitude": 77.3100, "population": 12000, "severity": 3.8, "accessibility_score": 0.60, "road_condition": "Waterlogged Highway", "distance_km": 18.0, "travel_time_hours": 1.1, "water_demand": 16000, "food_demand": 8000, "med_demand": 1000, "vehicle_demand": 3, "team_demand": 3, "shelter_demand": 210, "critical_priority": "Medium"}
        ],
        "resources": DEFAULT_RESOURCES,
        "vehicles": DEFAULT_VEHICLES,
        "teams": DEFAULT_TEAMS
    },

    # 8. UTTARAKHAND (Uttarakhand SEOC)
    "Himalayan Flash Flood & Landslide": {
        "disaster": {
            "id": 8,
            "name": "Himalayan Cloudburst & Mountain Landslides",
            "type": "Landslide",
            "state_name": "Uttarakhand",
            "declaration_date": "2026-10-31",
            "status": "Critical Rescue",
            "description": "High-altitude cloudburst triggering debris flows, washed out bridges, and isolated mountain settlements."
        },
        "hub": ALL_INDIA_SEOC_HUBS[26], # Uttarakhand SEOC, Dehradun
        "regions": [
            {"id": 1, "state_name": "Uttarakhand", "district": "Chamoli", "name": "Cloudburst Gorge Upper Ward", "latitude": 30.145, "longitude": 79.280, "population": 4200, "severity": 4.9, "accessibility_score": 0.15, "road_condition": "Debris Blocked / Air Drop Only", "distance_km": 140.0, "travel_time_hours": 5.5, "water_demand": 11000, "food_demand": 5800, "med_demand": 850, "vehicle_demand": 3, "team_demand": 4, "shelter_demand": 180, "critical_priority": "Critical"},
            {"id": 2, "state_name": "Uttarakhand", "district": "Rudraprayag", "name": "Terraced Orchard Hamlet", "latitude": 30.210, "longitude": 79.350, "population": 3100, "severity": 4.2, "accessibility_score": 0.35, "road_condition": "Mudslide / 4x4 Only", "distance_km": 125.0, "travel_time_hours": 4.8, "water_demand": 7500, "food_demand": 3900, "med_demand": 550, "vehicle_demand": 2, "team_demand": 3, "shelter_demand": 120, "critical_priority": "High"},
            {"id": 3, "state_name": "Uttarakhand", "district": "Chamoli", "name": "Upper Glacial Valley", "latitude": 30.320, "longitude": 79.420, "population": 2600, "severity": 4.8, "accessibility_score": 0.10, "road_condition": "Bridge Collapsed / Impassable", "distance_km": 160.0, "travel_time_hours": 6.5, "water_demand": 8000, "food_demand": 4200, "med_demand": 600, "vehicle_demand": 2, "team_demand": 3, "shelter_demand": 140, "critical_priority": "Critical"}
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 38000, "unit_cost": 1.20, "unit_weight_kg": 1.0, "priority_weight": 1.5, "description": "Highland pack-canisters"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 18000, "unit_cost": 3.00, "unit_weight_kg": 0.6, "priority_weight": 1.4, "description": "High-altitude calorie bars"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 2400, "unit_cost": 22.00, "unit_weight_kg": 2.5, "priority_weight": 2.2, "description": "Hypothermia and trauma kits"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 550, "unit_cost": 150.00, "unit_weight_kg": 16.0, "priority_weight": 1.6, "description": "Alpine thermal tents"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 6, "cargo_capacity_kg": 3500, "speed_kmh": 35, "cost_per_km": 4.2, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 2, "cargo_capacity_kg": 1000, "speed_kmh": 20, "cost_per_km": 6.0, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 4, "cargo_capacity_kg": 700, "speed_kmh": 50, "cost_per_km": 3.2, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 8, "personnel_per_team": 6, "specialization": "Mountain & rubble extrication", "daily_cost": 750.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 5, "personnel_per_team": 4, "specialization": "Alpine trauma care", "daily_cost": 950.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 5, "personnel_per_team": 6, "specialization": "Thermal shelter erection", "daily_cost": 500.0}
        ]
    },

    # 9. MAHARASHTRA (Maharashtra SEOC)
    "Urban Mega-Earthquake (Magnitude 7.4)": {
        "disaster": {
            "id": 9,
            "name": "Metropolitan Fault Slip Earthquake (M 7.4)",
            "type": "Earthquake",
            "state_name": "Maharashtra",
            "declaration_date": "2026-11-01",
            "status": "State of Emergency",
            "description": "Severe shallow crustal rupture causing high-density multi-story building collapse and mass casualties."
        },
        "hub": ALL_INDIA_SEOC_HUBS[13], # Maharashtra SEOC, Mantralaya, Mumbai
        "regions": [
            {"id": 1, "state_name": "Maharashtra", "district": "Mumbai City", "name": "Downtown Historic Quarter", "latitude": 18.930, "longitude": 72.835, "population": 28000, "severity": 5.0, "accessibility_score": 0.20, "road_condition": "Rubble Blocked / Gas Leaks", "distance_km": 2.5, "travel_time_hours": 0.8, "water_demand": 45000, "food_demand": 25000, "med_demand": 3800, "vehicle_demand": 8, "team_demand": 10, "shelter_demand": 600, "critical_priority": "Critical"},
            {"id": 2, "state_name": "Maharashtra", "district": "Mumbai Suburban", "name": "Metro Subway Interchange", "latitude": 19.045, "longitude": 72.865, "population": 19500, "severity": 4.8, "accessibility_score": 0.30, "road_condition": "Fissures & Structural Hazards", "distance_km": 14.0, "travel_time_hours": 1.5, "water_demand": 32000, "food_demand": 18000, "med_demand": 2600, "vehicle_demand": 6, "team_demand": 8, "shelter_demand": 420, "critical_priority": "Critical"},
            {"id": 3, "state_name": "Maharashtra", "district": "Mumbai Suburban", "name": "Hospital Corridor West", "latitude": 19.070, "longitude": 72.880, "population": 16000, "severity": 3.2, "accessibility_score": 0.85, "road_condition": "Cleared Emergency Lane", "distance_km": 17.0, "travel_time_hours": 1.1, "water_demand": 22000, "food_demand": 11000, "med_demand": 2100, "vehicle_demand": 4, "team_demand": 4, "shelter_demand": 280, "critical_priority": "Medium"}
        ],
        "resources": [
            {"id": 1, "name": "Clean Drinking Water", "type": "Divisible", "unit": "Liters", "total_available": 120000, "unit_cost": 0.90, "unit_weight_kg": 1.0, "priority_weight": 1.5, "description": "Purified water tankers and sachets"},
            {"id": 2, "name": "Ready-to-Eat Food Packets", "type": "Divisible", "unit": "Packets", "total_available": 65000, "unit_cost": 2.60, "unit_weight_kg": 0.6, "priority_weight": 1.3, "description": "Urban survival packs"},
            {"id": 3, "name": "Emergency Medical Kits", "type": "Divisible", "unit": "Kits", "total_available": 9500, "unit_cost": 18.00, "unit_weight_kg": 2.2, "priority_weight": 2.4, "description": "Trauma surgery & burn kits"},
            {"id": 4, "name": "Temporary Emergency Shelters", "type": "Indivisible", "unit": "Tents", "total_available": 1600, "unit_cost": 130.00, "unit_weight_kg": 15.0, "priority_weight": 1.4, "description": "Rapid deploy city shelters"}
        ],
        "vehicles": [
            {"id": 1, "type": "4x4 Heavy Relief Truck", "total_available": 15, "cargo_capacity_kg": 4000, "speed_kmh": 40, "cost_per_km": 3.5, "can_handle_rough_terrain": 1, "can_handle_waterlogged": 0},
            {"id": 2, "type": "Inflatable Rescue Boat & Trailer", "total_available": 4, "cargo_capacity_kg": 1200, "speed_kmh": 25, "cost_per_km": 5.0, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 1},
            {"id": 3, "type": "Emergency Paramedic Ambulance", "total_available": 14, "cargo_capacity_kg": 800, "speed_kmh": 55, "cost_per_km": 2.8, "can_handle_rough_terrain": 0, "can_handle_waterlogged": 0}
        ],
        "teams": [
            {"id": 1, "type": "Search and Rescue (SAR) Squad", "total_available": 18, "personnel_per_team": 6, "specialization": "Canine search & heavy rubble cutting", "daily_cost": 700.0},
            {"id": 2, "type": "Emergency Medical Response Unit", "total_available": 15, "personnel_per_team": 4, "specialization": "Field triage & critical care", "daily_cost": 950.0},
            {"id": 3, "type": "Logistics & Shelter Deployment Crew", "total_available": 10, "personnel_per_team": 8, "specialization": "Displaced population management", "daily_cost": 450.0}
        ]
    }
}
