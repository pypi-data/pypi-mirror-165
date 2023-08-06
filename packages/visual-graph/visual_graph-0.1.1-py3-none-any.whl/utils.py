import networkx as nx
import random

def grid_layout(width, height, grid_width, grid_height):
  x_spacing = width / (grid_width - 1)
  y_spacing = height / (grid_height - 1)
  pos = {}
  for row in range(grid_height):
    for col in range(grid_width):
      node = row * grid_width + col
      pos[node] = (col * x_spacing, row * y_spacing)
  return pos
  
def create_bipartite_graph(nodes):
  top_nodes = round(random.uniform(0.3*nodes, 0.7*nodes))
  bottom_nodes = nodes - top_nodes
  edges = round(nodes + random.uniform(0.1*nodes, 0.3*nodes))

  graph = None
  while True:
    graph = nx.bipartite.gnmk_random_graph(top_nodes, bottom_nodes, edges)
    if nx.is_connected(graph):
      break
  return graph
  
def create_grid_graph(width, height):
    graph = nx.Graph() 
    id = 0
    for row in range(height):
      for col in range(width):
        graph.add_node(id)
        if col > 0:
          graph.add_edge(id - 1, id) # add horizantal edge
        if row > 0:
          graph.add_edge(id - width, id) # add vertical edge
        id += 1
    return graph