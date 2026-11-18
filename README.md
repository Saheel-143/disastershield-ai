# DisasterShield AI – Intelligent Disaster Resource Allocation 🛡️

**Academic Course Project:** CSDX 507 Decision-Making for Data Science (Module IV & Module V)  
**Prototype Classification:** Academic Operations Research & Decision-Support System  
**Visual Aesthetic:** Dark Navy Command Center (`#0B192C`, `#1E3E62`) with Neon Emergency Orange (`#FF6500`, `#FF8A08`)

---

## 📌 Executive Summary

**DisasterShield AI** is an AI-powered disaster management decision-support web application designed to help emergency planners equitably and optimally allocate strictly constrained relief resources—including **clean drinking water**, **ready-to-eat rations**, **medical trauma kits**, **rescue vehicles**, **specialized rescue teams**, and **emergency shelters**—across disaster-affected communities.

The platform provides a unified decision framework for **Floods**, **Cyclones**, **Earthquakes**, and **Landslides**, addressing realistic disaster operational challenges: severe resource deficits (~67% demand coverage), degraded or blocked road corridors, variable regional vulnerability, and competing operational objectives (minimizing casualty risk and delivery latency vs. budget expenditure).

---

## 🎓 Academic Alignment: CSDX 507 Decision-Making for Data Science

The platform serves as an interactive demonstration laboratory for core optimization methodologies covered in **Modules IV and V**:

| Algorithm | Category | Syllabus Topic | Mathematical Focus |
| :--- | :--- | :--- | :--- |
| **Linear Programming** | Exact Optimization | Module IV: LP & Simplex | Continuous relaxation for divisible supplies; dual simplex solver (`scipy.optimize.linprog` HiGHS) |
| **Integer Programming** | Exact Optimization | Module IV: IP & Branch-and-Bound | Discrete integer dispatch for indivisible vehicles & rescue teams (`OR-Tools` SCIP solver) |
| **Greedy Urgency Heuristic** | Heuristic Algorithm | Module V: Priority Heuristics | Transparent multi-factor Urgency Index ranking with step-by-step decision audit logs |
| **Genetic Algorithm** | Metaheuristic | Module V: Evolutionary Algorithms | Population-based exploration (`DEAP`) with dedicated **feasibility repair operators** |
| **Simulated Annealing** | Metaheuristic | Module V: Trajectory Metaheuristics | Metropolis acceptance criterion with geometric temperature cooling ($T_{k+1} = \alpha T_k$) |
| **Multi-Objective (NSGA-II)** | Pareto Optimization | Module V: Multi-Criteria Decision | Simultaneous minimization of delivery latency & operational cost vs. unmet shortages (`pymoo`) |

---

## 📐 Mathematical Formulations

### 1. Linear Programming (LP)
* **Variables:** $x_{i, r} \ge 0$, volume of resource $r$ dispatched to region $i$.
* **Objective:** Maximize urgency-weighted demand satisfaction minus distance-weighted delivery penalties:
  $$\max Z = \sum_{i=1}^N \sum_{r \in \mathcal{R}} w_r \cdot U_i \cdot \left(\frac{x_{i, r}}{\text{Demand}_{i, r}}\right) - \lambda \sum_{i=1}^N \sum_{r \in \mathcal{R}} \left(\frac{\text{Distance}_i}{100}\right) \cdot \text{Cost}_r \cdot x_{i, r}$$
* **Constraints:**
  1. Supply limit: $\sum_{i=1}^N x_{i, r} \le \text{Supply}_r \quad \forall r \in \mathcal{R}$
  2. Demand upper bound: $0 \le x_{i, r} \le \text{Demand}_{i, r} \quad \forall i, r$

### 2. Integer Programming (IP)
* **Variables:** $y_{i, v} \in \mathbb{Z}_{\ge 0}$ (whole vehicles), $z_{i, t} \in \mathbb{Z}_{\ge 0}$ (whole rescue squads).
* **Objective:** Maximize life rescue capability and critical coverage:
  $$\max \sum_{i=1}^N U_i \left( \sum_v \text{Capacity}_v \cdot y_{i, v} + \sum_t \text{Personnel}_t \cdot z_{i, t} \right) - \sum \text{DispatchCosts}$$
* **Constraints:** Fleet and team availability bounds; road accessibility terrain rules (e.g., rescue boats required in waterlogged zones; standard ambulances restricted on flooded roads).

