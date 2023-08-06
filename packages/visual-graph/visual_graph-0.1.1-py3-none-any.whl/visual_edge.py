class VisualEdge:
  def __init__(self, node1, node2, graph):
    self.node1 = node1
    self.node2 = node2
    self._graph = graph

  def __repr__(self):
    return f"VisualEdge({self.node1}, {self.node2})"

  @property
  def value(self):
    return self._graph._graph.get_edge_data(self.node1, self.node2, {}).get("value", 0) 

  @value.setter
  def value(self, value):
    self._graph._graph[self.node1][self.node2]["value"] = value
