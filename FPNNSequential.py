#FPNNSequential.py
import math

#------------------------------------------------------------------------------
class Link():
  '''
  This class defines a link.  It is an object that connects nodes together.
  Nodes contain lists of links and they manage the connections between links
  and activators.
  Functions:
  -connectAsPred() ret: None
  -connectAsSucc() ret: None
  -read() ret: self.output
  -write() ret: None
  Internal Variables:
  -(int, float): W
  -(int, float): T
  -Node: pred
  -Node: succ
  -(int, float): output
  -bool: inReady
  -bool: outReady
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, W, T):
    '''
    W: Weight for affine transform
    T: Weight for affine transform
    The transform is alpha : x -> Wx + T
    There are a lot of assertion statements.  These are for protection,
    any time an assertion fails it is treated as a fatal error.  It may be
    useful to define custom errors instead of using assertions for everything.
    '''
    assert isinstance(W, (int, float)), 'W must be a number'
    assert isinstance(T, (int, float)), 'T must be a number'
    self.W = W
    self.T = T
    self.output = 0 #This is the output value.  It is read with read()

    #The following values aren't really needed.  They are just helpful to
    #ensure correct operation and ensure nothing is happening that shouldn't
    self.pred = None #The predeccesor node
    self.succ = None #The successor node

    #outReady is a safety to prevent the same output being read multiple times.
    #outReady is False at init, set to true after an input has been received,
    #and set to false again after that output has been read.
    self.outReady = False

    #inReady is similar to outReady.  It is True at init, set to False when an
    #input is received, and reset to True when that output is read.
    self.inReady = True
    return

  #----------------------------------------------------------------------------  
  def connectAsPred(self, N):
    '''
    The Node 'N' connects to this Link as a predecessor.  That is, the node N
    will send it's outputs through this Link.  This link will only accept
    an input from the node connected as it's predecessor.
    '''
    assert isinstance(N, Node), 'N must be a Node'
    assert N != self.succ, 'Loopbacks are not allowed'
    self.pred = N
    return

  #----------------------------------------------------------------------------  
  def connectAsSucc(self, N):
    '''
    The Node 'N' connects to this Link as a successor.  That is, the node N
    will receive inputs from this Link.  This link will only allow it's output
    to be read by the node connected as it's successor.
    '''
    assert isinstance(N, Node), 'N must be a Node'
    assert N != self.pred, 'Loopbacks are not allowed'
    self.succ = N
    return

  #----------------------------------------------------------------------------  
  def read(self, N):
    '''
    This function 'reads' the output of the link.  It returns the output
    '''
    assert isinstance(N, Node), 'N must be a Node'
    assert N == self.succ, 'N must be my successor'
    assert self.outReady == True, 'This output is stale'
    self.outReady = False
    self.inReady = True
    return self.output

  #----------------------------------------------------------------------------  
  def write(self, x, N):
    '''
    This function takes in an input x and applies it\'s affine transform.  It
    then sets output: Wx + T
    '''
    assert isinstance(N, Node), 'N must be a Node'
    assert isinstance(x, (int, float)), 'x must be a number'
    assert N == self.pred, 'N must be my predecessor'
    assert self.inReady == True, 'The output hasn\'t been read yet'
    self.inReady = False
    self.outReady = True
    self.output = self.W*x + self.T
    return

#------------------------------------------------------------------------------
class Activator():
  '''
  This is an activator.  Nodes use activators to compute outputs.  Since many
  (most) Nodes will have the same type of activator, defining it as a
  seperate class makes things a little simpler.
  Functions:
  -iterator(), ret: defined by the iteration function self.i
  -activate(), ret: defined by the activation function self.f
  Internal Variables:
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, i, f):
    '''
    i: The iteration function
    f: The final output function
    '''
    assert hasattr(i, '__call__'), 'i must be a function'
    assert hasattr(f, '__call__'), 'f must be a function'
    self.i = i
    self.f = f
    return

  #----------------------------------------------------------------------------  
  def iterator(self, x):
    '''
    Calls the iterator function i on x and returns i's return.
    No error handling happens here.
    '''
    return self.i(x)

  #----------------------------------------------------------------------------  
  def activate(self, x):
    '''
    Calls the activation function f on x and returns f's return.
    No error handling happens here.
    '''
    return self.f(x)

