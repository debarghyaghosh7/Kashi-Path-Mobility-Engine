# **Kashi Path: Predictive Urban Mobility Engine**

### *Making AI Work for India*

**Kashi Path** is a multi-modal autonomous governance engine designed to optimize urban mobility in Varanasi. It bridges the "usable intelligence" gap by integrating real-time environmental, infrastructure, and safety data into a unified routing logic for public and emergency services.

## **Core Features**

* **Multi-Modal Layered Graph:** Optimized routing for E-Buses, E-Rickshaws (Informal Sector), and Ambulances.
* **Safety-First Routing:** Automated blockades based on **Central Water Commission (CWC)** flood levels (71.26m mark).
* **Predictive Crowd Management:** Integration with **Kashi Integrated Command and Control Centre (KICCC)** metadata to preemptively bypass crowd surges.
* **Infrastructure Preservation:** Algorithmically avoids "Poor" quality road segments using the **International Roughness Index (IRI)** to protect EV assets.
* **Public Health Nudge:** AQI-aware pathfinding to reduce pollutant exposure for passengers and informal workers.

---

## **Tech Stack**

* **Language:** Python 3.9+
* **Graph Engine:** `networkx`
* **Computing:** Optimized for the **IndiaAI 38,000 GPU** national infrastructure.
* **Integrations:** BharatGen AI (Multilingual Voice), CPCB (Environment), CWC (Safety).

---

## **Setup Instructions**

### **1. Prerequisites**

Ensure you have Python installed on your system. It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### **2. Install Dependencies**

The engine is built with a focus on **Feasibility (10%)** and lightweight deployment.

```bash
pip install networkx

```

### **3. Project Structure**

```text
KashiPath/
├── engine.py           # Core MultiDiGraph logic and MOSP algorithm
├── simulation.py       # Live data simulation and scenario testing
├── data/
│   └── routes.csv      # Digitalized Varanasi transit network
└── README.md           # Documentation

```

### **4. Running the Engine**

To execute the unified mobility simulation with real-time governance constraints:

```bash
python engine.py

```

---

## **Working Principles & Weightage**

The engine operates on a **Multi-Objective Cost Function**:
$$Weight = T_{base} \times (1 + \alpha_{IRI} + \beta_{AQI} + \gamma_{Crowd}) + \Omega_{Flood}$$

| Parameter | Weightage Logic | Governance Goal |
| --- | --- | --- |
| **IRI ()** | 40% Penalty if IRI > 170 | Asset Preservation (E-Bus Maintenance) |
| **AQI ()** | 5-10% Nudge if AQI > 200 | Public Health Protection |
| **Crowd ()** | Exponential increase > 4  | Safety & Gridlock Prevention |
| **Flood ()** | Infinite Weight (Blockade) | Zero-Casualty Governance |

---

## **Documentation of Logic Traces**

To satisfy the **Interpretability (20%)** requirement, every routing decision produces a **Governance Trace**. This allows administrators to verify *why* the AI diverted a vehicle:

* **Example Output:** `[Ambulance] Optimized Route: SSPG -> Cantt -> BHU`
* **Trace:** `[!] Segment Godowlia-Lanka bypassed: PEDESTRIAN_ZONE_ACTIVE (Mela Surge: 5.2 P/m² detected by KICCC).`

---

## **Scalability & Mission Alignment**

* **Digital ShramSetu:** Includes dedicated logic for e-rickshaw stands to formalize the informal sector.
* **BharatGen Integration:** The engine is modularized to accept voice-query inputs via the national multimodal LLM for **22-language support**.
* **Infrastructure-Agnostic:** Capable of running in low-bandwidth or compute-deficient districts by identifying "Resilient Corridors."

---

**Developed for the AI for Governance Hackathon 2026**
*Transforming Varanasi’s ancient flow with modern intelligence.*
