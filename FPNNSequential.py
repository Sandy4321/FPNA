#FPNNSequential.py
import math

#------------------------------------------------------------------------------
class Link():
  '''
  This class defines a link.  It is an object that connects nodes together.
  Nodes contain lists of links and they manage the connections between links
  and activators.
  Functions:
  -activate()
  -connectToInput()
  -connectToOutput()
  Internal Variables:
  -(float): W
  -(float): T
  -Node: pred
  -Node: succ
  -(float): output
  -bool: inReady
  -bool: outReady
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, W, T, name = None):
    '''
    W: Weight for affine transform
    T: Weight for affine transform
    The transform is alpha : x -> Wx + T
    There are a lot of assertion statements.  These are for protection,
    any time an assertion fails it is treated as a fatal error.  It may be
    useful to define custom errors instead of using assertions for everything.
    '''
    assert isinstance(W, (float)), 'W must be a float'
    assert isinstance(T, (float)), 'T must be a float'
    assert isinstance(name, str) or name == None, 'name must be a string'
    self.W = W
    self.T = T
    self.output = 0 #This is the output value.  It is read with read()
    self.inputNode = None #Predecessor node
    self.outputNode = None #Successor node
    self.name = name
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def activate(self, x):
    '''
    Simply returns the value calculated by this link
    x: A number
    '''
    assert isinstance(x, (float)), 'x must be a float'
    return self.W*x + self.T

  #----------------------------------------------------------------------------  
  def connectToInput(self, N):
    '''
    Connects node N to connect to the input of this link.
    '''
    assert isinstance(N, (InputNode, HiddenNode)), 'N must be a node'
    assert N != self.outputNode, 'Loopbacks are not allowed'
    self.inputNode = N
    return

  #----------------------------------------------------------------------------  
  def connectToOutput(self, N):
    '''
    Connects node N to the output of this link.
    '''
    assert isinstance(N, (OutputNode, HiddenNode)), 'N must be a node'
    assert N != self.inputNode, 'Loopbacks are not allowed'
    self.outputNode = N
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
  def __init__(self, i, f, name = None):
    '''
    i: The iteration function
    f: The final output function
    '''
    assert hasattr(i, '__call__'), 'i must be a function'
    assert hasattr(f, '__call__'), 'f must be a function'
    assert isinstance(name, str) or name == None, 'name must be a string'
    self.i = i
    self.f = f
    self.name = name
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def iterate(self, x):
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
class InputNode():
  '''
  An input node
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, c = 0, succ = (None,), name = None):
    '''
    activator: The activator class contained by this node
    c: The number of inputs
    succ: A tuple of successors, this defines it's connections
    '''
    assert isinstance(activator, Activator), 'activator must be an Activator'
    assert isinstance(succ, tuple), 'succ must be a tuple'
    assert (isinstance(succ[0], Link) or 
            succ[0] is None), 'succ must contain Links'

    assert isinstance(name, str) or name == None, 'name must be a string'
    self.activator = activator
    self.succ = succ
    for s in [s for s in self.succ if s != None]:
      s.connectToInput(self)

    assert isinstance(c, int) and c >= 0, 'c must be an int >= 0'
    self.c = c
    self.name = name
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()
 
#------------------------------------------------------------------------------
class HiddenNode():
  '''
  A hidden node
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, pred = (None,), succ = (None,), 
               vLinks = ((None, None),), theta = 0, a = 1, name = None):
    '''
    activator: The activator class contained by this node
    pred: Tuple of predecessor Links
    succ: Tuple of successor Links
    vLinks: Tuple of tuples of Links that are configured as virtual links.
    theta: Starting value for x
    a: Number of iterations of activator's iteration function.
    '''

    assert isinstance(activator, Activator), 'activator must be an Activator'
    assert isinstance(succ, tuple), 'succ must be a tuple'
    assert (isinstance(succ[0], Link) or 
            succ[0] is None), 'succ must contain Links'


    assert isinstance(pred, tuple), 'pred must be a tuple'
    assert (isinstance(pred[0], Link) or 
            pred[0] is None), 'pred must contain Links'

    assert isinstance(vLinks, tuple), 'vLinks must be a tuple of tuples'
    assert isinstance(vLinks[0], tuple), 'vLinks must be a tuple of tuples'
    assert (isinstance(vLinks[0][0], Link) or 
            vLinks[0][0] is None), 'vLinks must contain Links'

    assert isinstance(theta, (float)), 'theta must be a float'
    assert isinstance(a, int) and a > 0, 'a must be a number > 0'
    
    assert isinstance(name, str) or name == None, 'name must be a string'

    self.succ = succ
    for s in [s for s in self.succ if s != None]:
      s.connectToInput(self)

    self.pred = pred
    for p in [p for p in self.pred if p != None]:
      p.connectToOutput(self)

    self.vLinks = vLinks
    for vl in [vl for vl in self.vLinks if not None in vl]:
      vl[0].connectToOutput(self)
      vl[1].connectToInput(self)

    self.activator = activator
    self.a = a
    self.theta = theta
    self.name = name
    self.x = theta
    self.c = 0
    return

  #----------------------------------------------------------------------------
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------
  def activate(self, xp):
    self.c += 1
    self.x = self.activator.iterate([self.x, xp])
    if self.c == self.a:
      self.c = 0
      y = self.activator.activate(self.x)
      self.x = self.theta
      return y
    else:
      return None

#------------------------------------------------------------------------------
class OutputNode():
  '''
  An output node
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, pred = (None,), theta = 0, a = 1, name = None):
    '''
    activator: The activator Class contained by this node.
    pred: A tuple of predecessor links.
    succ: A tuple of successor links.
    theta: The initial value of x.
    a: The number of times to apply the activator's iteration function.
    '''
    assert isinstance(activator, Activator), 'activator must be an Activator'

    assert isinstance(pred, tuple), 'pred must be a tuple'
    assert (isinstance(pred[0], Link) or 
            pred[0] is None), 'pred must contain Links'

    assert isinstance(theta, (float)), 'theta must be a float'
    assert isinstance(a, int) and a > 0, 'a must be a number > 0'
    
    assert isinstance(name, str) or name == None, 'name must be a string'

    self.pred = pred
    for p in [p for p in self.pred if p != None]:
      p.connectToOutput(self)

    self.a = a
    self.theta = theta
    self.activator = activator
    self.x = theta
    self.c = 0
    self.name = name

    return

  #----------------------------------------------------------------------------
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------
  def activate(self, xp):
    self.c += 1
    self.x = self.activator.iterate([self.x, xp])
    if self.c == self.a:
      self.c = 0
      y = self.activator.activate(self.x)
      self.x = self.theta
      return y
    else:
      return None

