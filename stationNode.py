class StationNode:
    """Represents a single station in the transit network."""
    def __init__(self, station_id, name, systems, lines):
        # --- Core Attributes ---
        self.id = station_id      # Unique ID, e.g., 'zocalo_metro'
        self.name = name          # Official name, e.g., 'Zócalo/Tenochtitlan'
        self.systems = systems    # A list of systems, e.g., ['Metro']
        self.lines = lines        # A list of lines, e.g., ['Metro Line 2']

        # --- Graph Structure ---
        # This dictionary stores direct connections to other nodes
        # Format: {neighbor_node_object: weight}
        self.neighbors = {}

    # Helper method for the priority queue in the pathfinding algorithm
    def __lt__(self, other):
        return self.id < other.id

    # Print the node object
    def __repr__(self):
        return f"StationNode(Name: {self.name})"