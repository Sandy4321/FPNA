#Brain.py
#The Node classes would benefit slightly from inheritance, but I think it 
#will keep things simple if they are all seperate.  It is a small system,
#inheritance won't make that big of a difference.

#This is currently a sequential implementation

from tissue import InputNode, HiddenNode, OutputNode, Link, Activator

#------------------------------------------------------------------------------
class Brain():
  '''
  The 'Brain' is the controller for all the pieces of the FPNA.  The Nodes
  and the Links.  The brain essentially just calls the activate method of the
  nodes and links in the correct order for proper operation.  It is basically
  just a state machine that drives the nodes and links.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, N, E, A, rRS, name = None):
    '''
    N: An integer defining the number of nodes.
    E: An NxN matrix defining links, their connections, and their weights.
    If E[n][m] == (float, float) then a link (n,m) is created.
    It's connections are defined in the rRS matrix.
    A: A length N array of activator classes.  Activator A[n] is assigned
    to Node n.
    rRS: An NxN matrix defining the r, R, and S values for each node.
    '''
    assert isinstance(N, int), 'N must be an integer'
    assert all([isinstance(l, list) for l in E]), 'E must be a matrix'
    assert all([len(l) == N for l in E]), 'E must be NxN'
    assert (all([isinstance(a, Activator) for a in A]),
            'A should contain Activators')
    assert len(A) == N, 'A should be of length N'
    assert name == None or isinstance(name, str), 'name should be a string'
    self.N = N
    self.E = E
    self.A = A
    self.rRS = rRS
    self.name = name

    self.buildNetwork()
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def buildNetwork(self):
    '''
    Constructs a network based off of N, E, A, rRS.
    '''
    return

  #----------------------------------------------------------------------------  
  def activate(self):
    return

#==============================================================================
l = Link(1.0, 2.0)
