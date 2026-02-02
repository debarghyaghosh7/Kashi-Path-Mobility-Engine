import networkx as nx
from datetime import datetime

class KashiPathEngine:
    def __init__(self):
        # Using MultiDiGraph to support different transit modes on the same route
        self.G = nx.MultiDiGraph()
        
        # Governance Constants & Thresholds
        self.FLOOD_DANGER_MARK = 71.26
        self.IRI_BAD_THRESHOLD = 170
        self.CROWD_SAFETY_LIMIT = 4.0
        
        self.initialize_city_network()

    def initialize_city_network(self):
        """Builds the foundational digital twin of Varanasi's transit layers."""
        # 1. NODES: Transit Hubs and Emergency Centers
        hubs = [
            ("LBS_Airport", "Transit"), ("Cantt_Station", "Transit"),
            ("Godowlia_Stand", "Rickshaw"), ("Lanka_Stand", "Rickshaw"),
            ("BHU_Trauma_Centre", "Hospital"), ("SSPG_Kabir_Chaura", "Hospital"),
            ("Maidagin_Chowk", "Junction"), ("Dashashwamedh_Ghat", "Riverfront")
        ]
        for name, n_type in hubs:
            self.G.add_node(name, type=n_type)

        # 2. EDGES: Multi-modal connections with explicit mode tagging
        # Format: (Source, Target, BaseTime, Mode)
        routes = [
            # formal sector: E-Buses (Route E101/E102)
            ("LBS_Airport", "Cantt_Station", 42, "E-Bus"),
            ("Cantt_Station", "Maidagin_Chowk", 18, "E-Bus"),
            ("Cantt_Station", "Lanka_Stand", 28, "E-Bus"),
            
            # Informal sector: Digital ShramSetu E-Rickshaws
            ("Maidagin_Chowk", "Godowlia_Stand", 12, "E-Rickshaw"),
            ("Godowlia_Stand", "Dashashwamedh_Ghat", 8, "E-Rickshaw"),
            ("Godowlia_Stand", "Lanka_Stand", 18, "E-Rickshaw"),
            
            # Emergency: Ambulance Green Corridors
            ("SSPG_Kabir_Chaura", "Cantt_Station", 10, "Ambulance"),
            ("Cantt_Station", "BHU_Trauma_Centre", 22, "Ambulance")
        ]
        
        for u, v, t, m in routes:
            # Ensure every edge is initialized with all required keys to prevent KeyErrors
            self.G.add_edge(u, v, weight=float(t), base_time=float(t), mode=m, status="Clear")

    def sync_governance_data(self, flood_lvl, aqi, road_conditions, crowd_densities, mela_active=False):
        """Updates graph weights based on real-time city pulse."""
        print(f"\n--- Unified Kashi-Pulse Update: {datetime.now().strftime('%H:%M:%S')} ---")
        
        for u, v, key, data in self.G.edges(keys=True, data=True):
            # Start with the base travel time
            cost = data.get('base_time', 15.0)
            status = "Clear"
            mode = data.get('mode', 'General')

            # 1. INFRASTRUCTURE: Road Quality (IRI)
            if road_conditions.get(f"{u}-{v}", 80) > self.IRI_BAD_THRESHOLD:
                cost *= 1.4  # 40% maintenance penalty for E-Bus protection
                status = "CAUTION_ROUGH_ROAD"

            # 2. PREDICTIVE: KICCC Crowd Analytics
            density = crowd_densities.get(v, 0.5)
            if density > self.CROWD_SAFETY_LIMIT:
                cost *= (density / 2.0)  # Exponential congestion penalty
                status = f"SURGE_ALERT_{density}P/m2"

            # 3. HEALTH: Environmental AQI Nudge
            if aqi > 200:
                cost *= 1.1 if mode == "E-Rickshaw" else 1.05
                if status == "Clear": status = "HEALTH_NUDGE_ACTIVE"

            # 4. SAFETY: CWC Flood Danger Gate
            if flood_lvl >= self.FLOOD_DANGER_MARK and ("Ghat" in v or "Ghat" in u):
                cost = 1e9  # Infinite cost to simulate a blockade
                status = "BLOCKADE_FLOOD_ALERT"

            # Update the edge with new calculated weight and status trace
            self.G[u][v][key].update({'weight': cost, 'status': status})

    def solve_path(self, start, end, vehicle_type):
        """Solves for the optimal path while providing interpretability traces."""
        # Define allowed modes: Ambulances can use E-Bus lanes
        allowed_modes = [vehicle_type]
        if vehicle_type == "Ambulance":
            allowed_modes.append("E-Bus")

        # Robust weight logic to prevent KeyErrors
        def weight_logic(u, v, d):
            edge_mode = d.get('mode', 'General')
            edge_weight = d.get('weight', 1e9)
            return edge_weight if edge_mode in allowed_modes else 1e9

        try:
            path = nx.shortest_path(self.G, start, end, weight=weight_logic)
            total_cost = nx.shortest_path_length(self.G, start, end, weight=weight_logic)
            
            print(f"\n[{vehicle_type}] Optimized Route: {' -> '.join(path)}")
            print(f"Governance Cost Score: {total_cost:.2f}")
            
            # Print Logic Trace for transparency
            for i in range(len(path)-1):
                # Retrieve edge data safely
                edge_data = list(self.G.get_edge_data(path[i], path[i+1]).values())[0]
                if edge_data.get('status') != "Clear":
                    print(f"  > Segment {path[i]}-{path[i+1]}: {edge_data['status']}")
            
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            print(f"[!] No safe route found for {vehicle_type} from {start} to {end}.")

# --- DEMO EXECUTION SCENARIO ---
if __name__ == "__main__":
    engine = KashiPathEngine()

    # Simulated Live Governance Data
    live_feeds = {
        "river": 71.5,  # Ganga above danger mark
        "aqi": 245,     # High pollution alert
        "roads": {"LBS_Airport-Cantt_Station": 195}, # Infrastructure damage
        "crowds": {"Dashashwamedh_Ghat": 5.2}, # Predictive surge detected
        "mela": True
    }

    # Update the engine with city data
    engine.sync_governance_data(
        flood_lvl=live_feeds["river"],
        aqi=live_feeds["aqi"],
        road_conditions=live_feeds["roads"],
        crowd_densities=live_feeds["crowds"]
    )

    # Solve paths for different public sectors
    engine.solve_path("Cantt_Station", "Lanka_Stand", "E-Rickshaw")
    engine.solve_path("SSPG_Kabir_Chaura", "BHU_Trauma_Centre", "Ambulance")
    
    print("\n" + "="*45)
    print("KASHI PATH: ENGINE OPERATIONAL")
    print("Mission: AI for Governance Hackathon 2026")
    print("="*45)
