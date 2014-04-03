#Brain.py
#The Node classes would benefit slightly from inheritance, but I think it 
#will keep things simple if they are all seperate.  It is a small system,
#inheritance won't make that big of a difference.

#This is currently a sequential implementation

from tissue import InputNode, HiddenNode, Link, Activator
import pydot as pd
import warnings
import math

#------------------------------------------------------------------------------
class Brain():
  '''
  The 'Brain' is the controller for all the pieces of the FPNA.  The Nodes
  and the Links.  The brain essentially just calls the activate method of the
  nodes and links in the correct order for proper operation.  It is basically
  just a state machine that drives the nodes and links.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, name = None)
    '''
    '''
    assert(name, str) or name == None, 'name must be a string'
    self.name = name
    self.inputNodes = []
    self.hiddenNodes = []
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.name

  #----------------------------------------------------------------------------
  def activate(self):
    return

  #---------------------------------------------------------------------------- 
  def addInputNode(self, c = None, name = None):
    if c == None:
      c = rawInput('Number of inputs that will be sent to this node?')
      if c == '':
        c = 1
      c = int(c)

    if name == None:
      name = rawInput('Node Name?')
      if name == '':
        name = 'InputNode%d' %len(inputNodes)

    self.inputNodes.append(InputNode(c, name))
    return
  
  #---------------------------------------------------------------------------- 
  def addHiddenNode(self, activator = None, theta = None, a = None, 
                    name = None):
    if activator == None:
      activator = self.createActivator()

    if Theta == None:
      theta = rawInput('Initial x value?')
      if theta == '':
        theta = 0
      theta = int(theta)
      
    if a == None:
      a = rawInput('Number of iterations before activation function applied?')
      if a == '':
        a = 1
      a = int(a)

    if name == None:
      name = rawInput('Node name?')
      if name == '':
        name = 'HiddenNode%d' %len(hiddenNodes)
    self.hiddenNodes.append(HiddenNode(

  #---------------------------------------------------------------------------- 
  def printNet(self):
    '''
    Uses a graphviz api to create a visual representation of the FPNA.
    '''
    raise NotImplementedError
    G = pd.Dot(graph_type='digraph')
    for n in self.N:
      if isinstance(n, InputNode):
        self.extendGraph(n, G)
    G.write_png('test.png')
    return

  #---------------------------------------------------------------------------- 
  def extendGraph(self, N, G):
    '''
    Recursively extends the graph layout by traversing the FPNA.  
    N: The node
    G: The graph
    '''
    raise NotImplementedError
    if N == None:
      return
    for L in N.getOutputConnections():
      print str(N) + '->' + str(L.getOutputNode())
      e = pd.Edge(str(N), str(L.getOutputNode()))
      G.add_edge(e)
      self.extendGraph(L.getOutputNode(), G)
      """
    for L in N.getVLinks():
      print L.getInputNode()
      print str(N) + '->' + str(L.getOutputNode())
      e = pd.Edge(str(N), str(L.getOutputNode()), set_label = 'vLink')
      G.add_edge(e)
      self.extendGraph(L.getOutputNode(), G)
      """
      return

#==============================================================================
def i(x, xp):
  return x + xp

def f(x):
  math.tanh(x)


