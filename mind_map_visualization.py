import sqlite3
import matplotlib.pyplot as plt
import networkx as nx
import logging

logging.basicConfig(level=logging.INFO)

def fetch_thoughts(cursor):
    cursor.execute("SELECT id, thought FROM thoughts")
    thoughts = cursor.fetchall()
    return {row[0]: row[1] for row in thoughts}

def fetch_relationships(cursor):
    cursor.execute("SELECT from_thought_id, to_thought_id, relationship_type FROM relationships")
    return cursor.fetchall()

def build_graph(thought_ids, relationships):
    G = nx.DiGraph()
    # Add nodes
    for thought_id, thought_text in thought_ids.items():
        G.add_node(thought_id, label=thought_text)
    # Add edges with relationship types
    edge_colors = []
    for from_id, to_id, relationship_type in relationships:
        if from_id in thought_ids and to_id in thought_ids:
            G.add_edge(from_id, to_id, relationship=relationship_type)
    return G

def draw_graph(G):
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    labels = nx.get_node_attributes(G, 'label')
    labels = {node: (text[:20] + '...') if len(text) > 20 else text for node, text in labels.items()}

    edge_colors = ['black' if G[u][v]['relationship'] == 'hierarchical' else 'red' for u, v in G.edges()]
    nx.draw(G, pos, with_labels=False, node_size=2000, node_color='skyblue',
            font_size=10, font_weight='bold', edge_color=edge_colors)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)

    plt.title("Mind Map Visualization")
    plt.show()

def create_mind_map(database_path='database.db'):
    logging.info("Starting mind map creation.")
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        thought_ids = fetch_thoughts(cursor)
        if not thought_ids:
            print("No thoughts found in the database.")
            return
        relationships = fetch_relationships(cursor)
        if not relationships:
            print("No relationships found in the database.")
        G = build_graph(thought_ids, relationships)
        draw_graph(G)
    logging.info("Mind map creation completed.")

if __name__ == "__main__":
    create_mind_map()
