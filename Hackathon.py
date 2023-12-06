import pandas as pd
import networkx as nx

# Load the dataset
df = pd.read_csv("Path sample gen.xlsx - Vehicle Routes.csv")

# Remove rows with empty values in 'Time to Next Stop'
df = df.dropna(subset=['Time to Next Stop'])

# Create a directed graph using NetworkX
G = nx.DiGraph()

# Add edges to the graph based on the data
for i in range(len(df) - 1):
    source_stop = df.iloc[i]['Stop']
    target_stop = df.iloc[i + 1]['Stop']
    route_id = df.iloc[i]['Route ID']
    time_to_next_stop = df.iloc[i]['Time to Next Stop']
    postcode = df.iloc[i]['Postcode']
    
    G.add_edge(source_stop, target_stop, route_id=route_id, time_to_next_stop=time_to_next_stop, postcode=postcode)

# Function to find the shortest path between two stops using A* algorithm
def find_shortest_path(graph, stops):
    shortest_path = []
    total_distance = 0

    for i in range(len(stops) - 1):
        start_stop = stops[i]
        end_stop = stops[i + 1]

        try:
            path = nx.astar_path(graph, source=start_stop, target=end_stop, heuristic=None)
            distance = nx.astar_path_length(graph, source=start_stop, target=end_stop)
            shortest_path.extend(path[1:])  # Skip the first stop to avoid duplication
            total_distance += distance
        except nx.NetworkXNoPath:
            return None, None

    return shortest_path, total_distance

# User input for five stops
stops = []
n = int(input("Number of Stops: "))
for i in range(n):
    stop_input = input(f"Enter stop {i + 1}: ")
    stops.append(stop_input)

# Find the shortest path for the given stops
shortest_path, total_distance = find_shortest_path(G, stops)

# Display the result
if shortest_path:
    print(f"Shortest path between the given stops:")
    for i in range(len(shortest_path) - 1):
        route_id = G[shortest_path[i]][shortest_path[i + 1]]['route_id']
        postcode = G[shortest_path[i]][shortest_path[i + 1]]['postcode']
        print(f"  From {[shortest_path[i]]} to {[shortest_path[i + 1]]}")
        print(f"      (Route ID: {route_id}), (Postcode: {postcode})")
else:
    print("No path found between the given stops.")
