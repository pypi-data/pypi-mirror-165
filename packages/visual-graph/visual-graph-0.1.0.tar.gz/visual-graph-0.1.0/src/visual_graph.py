from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx
import os, time

from utils import grid_layout, create_bipartite_graph, create_grid_graph
from visual_node import VisualNode
from visual_edge import VisualEdge
 
class VisualGraph:
  """
  A graph with nodes and edges which can be drawn.
  """
  
  class GraphType(Enum):
    BIPARTITE = 0
    GRID = 1
  
  def __init__(self, type=GraphType.BIPARTITE, nodes=10, grid_width=4, grid_height=4, update_interval=1, width=6, height=4, ascii_mode=False, auto_redraw=True):
    """
    Parameters
    ----------
    type : VisualGraph.GraphType, optional (default=VisualGraph.GraphType.BIPARTITE)
        The type of graph. Options are:
          BIPARTITE: A randomly generated bipartite (two-colourable) graph
          GRID: A graph whose nodes are connected in a 2D grid/lattice pattern
    nodes : int, optional (default=10)
        The total number of nodes in BIPARTITE graph 
    grid_width : int, optional (default=4)
        The number of nodes wide for the GRID graph
    grid_height : int, optional (default=4)
        The number of nodes high for the GRID graph
    update_interval : float, optional (default=1)
        The time in seconds between drawing updates (set to 0 for instant updates)
    width : float, optional (default=4)
        The width in inches of the drawn graph
    height : float, optional (default=4)
        The height in inches of the drawn graph
    ascii_mode : boolean, optional (default=False)
        If True, render the graph as an ASCII graphic in a terminal.
    auto_redraw : boolean, optional (default=True)
        If True, redraw the graph whenever it changes 
    """
    self.update_interval = update_interval
    self._graph = None
    self._pos = None
    self._layout_function = None
    self._nodes = {}
    self._edges = {}
    self._height = height
    self._width = width
    self._grid_height = grid_height
    self._grid_width = grid_width
    self.edge_label_attribute = None
    self._ascii_mode = ascii_mode
    self._auto_redraw = auto_redraw

    VisualNode._instances = {}
    VisualNode._initialised = set()

    if self.ascii_mode:
      import matplotlib
      matplotlib.use('module://drawilleplot')

    #TODO validate figure and graph height and width values ...
    
    if type == VisualGraph.GraphType.BIPARTITE:
      #TODO log a warning if GRID details were supplied
      if not nodes:
        self._graph = nx.Graph()
        return
      self._graph = create_bipartite_graph(nodes)
      self._layout_function = lambda : nx.spring_layout(self._graph)
    elif type == VisualGraph.GraphType.GRID:
      #TODO log a warning if BIPARTITE details were supplied
      self._graph = create_grid_graph(self._grid_width, self._grid_height)
      self._layout_function = lambda : grid_layout(self._width, self._height, self._grid_width, self._grid_height)
    else:
      assert False, f"{type} is not a supported GraphType"

    self._pos = self._layout_function() 
    self._nodes = {value: VisualNode(value, self) for value in self._graph.nodes}
    self._edges = {(node1, node2): VisualEdge(node1, node2, self) for node1, node2 in self._graph.edges}

    # set up drawing 
    plt.figure().set_size_inches(self._width, self._height)
    if self._auto_redraw:
      self.draw(force_refresh=True)

  def create_node(self, value):
    """Create a Node with the provided value and add it two the graph

    Parameters
    ----------
    value : int
      Value of the Node
    """
    node = VisualNode(value, self)
    self._graph.add_node(value)
    self._nodes[value] = node #TODO make this a property
    return node

  def connect(self, node1, node2):
    """Add an edge between the two provided Nodes

    Parameters
    ----------
    node1 : VisualNode
      First node
    node2 : VisualNode
      Second node
    """
    self._graph.add_edge(node1.value, node2.value)
    self._edges[(node1.value, node2.value)] =  VisualEdge(node1.value, node2.value, self)

  def disconnect(self, node1, node2):
    """Remove the edge between the two provided Nodes

    Parameters
    ----------
    node1 : VisualNode
      First node
    node2 : VisualNode
      Second node
    """
    self._graph.remove_edge(node1.value, node2.value)
    self._edges.pop((node1.value, node2.value))

  def _get_attributes(self, name):
    nx_attributes =  nx.get_node_attributes(self._graph, name)
    return {node:nx_attributes.get(node) for node in self._nodes}

  def _set_attributes(self, name, attributes):
    nx.set_node_attributes(self._graph, attributes, name=name)

  @property
  def nodes(self):
    """list of Nodes in the graph"""
    return list(self._nodes.values())

  @property
  def edges(self):
    """list of edges in the graph"""
    return list(self._edges.values())

  def get_edge_between(self, node1, node2):
    """return the Edge between the two provided Nodes

    Parameters
    ----------
    node1 : VisualNode
      First node
    node2 : VisualNode
      Second node
    """
    if node1 > node2:
      node1, node2 = node2, node1 # reorder
    return self._edges[(node1.value, node2.value)]
  
  def get_node(self, value):
    """get a node from the graph

    Parameters
    ----------
    value : int
        value of the node to get 
       
    Returns
    -------
    Node
        the node with the given value if it exists, otherwise None
    """
    return self.nodes[value] if value in self._graph.nodes else None

  @property
  def colours(self):
    """dictionary mapping graph Nodes to their colours"""
    return self._get_attributes("colour") 

  @property
  def ascii_mode(self):
    """Returns whether the graph should be drawn as ASCII in the terminal"""
    return self._ascii_mode

  @property
  def auto_redraw(self):
    """Returns whether the graph should be automatically redrawn whenever it changes"""
    return self._auto_redraw

  @colours.setter
  def colours(self, value):
    self._set_attributes("colour", value)
    if self._auto_redraw:
      self.draw()

  def clear_colours(self):
    """clear the colours of all Nodes in graph"""
    self.colours = {node:None for node in self._nodes}
    if self._auto_redraw:
      self.draw()

  def _draw(self):
    colours = [colour if colour else "white" for colour in self.colours.values()]

    additional_kwargs = {}
    if self.ascii_mode:
      colour2width = {colour:(i*10+1) for i, colour in enumerate(sorted(list(set(colours) - {"white"})))}
      colour2width["white"] = 1
      additional_kwargs["verticalalignment"]   = "bottom"
      additional_kwargs["horizontalalignment"] = "left"
      additional_kwargs["linewidths"]          = [colour2width[colour] for colour in colours]

    nx.draw(self._graph, self._pos, with_labels=True, node_color=colours, edgecolors="black", **additional_kwargs)

    if self.edge_label_attribute:
      edge_labels = {nodes:edge.get_attribute(self.edge_label_attribute, 0) for nodes, edge in self._edges.items()}
      nx.draw_networkx_edge_labels(self._graph, edge_labels=edge_labels, pos=self._layout_function())

  def draw(self, force_refresh=False, force_layout_refresh=False):
    """draw the graph, or update the existing drawing if the graph has changed

    Parameters
    ----------
    force_refresh : boolean, optional (default=False)
       if True, clears the existing drawing before redrawing. Useful if edges or nodes have been removed since the last drawing.
    force_layout_refresh : boolean, optional (default=False)
       if True, recomputes the positions of the nodes before drawing. Useful if nodes have been added or removed since the last drawing. 
    """

    if force_refresh:
      plt.clf()
    if force_layout_refresh:
      self._pos = self._layout_function()

    if self.ascii_mode:
      plt.clf()
      os.system("clear")
    
    self._draw()

    if self.update_interval > 0:
      if self.ascii_mode:
        plt.show()
        time.sleep(self.update_interval)
      else:
        plt.pause(self.update_interval)
    else:
      if self.ascii_mode:
        plt.show()
      else:
        plt.show(block=False)
