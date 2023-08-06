class VisualNode:
  """
  A node containing a value and belonging to a graph.
  """

  _instances = {} # map of values to instances
  _initialised = set() # set of values for which instances have been initialised
  def __new__(cls, *args, **kwargs):
    # only allow one Node instance per value
    value = args[0]
    if value in cls._instances:
      return cls._instances[value]
    instance = super().__new__(cls)
    cls._instances[value] = instance
    return instance
  
  def __init__(self, value, graph=None):
    """
    Parameters
    ----------
    value : int
        The value of the Node
    graph : DrawableGraph
        The graph the Node belongs to
    """
    if value in self._initialised:
      return
    self.value = value
    assert graph is not None, f"Node({value}) does not exist"
    self._graph = graph
    self._initialised.add(value)

  def __repr__(self):
    return f"VisualNode({self.value})"

  def __hash__(self):
    return hash(self.value)
    
  def __eq__(self, other):
    return self.value == other.value

  def __gt__(self, other):
    return self.value > other.value

  def _get_attribute(self, name):
    return self._graph._graph.nodes[self.value].get(name)

  def _set_attribute(self, name, value):
    self._graph._graph.nodes[self.value][name] = value

  @property
  def colour(self):
    """string representing the colour of this Node"""
    return self._get_attribute("colour")

  @colour.setter
  def colour(self, colour):
    self._set_attribute("colour", colour)
    if self._graph._auto_redraw:
      self._graph.draw()

  def connect(self, node):
    """Add an edge to the provided node

    Parameters
    ----------
    node : VisualNode
       Node to connect to
    """
    self._graph.connect(self, node)

  @property
  def neighbours(self):
    """list of Nodes neigbouring this Node in the graph"""
    nx_neighbours = self._graph._graph.neighbors(self.value)
    return [self._graph._nodes[neighbour] for neighbour in nx_neighbours]
