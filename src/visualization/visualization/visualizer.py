"""
This file provides three methods that create the visualizations of the social networks.
"""
import networkx as nx
import matplotlib.pyplot as plt

def visualize_directed_graph(vertices: list[dict], edges: list[dict], output_path: str, output_file_name: str):
    # Extract resource names from the list of dictionaries for nodes
    node_names = [node['resource'] for node in vertices]

    G = nx.DiGraph()

    # Add nodes to the graph
    G.add_nodes_from(node_names)

    # Add edges to the graph (u = resource_performer, v = resource_consumer)
    G.add_edges_from([(edge['resource_performer'], edge['resource_consumer']) for edge in edges])

    # Layout for graph visualization
    fixed_positions = nx.spring_layout(G, seed=3000)
    pos = nx.spring_layout(G, pos=fixed_positions, k=4, seed=3000)

    plt.figure(figsize=(16, 9))

    # Get adjusted PageRank nodes
    page_rank_nodes = __get_pagerank(nodes=node_names, edges=edges)
    
    # Use PageRank values to scale node sizes, fallback to uniform size if mismatch
    if len(page_rank_nodes) == len(node_names):
        node_sizes = [3000 * node[1] for node in page_rank_nodes]
    else:
        print(f"PageRank size mismatch, falling back to uniform sizes")
        node_sizes = [3000] * len(node_names)

    # Ensure node sizes are float
    node_sizes = [float(size) for size in node_sizes]

    # Define colors
    colormap = plt.cm.get_cmap('tab20', len(node_names))
    node_colors = [colormap(i) for i in range(len(node_names))]

    # Draw network graph
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=0.8, arrows=True, edge_color='black', alpha=0.5, connectionstyle='arc3, rad=0.1')

    # Edge labels based on activities (reduced font size for edge labels)
    edge_labels = {(edge['resource_performer'], edge['resource_consumer']): edge['activity'] for edge in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=6)  # Reduced font size to 6

    # Node labels
    nx.draw_networkx_labels(G, pos, labels={node: node for node in node_names}, font_color='black', font_size=10)

    plt.axis('off')

    plt.tight_layout(rect=[0, 0, 0.9, 1])

    # Store the graph
    plt.savefig(output_path + output_file_name + ".png", dpi=300)
    plt.show()

def __get_pagerank(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from([(edge['resource_performer'], edge['resource_consumer']) for edge in edges])

    pr = nx.pagerank(G)

    # Update nodes list with PageRank scores
    nodes = [(node, pr[node]) for node in nodes]

    # Sort nodes by PageRank score in descending order
    page_ranked_nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    return page_ranked_nodes