### 3. Explainable Greedy Priority Heuristic
* **Urgency Index ($U_i$):**
  $$U_i = 0.40 \cdot \left(\frac{\text{Severity}_i}{5.0}\right) + 0.25 \cdot \left(\frac{\text{Population}_i}{\max \text{Pop}}\right) + 0.20 \cdot (1.0 - \text{Accessibility}_i) + 0.15 \cdot \text{PriorityFactor}_i$$
* **Policy:** Sort regions in descending order of $U_i$ and greedily allocate $\min(\text{Demand}_{i, r}, \text{RemainingSupply}_r)$ with a full audit log.

### 4. Genetic Algorithm (DEAP) with Feasibility Repair
* **Chromosome:** Real-valued vectors $g_{i, r} \in [0, 1]$ representing demand fulfillment fractions.
* **Repair Operator:** If $\sum_i g_{i, r} \cdot \text{Demand}_{i, r} > \text{Supply}_r$, allocations are proportionally rescaled down to exact supply capacity, guaranteeing 100% strict physical feasibility for every candidate evaluated.

### 5. Simulated Annealing (Metropolis Trajectory Search)
* **Neighbor Generation:** Transfers a quantum mass $\delta$ from donor region $i$ to recipient region $j$ for resource $r$, strictly bounded by available supply and recipient demand headroom.
* **Metropolis Criterion:** Accepts worsening moves with probability $P = \exp(-\Delta E / T)$ where temperature cools geometrically: $T_{k+1} = \alpha T_k$ ($\alpha = 0.94$).

### 6. Multi-Objective Optimization (pymoo NSGA-II)
* **Conflicting Objectives:**
  1. $f_1(x)$: Minimize Total Delivery Latency (urgency-weighted hours)
  2. $f_2(x)$: Minimize Total Operational & Distribution Cost (USD)
  3. $f_3(x)$: Minimize Unmet Resource Shortage (Maximizing Fulfillment)
* **Output:** Generates non-dominated Pareto front; automatically identifies the **Compromise Knee Point** using minimum normalized Euclidean distance to the Utopia point.

---

## 🤖 AI Severity Prediction Model

* **Architecture:** Scikit-Learn `RandomForestRegressor` trained on 1,500 multi-hazard synthetic scenarios.
* **Features:** 24h rainfall (mm), flood gauge level (m), wind speed (km/h), soil moisture saturation (%), Richter magnitude, terrain slope (degrees), population density, infrastructure quality score, bridge cutoff indicator, and distance to central hub.
* **Metrics:** Evaluated via Train/Test split: $R^2 \approx 0.82$, $\text{RMSE} \approx 0.45$, $\text{MAE} \approx 0.36$.
* **Advisory Engine:** Maps severity to operational posture and recommended demand multipliers ($0.7\times$ to $1.6\times$).

---

## 📂 Project Architecture

```
disastershield_ai/
├── app.py                      # Main Streamlit web application & command dashboard
├── requirements.txt            # Python dependencies (open-source only)
├── README.md                   # Comprehensive documentation & mathematical formulations
├── database/
│   ├── db.py                   # SQLite database manager, schemas, CRUD helpers, run persistence
│   └── disastershield.db       # SQLite local database instance
├── data/
│   ├── default_data.py         # Realistic baseline scenario (10 regions, depot, resources, fleet)
│   ├── generate_historical_data.py # Synthetic historical disaster dataset generator
│   └── historical_disaster_data.csv # 1,500 training records for AI model
├── models/
│   ├── severity_predictor.py   # Scikit-Learn Random Forest model training & real-time inference
│   └── severity_model.joblib   # Persisted model artifact
├── algorithms/
│   ├── base.py                 # Core OptimizationProblem, OptimizationResult, constraint validator
│   ├── linear_programming.py   # SciPy HiGHS Simplex LP solver
│   ├── integer_programming.py  # Google OR-Tools SCIP Integer solver
│   ├── greedy.py               # Explainable urgency heuristic with decision audit log
│   ├── genetic_algorithm.py    # DEAP Evolutionary Algorithm with constraint repair operator
│   ├── simulated_annealing.py  # Metropolis neighborhood search with geometric cooling
│   ├── multi_objective.py      # pymoo NSGA-II Multi-Objective solver with Pareto front
│   └── benchmark.py            # Unified comparison engine running all 6 solvers
├── utils/
│   ├── map_visualizer.py       # Folium map visualizer with custom emergency pins & corridors
│   ├── chart_builder.py        # Plotly charts (Pareto front, convergence, radars, stacked bars)
│   └── pdf_exporter.py         # ReportLab official PDF dispatch plan & CSV exporter
└── tests/
    └── test_algorithms.py      # Rigorous unit test suite verifying constraints & edge cases (10/10 PASS)
```

