import sqlite3
import matplotlib.pyplot as plt
import networkx as nx

def create_mind_map():
    # Connect to SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Fetch all thoughts
    cursor.execute("SELECT id, thought FROM thoughts")
    thoughts = cursor.fetchall()
    thought_ids = {row[0]: row[1] for row in thoughts}
    
    # Add nodes to the graph
    for thought_id, thought_text in thought_ids.items():
        G.add_node(thought_id, label=thought_text)
    
    # Fetch all relationships
    cursor.execute("SELECT parent_thought_id, child_thought_id, relationship_type FROM relationships")
    relationships = cursor.fetchall()
    
    # Add edges to the graph
    for parent_id, child_id, _ in relationships:
        if parent_id in thought_ids and child_id in thought_ids:
            G.add_edge(parent_id, child_id)
    
    # Draw the graph
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=False, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)
    
    plt.title("Mind Map Visualization")
    plt.show()
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    create_mind_map()
