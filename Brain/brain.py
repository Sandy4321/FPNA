#Brain.py
#The Node classes would benefit slightly from inheritance, but I think it 
#will keep things simple if they are all seperate.  It is a small system,
#inheritance won't make that big of a difference.

#This is currently a sequential implementation

from tissue import InputNode, HiddenNode, Link, Activator
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
  def __init__(self, N, E, name = None):
    '''
    N: A list defining the constants for the NN.  Each element should be a 
    tuple (theta, a, A).  If theta is None that node should be an input node and
    then the value of a will be interpreted as c (number of inputs).  A
    should be an activator.
    E: An NxN matrix defining links, their connections, and their weights.
    pred(n) = E[*][n]
    succ(n) = E[n][*]
    if row r is is empty, then node r is an output
    if column c is empty, then node c is an input
    Each entry in E should be either None to indicate that there is no link
    or a tuple containing (W, T, r, S, [R]). Where [R] is a list of
    indices to indicate virtual links.  If E[n][m]'s [R] = [1,2] then there
    is a virtual link from E[n][m] to E[m][1] and E[m][2].  The order
    here matters.  E[n][m] -> E[m][1] and E[n][m] -> E[m][2].
    A: A length N array of activator classes.  Activator A[n] is assigned
    to Node n.
    '''
    assert isinstance(N, list), 'N must be a list'
    assert all([isinstance(t, (tuple,list)) for t in N])
    assert all([len(t) == 3 for t in N])
    assert all([(isinstance(x[0], float) or x[0] == None)
                and isinstance(x[1], int)
                and (isinstance(x[2], Activator)
                or x[2] == None) for x in N])

    assert all([isinstance(l, list) for l in E])
    n = len(N)
    for l in E:
      assert all([(x == None or x == ())
                  or (isinstance(x[0], float) and isinstance(x[1], float)
                  and isinstance(x[2], (bool)) and isinstance(x[3], bool)
                  and isinstance(x[4], list))
                  for x in l])
      assert all([isinstance(x, int) and x>=0 and x<=n  for x[4] in l])

    assert all([len(l) == n for l in E])
    assert name == None or isinstance(name, str), 'name should be a string'

    self.n = n #The number of nodes
    self.E = E
    self.A = A
    self.name = name

    self.buildNetwork()
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.name

  #----------------------------------------------------------------------------  
  def buildNetwork(self):
    '''
    Constructs a network based off of N, and E.
    '''
    #N: (theta, a, A)
    for i in range(len(self.N)):
      if(self.N[i][0] == None): #Input node
        assert (self.N[i][2] == None)
        self.N[i] = InputNode(n[i][1],'inN' + str(i))
      else:
        self.N[i] = Node(self.N[i][2], self.N[i][0], self.N[i][1],
                         'N' + str(i))

    E = [[]]
    i = 0
    for row in self.E:
      j = 0
      for l in row:
        if l == None or l == ():
          E[i].append(None)
        else:
          E[i].append(Link(l[0], l[1], 'L' + str(i) + str(j)))
        j += 1
      i += 1

    i = 0
    for row in self.E:
      j = 0
      for l in row:
        if l == None or l == ():
          pass
        else:
          self.N[j].bind(E[i][j], l[4], l[3])
          if l[2]:
            self.N[i].createconnection(E[i][j])
        j += 1
      i += 1

    self.E = E
    return

  #----------------------------------------------------------------------------  
  def activate(self):
    return

#==============================================================================
def i(x, xp):
  return x + xp

def f(x):
  math.tanh(x)

A = Activator(i, f, 'act')

#(theta, a, A)
#(W, T, r, S, [R])
#W = i*j
#T = i + j
N = [(None, 2, None), (None, 1, None), (2.1, 3, A), (-1.9, 2, A), (0.0, 2, A)]
E = [[(), (), (3,4,0,True,[4]), (), ()],
     [(), (), (6,5,True,True,[]), (8,6,True,True,[]), ()],
     [(), (), (), (12,7,True,False,[]), (15,8,True,True,[])],
     [(), (), (), (), (20,9,True,True,[])],
     [(), (), (15,8,True,False,[]), (), ()]]


B = Brain(N, E, 'I\m a Brain!')
