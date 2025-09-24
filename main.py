import csv
import heapq
import sys
from stationNode import StationNode



class MetroGraph:
    """Represents the Mexico City Metro network."""
    def __init__(self):
        self.nodes = {}

    def load_nodes_from_csv(self, file_path):
        """Reads station data and creates StationNode objects."""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                systems = row['system'].split(';')
                lines = row['lines'].split(';')
                self.nodes[row['station_id']] = StationNode(
                    row['station_id'], row['name'], systems, lines
                )
        print(f"Loaded {len(self.nodes)} nodes into the graph.")

    def load_edges_from_csv(self, file_path):
        """Reads connection data and connects the nodes."""
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                from_id = row['from_station_id']
                to_id = row['to_station_id']
                weight = int(row['weight'])
                if from_id in self.nodes and to_id in self.nodes:
                    from_node = self.nodes[from_id]
                    to_node = self.nodes[to_id]
                    from_node.neighbors[to_node] = weight
                    count += 1
        print(f"Loaded {count} edges, connecting the nodes.")

    # --- ADDED THIS METHOD TO PRINT THE GRAPH ---
    def print_graph(self):
        """Prints all Metro stations and their connections in a readable format."""
        print("\n--- Mexico City Metro Network Structure ---")
        if not self.nodes:
            print("Metro network is empty.")
            return

        # Iterate through each Metro station in the graph, sorted by ID for consistency
        for station_id in sorted(self.nodes.keys()):
            node = self.nodes[station_id]
            print(f"\nStation: {node.name} ({node.id})")
            if not node.neighbors:
                print("  -> No outgoing connections.")
            else:
                # Print all connections for the current Metro station
                for neighbor, weight in node.neighbors.items():
                    print(f"  -> connects to {neighbor.name} (cost: {weight})")

    def calculate_total_weight(self):
        """Calculates and returns the total weight of all edges in the Metro network."""
        total_weight = 0
        edge_count = 0
        
        for station in self.nodes.values():
            for neighbor, weight in station.neighbors.items():
                total_weight += weight
                edge_count += 1
        
        print(f"\nMetro Network Weight Statistics:")
        print(f"Total number of edges: {edge_count}")
        print(f"Total weight of all edges: {total_weight}")
        
        return total_weight

    def print_metro_lines_and_transfers(self):
        """Prints every metro line with their stations and possible transfers (transbordos)."""
        print("\n" + "="*70)
        print("MEXICO CITY METRO LINES AND TRANSFERS (TRANSBORDOS)")
        print("="*70)
        
        # Organize stations by line
        metro_lines = {}
        for station in self.nodes.values():
            if 'Metro' in station.systems:
                for line in station.lines:
                    if line not in metro_lines:
                        metro_lines[line] = []
                    metro_lines[line].append(station)
        
        # Sort stations within each line (you might want to improve this ordering)
        for line in metro_lines:
            metro_lines[line].sort(key=lambda x: x.name)
        
        # Print each line with transfer information
        for line in sorted(metro_lines.keys()):
            stations = metro_lines[line]
            print(f"\nLINE {line} ({len(stations)} stations)")
            print("─" * 50)
            
            transfer_stations = []
            regular_stations = []
            
            for station in stations:
                if len(station.lines) > 1:
                    transfer_stations.append(station)
                else:
                    regular_stations.append(station)
            
            # Print transfer stations first
            if transfer_stations:
                print(f"\n TRANSFER STATIONS ({len(transfer_stations)}):")
                for station in transfer_stations:
                    other_lines = [l for l in station.lines if l != line]
                    lines_str = ", ".join(f"Line {l}" for l in other_lines)
                    print(f"   {station.name}")
                    print(f"     └─ Connected with: {lines_str}")
            
            # Print regular stations
            if regular_stations:
                print(f"\n REGULAR STATIONS ({len(regular_stations)}):")
                for i, station in enumerate(regular_stations):
                    print(f"  {i+1:2d}. {station.name}")
        
        # Summary of all transfers
        print(f"\n" + "="*70)
        print("CONNECTIONS SUMMARY")
        print("="*70)
        
        all_transfer_stations = [station for station in self.nodes.values() 
                               if 'Metro' in station.systems and len(station.lines) > 1]
        
        all_transfer_stations.sort(key=lambda x: len(x.lines), reverse=True)

        print(f"\nTotal transfer stations: {len(all_transfer_stations)}")
        print(f"\n STATIONS WITH MORE CONNECTIONS:")
        
        for station in all_transfer_stations:
            lines_str = ", ".join(f"LLine {l}" for l in station.lines)
            print(f" {station.name} ({len(station.lines)} lines)")
            print(f"     └─ {lines_str}")
        
    def validate_metro_network(self):
        """Validates the metro network structure and provides detailed analysis."""
        print("\n" + "="*60)
        print("METRO NETWORK VALIDATION REPORT")
        print("="*60)
        
        # 1. Basic Statistics - Only Metro stations
        metro_stations = [node for node in self.nodes.values() if 'Metro' in node.systems]
        
        print(f"\n BASIC STATISTICS:")
        print(f"Total Metro stations: {len(metro_stations)}")
        
        # 2. Metro Lines Analysis
        print(f"\n METRO LINES ANALYSIS:")
        metro_lines = {}
        for station in metro_stations:
            for line in station.lines:
                if line not in metro_lines:
                    metro_lines[line] = []
                metro_lines[line].append(station)
        
        print(f"Metro lines found: {sorted(metro_lines.keys())}")
        for line in sorted(metro_lines.keys()):
            print(f"  Line {line}: {len(metro_lines[line])} stations")
        
        # 3. Connectivity Analysis
        print(f"\n CONNECTIVITY ANALYSIS:")
        isolated_stations = []
        stations_with_connections = []
        hub_stations = []
        
        for station in self.nodes.values():
            if len(station.neighbors) == 0:
                isolated_stations.append(station)
            elif len(station.neighbors) >= 3:
                hub_stations.append(station)
            else:
                stations_with_connections.append(station)
        
        print(f"Isolated stations (no connections): {len(isolated_stations)}")
        print(f"Regular stations (1-2 connections): {len(stations_with_connections)}")
        print(f"Hub stations (3+ connections): {len(hub_stations)}")
        
        # 4. List isolated stations (problematic)
        if isolated_stations:
            print(f"\n  ISOLATED STATIONS (NEED CONNECTIONS):")
            for station in isolated_stations:
                print(f"  - {station.name} ({station.id})")
        
        # 5. List hub stations (transfer points)
        if hub_stations:
            print(f"\n HUB STATIONS (TRANSFER POINTS):")
            for station in sorted(hub_stations, key=lambda x: len(x.neighbors), reverse=True):
                print(f"  - {station.name}: {len(station.neighbors)} connections")
        
        # 6. Data integrity
        print(f"\n DATA INTEGRITY:")
        print(f"Metro stations loaded successfully: {len(self.nodes) > 0}")
        
        # 7. Edge validation
        total_edges = sum(len(node.neighbors) for node in self.nodes.values())
        print(f"Total directed edges: {total_edges}")
        
        # 8. Check for bidirectional connections
        bidirectional_count = 0
        unidirectional_edges = []
        
        for station in self.nodes.values():
            for neighbor, weight in station.neighbors.items():
                # Check if the reverse connection exists
                if station in neighbor.neighbors:
                    if neighbor.neighbors[station] == weight:
                        bidirectional_count += 1
                else:
                    unidirectional_edges.append((station.name, neighbor.name, weight))
        
        print(f"Bidirectional connections: {bidirectional_count // 2}")  # Divide by 2 since we count each twice
        
        if unidirectional_edges:
            print(f"\n UNIDIRECTIONAL CONNECTIONS:")
            for from_station, to_station, weight in unidirectional_edges[:10]:  # Show first 10
                print(f"  - {from_station} → {to_station} (weight: {weight})")
        
        print(f"\n METRO NETWORK VALIDATION COMPLETE")
        return {
            'total_stations': len(self.nodes),
            'metro_stations': len(metro_stations),
            'isolated_stations': len(isolated_stations),
            'hub_stations': len(hub_stations),
            'metro_lines': len(metro_lines)
        }
    
    def find_target_node(self, name):
        for node in self.nodes.values():
            if node.name.lower() == name.lower():
                return node
        return None

    def dijkstra(self, start_name, end_name):
        initial_node = self.find_target_node(start_name)
        if not initial_node:
            print(f"Station '{start_name}' not found.")
            return
        final_node = self.find_target_node(end_name)
        if not final_node:
            print(f"Station '{end_name}' not found.")
            return
        dist = {node.name: sys.maxsize for node in self.nodes.values()}
        previous = {node.name: None for node in self.nodes.values()}
        not_visited = set(self.nodes.values())
        dist[initial_node.name] = 0

        while not_visited:
            current_node = min(not_visited, key=lambda node: dist[node.name])
            not_visited.remove(current_node)

            if current_node == final_node:
                break

            for neighbor, weight in current_node.neighbors.items():
                alt = dist[current_node.name] + weight
                if alt < dist[neighbor.name]:
                    dist[neighbor.name] = alt
                    previous[neighbor.name] = current_node.name
        
        path = []
        current = final_node.name
    
        # If there's no path to the destination
        if dist[final_node.name] == sys.maxsize:
            print(f"No path found from '{start_name}' to '{end_name}'")
            return None
    
        # Build path by following previous nodes backwards
        while current is not None:
            node = self.find_target_node(current)
            path.append(node)
            current = previous.get(current)

        # Reverse to get path from start to end
        path.reverse()
        
        # Return results
        total_distance = dist[final_node.name]
        path_names = [node.name for node in path]
        
        print(f"\nShortest path from '{start_name}' to '{end_name}':")
        print(f"Total wait time: {total_distance} minutes.")
        print(f"Path: {' → '.join(path_names)}")
        print(f"Number of stations: {len(path)}")
    



        


# --- Main execution block ---
if __name__ == "__main__":
    # 1. Create and load the Metro graph
    cdmx_metro = MetroGraph()
    #Remember to change the path to your own path
    cdmx_metro.load_nodes_from_csv('csv_files/nodes.csv')
    cdmx_metro.load_edges_from_csv('csv_files/edges.csv')
    print("\nMexico City Metro network successfully created.")

    # 2. Print metro lines and their transfers (transbordos)
    cdmx_metro.print_metro_lines_and_transfers()

    # 3. Validate the metro network
    validation_results = cdmx_metro.validate_metro_network()

    # 4. Calculate and display the total weight of the Metro graph
    total_weight = cdmx_metro.calculate_total_weight()

    # 5. Uncomment to print the entire graph structure (verbose)
    #cdmx_metro.print_graph()

    # 6. Search algorithm to find optimum path between stations.
    djikstra_result = cdmx_metro.dijkstra("Lindavista", "Zaragoza")
    print(djikstra_result)