#------------------------------------------------------------------------------
class Node():
  '''
  Nodes are connected to numerous links, and contain an activator.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, succ = (None,)): 
    assert isinstance(activator, Activator), 'activator must be an Activator'
    assert isinstance(succ, tuple), 'succ must be a tuple'
    assert (isinstance(succ[0], Link) or 
            succ[0] is None), 'succ must contain Links'

    self.activator = activator
    self.succ = succ

    return


#------------------------------------------------------------------------------
class InputNode(Node):
  '''
  An input node
  '''
  def __init__(self, activator, c = 0, succ = (None,), ):
    '''
    activator: The activator class contained by this node
    c: The number of inputs
    succ: A tuple of successors, this defines it's connections
    '''
    Node.__init__(self, activator = activator, succ = succ)
    assert isinstance(c, int) and c >= 0, 'c must be an int >= 0'
    self.c = c
    return

#------------------------------------------------------------------------------
class HiddenNode(Node):
  '''
  A hidden node
  '''
  def __init__(self, activator, pred = (None,), succ = (None,), 
               vLinks = ((None, None),), theta = 0, a = 1):
    assert isinstance(pred, tuple), 'pred must be a tuple'
    assert (isinstance(pred[0], Link) or 
            pred[0] is None), 'pred must contain Links'

    assert isinstance(vLinks, tuple), 'vLinks must be a tuple of tuples'
    assert isinstance(vLinks[0], tuple), 'vLinks must be a tuple of tuples'
    assert (isinstance(vLinks[0][0], Link) or 
            vLinks[0][0] is None), 'vLinks must contain Links'

    assert isinstance(theta, (int, float)), 'theta must be a number'
    assert isinstance(a, int) and a > 0, 'a must be a number > 0'

    Node.__init__(self, activator, succ)

    self.pred = pred
    self.vLinks = vLinks
    self.a = a
    self.theta = theta

    self.x = 0
    self.c = 0
    return

#------------------------------------------------------------------------------
class OutputNode(Node):
  '''
  An output node
  '''
  def __init__(self, activator, pred = (None,), succ = (None,), 
               theta = 0, a = 1):
    assert isinstance(pred, tuple), 'pred must be a tuple'
    assert (isinstance(pred[0], Link) or 
            pred[0] is None), 'pred must contain Links'

    assert isinstance(theta, (int, float)), 'theta must be a number'
    assert isinstance(a, int) and a > 0, 'a must be a number > 0'
    
    Node.__init__(self, activator, succ)
    self.pred = pred
    self.a = a
    self.theta = theta

    self.x = 0
    self.c = 0

    return



#program entry
#==============================================================================
def i(x, xp):
  return x + xp

def f(x):
  return math.tanh(x)

def f5(x):
  return x

n1n3 = Link(3, 4)
n2n3 = Link(6, 5)
n2n4 = Link(8, 6)
n3n4 = Link(12, 7)
n3n5 = Link(15, 8)
n4n5 = Link(20, 9)
n5n3 = Link(15, 8)
A = Activator(i, f)
A5 = Activator(i, f5)

c1 = 2
c2 = 1

n1 = InputNode(activator = A, succ = (n1n3,)) #input node
n2 = InputNode(activator = A, succ = (n2n3, n2n4)) #input node

n3 = HiddenNode(activator = A, pred = (n2n3, n5n3), vLinks = ((n1n3, n3n4),),
          theta = 2.1, a = 3)
n4 = HiddenNode(activator = A, pred = (n2n4, n3n4), succ = (n4n5,), theta = -1.9,
          a = 2)
n5 = OutputNode(activator = A5, pred = (n3n5, n4n5), theta = 0, a = 2)

Ni = (n1, n2)
N = (n3, n4, n5)
E = (n1n3, n2n3, n2n4, n3n4, n3n5, n4n5, n5n3)

