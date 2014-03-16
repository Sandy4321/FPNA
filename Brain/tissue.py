#tissue.py
#------------------------------------------------------------------------------
class InputNode():
  '''
  Input nodes take input from the brain, they simply pass values into the 
  network.  They don't apply any transforms.  Their registers are written into
  by the brain only.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, n, name = None):
    '''
    n: Number of inputs (registers)
    name: Name of this Node
    '''
    assert isinstance(name, str) or name == None, 'name must be a string'
    assert isinstance(n, int) and n>0, 'n must be a positive integer'
    self.registers = [None]*n
    self.name = name
    self.outputConnections = []
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def activate(self):
    return

  #----------------------------------------------------------------------------  
  def write(self, n, x):
    '''
    Writes the float x into the n'th register.  Essentially a queue
    '''
    assert isinstance(x, float), 'x must be a float'
    assert (isinstance(n, int) and n>=0 and
            n<len(self.register)), 'n must be a valid index into a list'
    assert registers[n] == None, 'register location must be empty'
    self.registers[n] = x
    return

#------------------------------------------------------------------------------
class HiddenNode():
  '''
  Hidden nodes are the nodes that are neither InputNodes or OutputNodes.  They
  are the main computing elements of the PFNN.  They also facilitate virtual
  links between nodes.  They contain registers that connected links write to, 
  a tuple containing a list of output nodes to which this node writes, as well
  as a tuple to define virtual links.  The registers are implemented as a dict
  with the Link acting as the key.
  Functions:
  -Activate(), ret: None
  -write(), ret: None
  Internal Variables:
  -(str) name
  -(Activator) activator
  -(float) theta
  -(int) a
  -({Link, [float]}) inputRegisters
  -({Link, Link}) vLinks
  -((Link),) outputConnections
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, theta, a, name = None):
    assert isinstance(activator, Activator), 'activator must be an Activator'
    assert isinstance(name, str) or name == 0, 'name must be a string'
    assert isinstance(theta, float), 'theta must be a float'
    assert isinstance(a, int) and a > 0, 'a must be a positive integer'
    self.name = name
    self.inputRegisters = {}
    self.outputConnections = []
    self.vLinks = {}
    self.x = theta
    self.c = 0 #A counter for the number of iterations
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def activate(self):
    return

  #----------------------------------------------------------------------------  
  def write(self, L, x):
    '''
    The Link L writes the value x to the register that L is bound to.
    '''
    assert isinstance(L, Link), 'Link must be a Link'
    assert isinstance(x, float), 'x must be a float'
    assert L in self.inputRegisters, str(L) + ' must be bound to ' + str(self)
    assert len(self.registers[L]) == 0, 'Register must be empty'
    self.registers[L].append(x)
    return

  #----------------------------------------------------------------------------  
  def bind(self, L):
    '''
    The Link L binds itself to an input of this Node.  An attempt to bind 
    more than once is considered an error.
    '''
    assert isinstance(L, Link), 'L must be a Link'
    assert L not in self.registers, 'Attempt by ' + str(L) + ' to bind twice'
    self.registers[L] = []
    return

