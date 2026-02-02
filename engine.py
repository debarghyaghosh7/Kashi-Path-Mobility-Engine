import networkx as nx
from datetime import datetime

class KashiPathEngine:
    def __init__(self):
        # MultiDiGraph allows different travel modes between the same hubs
        self.G = nx.MultiDiGraph()
        
        # Governance Thresholds
        self.CWC_DANGER_LEVEL = 71.26  # Official Flood Mark for Varanasi
        self.IRI_POOR_THRESHOLD = 170   # Pavement Quality Index (Poor > 170)
        self.KICCC_CROWD_LIMIT = 4.0    # Pedestrians/sqm (Safety Threshold)
        
        self.initialize_city_network()

    def initialize_city_network(self):
        """Sets up the foundational multi-modal infrastructure of Varanasi."""
        # 1. NODES: Categorized Urban Hubs
        nodes = [
            ("LBS_Airport", "Transit"), ("Cantt_Station", "Transit"),
            ("Godowlia_Stand", "Rickshaw_Hub"), ("Lanka_Stand", "Rickshaw_Hub"),
            ("BHU_Trauma_Centre", "Hospital"), ("SSPG_Kabir_Chaura", "Hospital"),
            ("Maidagin_Chowk", "Junction"), ("Dashashwamedh_Ghat", "Riverfront")
        ]
        for name, n_type in nodes:
            self.G.add_node(name, node_type=n_type)

        # 2. EDGES: Multi-modal connections (Base Time in mins)
        edges = [
            # E-Bus Major Corridors (Route E101/E102)
            ("LBS_Airport", "Cantt_Station", 42, "E-Bus"),
            ("Cantt_Station", "Maidagin_Chowk", 18, "E-Bus"),
            ("Cantt_Station", "Lanka_Stand", 28, "E-Bus"),
            
            # E-Rickshaw Last-Mile (Digital ShramSetu Focus)
            ("Maidagin_Chowk", "Godowlia_Stand", 12, "E-Rickshaw"),
            ("Godowlia_Stand", "Dashashwamedh_Ghat", 8, "E-Rickshaw"),
            ("Godowlia_Stand", "Lanka_Stand", 18, "E-Rickshaw"),
            
            # Emergency Ambulance Corridors (Green Corridors)
            ("SSPG_Kabir_Chaura", "Cantt_Station", 10, "Ambulance"),
            ("Cantt_Station", "BHU_Trauma_Centre", 22, "Ambulance")
        ]
        for u, v, t, m in edges:
            self.G.add_edge(u, v, base_time=t, weight=t, mode=m, status="Clear")

    def update_governance_parameters(self, river_level, aqi, road_states, crowd_data, mela_active=False):
        """
        Applies Multi-Objective Cost logic to update graph weights.
        Weight = Base_Time * (1 + IRI_Penalty + AQI_Penalty + Crowd_Penalty) + Flood_Penalty
        """
        print(f"\n--- Unified Kashi-Pulse Update: {datetime.now().strftime('%H:%M:%S')} ---")
        
        for u, v, key, data in self.G.edges(keys=True, data=True):
            cost = data['base_time']
            segment_status = "Clear"

            # 1. INFRASTRUCTURE: Road Quality (IRI)
            # Penalty (alpha): High impact to protect EV battery and suspension assets
            iri_val = road_states.get(f"{u}-{v}", 80)
            if iri_val > self.IRI_POOR_THRESHOLD:
                cost *= 1.4  # 40% maintenance penalty
                segment_status = "CAUTION_BROKEN_ROAD"

            # 2. SAFETY: CWC Flood Levels
            # Penalty (Psi): Absolute safety gate for riverfront corridors
            if river_level >= self.CWC_DANGER_LEVEL and "Ghat" in v:
                cost += 2000 # Non-negotiable blockade
                segment_status = "BLOCKADE_FLOOD_ALERT"

            # 3. PREDICTIVE: KICCC Crowd Pulse
            # Penalty (gamma): Exponential delay as density nears limits
            density = crowd_data.get(v, 0.5)
            if density > self.KICCC_CROWD_LIMIT:
                cost *= (density / 2.0)  # Predictive congestion drainage
                segment_status = f"SURGE_ALERT_{density}P/m2"

            # 4. HEALTH: Air Quality (AQI) 
            # Penalty (beta): Calibrated low-impact nudge for green-routing
            if aqi > 200:
                aqi_penalty = 1.05 if data['mode'] == "E-Bus" else 1.10
                cost *= aqi_penalty
                if segment_status == "Clear": segment_status = "MINOR_AQI_NUDGE"

            # 5. GOVERNANCE: Magh Mela Pedestrian Zones
            if mela_active and "Godowlia" in v and data['mode'] != "Ambulance":
                cost += 60  # Administrative restriction delay
                segment_status = "PEDESTRIAN_ZONE_ACTIVE"

            # Finalize edge parameters
            self.G[u][v][key]['weight'] = cost
            self.G[u][v][key]['status'] = segment_status

    def solve_path(self, start, end, vehicle_type):
        """Calculates the best route for a specific vehicle mode."""
        # Ambulances are permitted to use E-Bus 'Green Corridors'
        allowed = [vehicle_type]
        if vehicle_type == "Ambulance": allowed.append("E-Bus")

        def weight_logic(u, v, d):
            return d['weight'] if d['mode'] in allowed else 1e9

        try:
            path = nx.shortest_path(self.G, start, end, weight=weight_logic)
            total_score = nx.shortest_path_length(self.G, start, end, weight=weight_logic)
            
            print(f"\n[{vehicle_type}] Optimized Route: {' -> '.join(path)}")
            print(f"Governance Cost Score: {total_score:.2f}")
            
            # Actionable Intelligence Trace for Administrators
            for i in range(len(path)-1):
                edge_data = list(self.G.get_edge_data(path[i], path[i+1]).values())[0]
                if edge_data['status'] != "Clear":
                    print(f"  > Segment {path[i]}-{path[i+1]}: {edge_data['status']}")
                    
            return path
        except nx.NetworkXNoPath:
            print(f"[!] No viable route found for {vehicle_type} under current constraints.")

# --- LIVE EXECUTION SCENARIO ---
if __name__ == "__main__":
    engine = KashiPathEngine()

    # Simulated Live Feeds
    city_snapshot = {
        "river": 71.5, # Above danger mark
        "aqi": 240,    # Poor quality
        "roads": {"LBS_Airport-Cantt_Station": 190}, # Broken segment
        "crowd": {"Dashashwamedh_Ghat": 5.2}, # Crowd surge detected
        "mela": True
    }

    engine.update_governance_parameters(
        river_level=city_snapshot["river"],
        aqi=city_snapshot["aqi"],
        road_states=city_snapshot["roads"],
        crowd_data=city_snapshot["crowd"],
        mela_active=city_snapshot["mela"]
    )

    # Output: Optimized paths for different sectors
    engine.solve_path("Cantt_Station", "Lanka_Stand", "E-Rickshaw")
    engine.solve_path("SSPG_Kabir_Chaura", "BHU_Trauma_Centre", "Ambulance")