---

## 🌐 Free Open-Source API Integrations (Zero API Key Required)

DisasterShield AI integrates 3 completely free, open-source public APIs that require **no API keys**, **no credit cards**, and **no cloud sign-ups**:

1. **Open-Meteo Weather & Flood API (`api.open-meteo.com`)**:
   - Queries real-time precipitation/rainfall (mm), sustained wind speeds (km/h), humidity, and surface pressure for any affected region's geographic coordinates.
   - Automatically feeds real-time telemetry into the **AI Severity Prediction** engine and road accessibility estimators.
2. **USGS Earthquake Hazards Program Live Feed (`earthquake.usgs.gov`)**:
   - Real-time seismic event feed streaming active global earthquakes with Richter magnitude, hypocenter depth (km), epicenter coordinates, tsunami alerts, and origin timestamps.
   - Planners can review live seismic hazards in the **Disaster & Locations** interface.
3. **OpenStreetMap Nominatim Geocoding API (`nominatim.openstreetmap.org`)**:
   - Free worldwide place-name resolution; converts real-world city, district, or village names into precise latitude and longitude coordinates.

---

## 💻 Installation & Execution Guide (Windows PowerShell)

### Prerequisites
* Windows 10/11
* Python 3.10+ installed

### Step 1: Open PowerShell and Navigate to Project Directory
```powershell
cd C:\Users\Sahee\.gemini\antigravity-ide\scratch\disastershield_ai
```

### Step 2: Install Required Dependencies
All libraries are free open-source packages:
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Run the Unit Test Suite
Verify that all algorithms and constraint validators pass with 100% feasibility:
```powershell
python -m unittest tests/test_algorithms.py
```
*(Expected output: `Ran 8 tests ... OK`)*

### Step 4: Launch the DisasterShield AI Web Application
```powershell
python -m streamlit run app.py
```
The application will launch automatically in your default browser at:  
👉 **`http://localhost:8501`**

---

## 🕹️ Module-by-Module Walkthrough

1. **🏠 Command Dashboard:** Live operational overview showing total affected population (86,200), critical emergency zones, aggregated supply deficit, fleet status, interactive Folium operational map, and quick-solve dispatch.
2. **🚨 Disaster & Locations:** View all 10 affected regions, edit regional demands/accessibility, or register new affected zones with real-time database updates.
3. **📦 Resources & Fleet:** Manage stockpile levels for water, food, medicines, shelters, vehicles (4x4 trucks, rescue boats, ambulances), and rescue personnel squads.
4. **🤖 AI Severity Prediction:** Interactive environmental hazard simulator predicting severity scores, risk tiers, and demand multipliers with model evaluation metrics and feature importance charts.
5. **⚡ Optimization Engine:** Execute individual algorithms (LP, IP, Greedy, GA, SA, NSGA-II), customize hyperparameters, inspect feasibility notes, review convergence curves, and download official PDF/CSV dispatch plans.
6. **📊 Benchmark & Comparison:** One-click execution of all 6 algorithms on the exact same baseline scenario, rendering a multi-dimensional performance radar, runtime vs. fulfillment scatter plot, and summary matrix.
7. **🌪️ Scenario Stress Simulator:** Dynamically apply disaster shocks (e.g. -25% supply cut, +30% population surge, major bridge collapse) and view side-by-side Before vs. After impact diffs.
8. **📑 Reports & Dispatch Orders:** Compile and download publication-ready official PDF dispatch orders and CSV manifests with complete audit trails.
9. **📚 Academic Theory (CSDX 507):** Full syllabus-aligned mathematical explanations, objective functions, constraint sets, and algorithmic methodologies.

---

## ⚠️ Academic & Operational Disclaimer

This platform is an **academic decision-support prototype** developed exclusively for educational and research demonstration in **CSDX 507 Decision-Making for Data Science**.
* It is **not** an operational emergency dispatch system and does not replace trained emergency services (e.g., National Disaster Response Force - NDRF, FEMA).
* Synthetic AI severity predictions and optimization outputs must be evaluated and approved by authorized disaster management personnel before real-world logistical deployment.
* No personal or sensitive emergency information is collected or processed.
