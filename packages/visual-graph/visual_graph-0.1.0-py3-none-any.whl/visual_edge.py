class VisualEdge:
  def __init__(self, node1, node2, graph):
    self.node1 = node1
    self.node2 = node2
    self._graph = graph
    self.value  = 3

  def __repr__(self):
    return f"Edge({self.node1}, {self.node2})"

  def set_attribute(self, name, value):
    self._graph._graph[self.node1][self.node2][name] = value
    
  def get_attribute(self, name, default=None):
    return self._graph._graph.get_edge_data(self.node1, self.node2, {}).get(name, default) 