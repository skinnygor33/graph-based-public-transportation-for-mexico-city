import csv
from stationNode import StationNode

class TransitGraph:
    """Represents the entire transportation network."""
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
        """Prints all nodes and their connections in a readable format."""
        print("\n--- Transit Graph Structure ---")
        if not self.nodes:
            print("Graph is empty.")
            return

        # Iterate through each node in the graph, sorted by ID for consistency
        for station_id in sorted(self.nodes.keys()):
            node = self.nodes[station_id]
            print(f"\nNode: {node.name} ({node.id})")
            if not node.neighbors:
                print("  -> No outgoing connections.")
            else:
                # Print all connections for the current node
                for neighbor, weight in node.neighbors.items():
                    print(f"  -> connects to {neighbor.name} (cost: {weight})")


# --- Main execution block ---
if __name__ == "__main__":
    # 1. Create and load the graph
    cdmx_graph = TransitGraph()
    #Remember to change the path to your own path
    cdmx_graph.load_nodes_from_csv('/Users/emiliamacarenarodriguezlavarriosarriaga/Desktop/Lab2/graph-based-public-transportation-for-mexico-city/csv_files/nodes.csv')
    cdmx_graph.load_edges_from_csv('/Users/emiliamacarenarodriguezlavarriosarriaga/Desktop/Lab2/graph-based-public-transportation-for-mexico-city/csv_files/edges.csv')
    print("\nGraph successfully created.")

    # 2. Print the entire graph structure
    cdmx_graph.print_graph()