#------------------------------------------------------------------------------
class Brain():
  '''
  The FPNN.  This class controls all of the nodes and links.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, Ni = (None,), Nh = (None,), No = (None,), name = None):
    '''
    Allowing Ni or No to remain None is illegal.  It is only there to
    demonstrate the form the input needs to be.
    Ni: A tuple of InputNodes.
    Nh: A tuple of HiddenNodes.
    No: A tuple of OutputNodes
    The should already be initialized properly in the Nodes.
    '''
    assert isinstance(Ni, tuple), 'Ni must be a tuple of InputNodes'
    assert isinstance(Ni[0], InputNode), 'Ni must be a tuple of InputNodes'
    assert isinstance(No, tuple), 'No must be a tuple of OutputNodes'
    assert isinstance(No[0], OutputNode), 'No must be a tuple of OutputNodes'
    assert isinstance(Nh, tuple), 'Nh must be a tuple'
    assert (isinstance(Nh[0], HiddenNode) or 
            Nh[0] is None), 'Nh must contain HiddenNodes or (None,)'

    assert isinstance(name, str) or name == None, 'name must be a string'
    
    self.Ni = Ni
    self.Nh = Nh
    self.No = No
    self.L = []
    self.name = name
    
    self.inputs = []
    
    for n in Ni:
      nInputs = [None]*n.c
      self.inputs.append(nInputs)
    
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def activate(self, inputValues = [[]]):
    if (not [len(x) for x in self.inputs] == [len(x) for x in inputValues]):
      raise AssertionErorr('You must pass n.c values to each InputNode ' +
                           'as nested lists.  [[n1.c ...], [n2.c ...], ...]')
    #Creates the task list
    Y = [0]*len(self.No)
    print Y
    i = 0
    for n in Ni:
      for s in n.succ:
        for x in inputValues[i]:
          self.L.append((s, x))
      i += 1

    print self.L

    while any(self.L):
      task = self.L.pop(0)
      link = task[0]
      n = link.outputNode
      x = task[1]
      xp = link.activate(x)
      if not isinstance(n, (InputNode, OutputNode)):
        for vl in n.vLinks:
          if link == vl[0]:
            self.L.append((vl[1], xp))
      
      if link in n.pred:
        y = n.activate(xp)
        if y != None:
          if isinstance(n, OutputNode):
            Y[self.No.index(n)] = y
          for s in n.succ:
            self.L.append((s, y))
      
      print self.L
    return Y

#program entry
#==============================================================================
def i(x):
  return x[0] + x[1]

def f(x):
  return math.tanh(x)

def f5(x):
  return x

n1n3 = Link(3.0, 4.0, name = 'n1n3')
n2n3 = Link(6.0, 5.0, name = 'n2n3')
n2n4 = Link(8.0, 6.0, name = 'n2n4')
n3n4 = Link(12.0, 7.0, name = 'n3n4')
n3n5 = Link(15.0, 8.0, name = 'n3n5')
n4n5 = Link(20.0, 9.0, name = 'n4n5')
n5n3 = Link(15.0, 8.0, name = 'n5n3')
A = Activator(i, f, name = 'A')
A5 = Activator(i, f5, name = 'A5')

c1 = 2
c2 = 1

n1 = InputNode(activator = A, c = 2, succ = (n1n3,), name = 'n1')
n2 = InputNode(activator = A, c = 1, succ = (n2n3, n2n4), name = 'n2')

n3 = HiddenNode(activator = A, pred = (n2n3, n5n3), vLinks = ((n1n3, n3n4),),
          theta = 2.1, a = 3, name = 'n3')
n4 = HiddenNode(activator = A, pred = (n2n4, n3n4), succ = (n4n5,), theta = -1.9,
          a = 2, name = 'n4')
n5 = OutputNode(activator = A5, pred = (n3n5, n4n5), theta = 0.0, 
                a = 2, name = 'n4')

Ni = (n1, n2)
Nh = (n3, n4)
No = (n5,)
E = (n1n3, n2n3, n2n4, n3n4, n3n5, n4n5, n5n3)

brain = Brain(Ni, Nh, No)

X = [[1.5, -0.8], [1.1]]
print brain.activate(X)