#------------------------------------------------------------------------------
class OutputNode():
  '''
  An output Node.  The Brain takes the output from output nodes and returns it.
  The output Nodes each contribute to the final output.
  Functions:
  -activate(), ret: A final output float
  -write(), ret: None
  -bind(), reg: None
  Internal Variables:
  -(str) name
  -(Activator) activator
  -(float) theta
  -(int) a
  -({Link, [float]}) inputRegisters
  -([Link]) outputConnections
  -(float) x
  -(int) c
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, theta, a, name = None):
    assert isinstance(activator, Activator), 'activator must be an Activator'
    assert isinstance(theta, float), 'theta must be a float'
    assert isinstance(a, int) and a > 0, 'a must be a positive integer'
    assert isinstance(name, str) or name == 0, 'name must be a string'
    self.name = name
    self.registers = {}
    self.outputConnections = []
    self.x = theta
    self.c = 0 #A counter for the number of iterations
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def activate(self):
    return

  #----------------------------------------------------------------------------  
  def write(self, L, x):
    '''
    The Link L writes the float x to the register of this OutputNode to which
    it is bound.
    '''
    assert isinstance(L, Link), 'L must be a Link'
    assert isinstance(x, float), 'x must be a float'
    assert L in self.registers, str(L) + ' must be bound to ' + str(self)
    assert len(self.registers[L]) == 0, 'Register must be empty'
    self.registers[L].append(x)
    return

  #----------------------------------------------------------------------------  
  def bind(self, L):
    '''
    The Link L binds itself to the input of this Node.  Many Links may be
    bound at once, but an attempt by a Link to bind a second time is considered
    an error.
    '''
    assert isinstance(L, Link), 'L must be a link'
    assert L not in self.registers, 'attempt by ' + str(L) + ' to bind twice'
    self.registers[L] = []
    return

#------------------------------------------------------------------------------
class Link():
  '''
  This class defines a link.  It is an object that connects nodes together.
  When it's activate method is called by Brain, the link will apply it's
  affine transform to the item placed in it's register and then write to the 
  regsiter of the node to which this link is connected.  The item is placed in
  it's register when the brain calls the activate method on the node connected
  to this links input.  The write method of this link writes into it's register.
  Functions:
  -activate(), ret: None
  -write(), ret: None
  -bind(), ret: None
  Internal Variables:
  -(float): W
  -(float): T
  -(dict{Node, float}): register
  -(Node): outputNode
  -(str): name
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, W, T, outputNode = None, name = None):
    '''
    W: Weight for affine transform W*x + T
    T: Weight for affine transfor W*x + t
    name: The name of this particular link
    outputNode: The node this link calls the write() method on
    '''
    assert isinstance(W, (float)), 'W must be a float'
    assert isinstance(T, (float)), 'T must be a float'
    assert isinstance(name, str) or name == None, 'name must be a string'
    assert (isinstance(outputNode, (HiddenNode, OutputNode)) or
            outputNode is None), 'outputNode must be a node'

    self.W = W
    self.T = T
    self.register = {}
    self.outputNode = outputNode
    self.name = name
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.__str__()

  #----------------------------------------------------------------------------  
  def activate(self):
    return

  #----------------------------------------------------------------------------  
  def write(self, N, x):
    '''
    The Node N writes the float x to the register of this Link.  The Node N
    must be bound to the Link and the register must be empty (contain None).
    '''
    assert isinstance(x, float), 'x must be a float'
    assert isinstance(N, InputNode, HiddenNode), 'N must be a Node'
    assert N in self.register, str(N) + ' must be bound to ' + str(self)
    assert len(self.register[N]) == 0, 'register must be empty'
    self.register[N].append(x)
    return
                        
  #----------------------------------------------------------------------------  
  def bind(self, N):
    '''
    The node N binds itself to the input of this Link.  The Link may only have
    one node bound to it at a time, and re-binding is considered an error.
    '''
    assert isinstance(N, (InputNode, HiddenNode)), 'N must be a node'
    assert len(self.register) == 0, str(str(N) + ' cannot rebind to link ' 
                                        + str(self))
    self.register[N] = []
    return

#------------------------------------------------------------------------------
class Activator():
  '''
  This is an activator.  Nodes use activators to compute their outputs.  Since
  many (most) nodes will have the same type of activator, defining it as a
  seperate class makes things a little simpler.
  Functions:
  -iterate(), ret: defined by the iteration function self.i
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
  def activate(self, x):
    '''
    Calls the activation function f on x and returns f's return value.
    No error handling happens here.  It should be done inside the node that
    contains this activator.
    '''
    return self.f(x)

  #----------------------------------------------------------------------------  
  def iterate(self, x):
    '''
    Calls the iterator function i on x and returns i's return value.
    No error handling happens here.  It should be done inside the Node 
    that contains this activator
    '''
    return self.i(x)
