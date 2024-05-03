import osmnx as ox
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import math
import random

def a_star(graph, source, target):
    open_list = [(0, source)]  # Priority queue with (f, node)
    closed_set = set()
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes()}
    g_score[source] = 0

    while open_list:
        _, current = min(open_list)
        open_list.remove((_, current))

        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return path[::-1]

        closed_set.add(current)

        for neighbor in graph.neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + graph[current][neighbor][0]['length']
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score
                open_list.append((f_score, neighbor))

    return None  # No path found

# Define the main function
def main():
    st.title("Shortest Path Visualization")

    # Ask for user input for the place name
    place_name = st.text_input("Enter the place name (e.g., Palm Jumeirah, Dubai, UAE):")

    if place_name:
        # Retrieve the road network graph
        graph = ox.graph_from_place(place_name, network_type="drive")

        # Button to select different random points as source and target
        if st.button("Select Random Source and Target"):
            source = random.choice(list(graph.nodes()))
            target = random.choice(list(graph.nodes()))

            shortest_path = a_star(graph, source, target)
            print("Shortest path:", shortest_path)
            # Plot the graph and the shortest path
            nodes, _ = ox.graph_to_gdfs(graph)
            node_positions = {node: (data['x'], data['y']) for node, data in nodes.iterrows()}

            fig, ax = plt.subplots(facecolor='white')  # Set face color to white
            ox.plot_graph(graph, ax=ax, show=False, close=False)
            if shortest_path:

                other_nodes = [node for node in graph.nodes() if node not in shortest_path]
                nx.draw_networkx_nodes(graph, pos=node_positions, ax=ax, nodelist=other_nodes, node_color='blue', node_size=10)  # Highlight other nodes in blue
                nx.draw_networkx_nodes(graph, pos=node_positions, ax=ax, nodelist=shortest_path, node_color='red', node_size=30)
                nx.draw_networkx_edges(graph, pos=node_positions, ax=ax, arrows=False)  # Remove arrows
            st.pyplot(fig)

if __name__ == "__main__":
    main()
