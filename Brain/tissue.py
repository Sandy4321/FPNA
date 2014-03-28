#tissue.py
#------------------------------------------------------------------------------
class InputNode():
  '''
  Input nodes take input from the brain, they simply pass values into the 
  network.  They don't apply any transforms.  Their queues are written into
  by the brain only.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, name = None):
    '''
    n: Number of inputs to be received
    name: Name of this Node
    '''
    assert isinstance(name, str) or name == None, 'name must be a string'
    self.Queue = [] #The last element is the input, Queue[0] is the first
    self.name = name
    self.outputConnections = []
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.name

  #----------------------------------------------------------------------------  
  def activate(self):
    '''
    All this does is pushes each value in the Queue to each link in the
    outputConnections list.
    '''
    while self.Queue != []:
      x = self.Queue.pop(0)
      for L in self.outputConnections:
        L.push(x)
    return

  #----------------------------------------------------------------------------  
  def push(self, x):
    '''
    Pushes the value x into the Queue
    '''
    assert isinstance(x, float), 'x must be a float'
    self.Queue.append(x)
    return

  #----------------------------------------------------------------------------  
  def createConnection(self, L_out):
    '''
    Creates a connection from this Node to a Link.  All outputs from the
    activator will be sent to this link.
    '''
    assert isinstance(L_out, Link) or L_out == None, 'L_out must be a Link'
    assert L_out not in self.outputConnections, 'Attempt to make conn twice'
    L_out.bind(self) #Bind to the input of the Link
    self.outputConnections.append(L_out)
    return

#------------------------------------------------------------------------------
class HiddenNode():
  '''
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, activator, theta, a, name = None):
    assert isinstance(activator, Activator), 'activator must be an Activator'
    assert isinstance(name, str) or name == 0, 'name must be a string'
    assert isinstance(theta, float), 'theta must be a float'
    assert isinstance(a, int) and a > 0, 'a must be a positive integer'
    assert isinstance(outputs, list), 'outputs must be a list'
    assert all([isinstance(o, Link) for o in outputs]), 'ouputs must be Links'

    self.outputConnections = [] #[L1, L2, ...]
    self.Queue = {} #{Link : ([floats], [Links], r) ...}
    self.activator = activator
    self.name = name
    self.theta = theta
    self.x = theta
    self.a = a
    self.c = 0 #A counter for the number of iterations
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.name

  #----------------------------------------------------------------------------  
  def activate(self):
    '''
    The node processes all values in it's queue and sends various outputs
    to the appropriate links.  The order here matters, vLinks are to be
    dealt with first.
    '''
    for Lin in self.Queue: #Iterate through all queues
      while self.Queue[Lin][0] != []:
        x = self.Queue[Lin][0].pop(0) #Take the first element from the queue
        for Lout in self.Queue[Lin][1]:
          Lout.push(x) #Send values to each Queue's virtual links
        if self.Queue[Lin][2]: #If r == 1 apply the activator
          self.x = self.activator.iterate(self.x, x) #call iterate function
          self.c += 1 #increment the counter
          if self.c == self.a: #If the counter has reached it's max vlue
            self.c = 0 #reset the counter
            y = self.activator.activate(x) #calculate the activation of x
            self.x = theta #reset x
            for Lout in self.outputConnections:
              Lout.push(y) #output the activation to all output connections
    return

  #----------------------------------------------------------------------------  
  def push(self, L, x):
    '''
    Push the value x into L's queue
    '''
    assert isinstance(x, float), 'x must be a float'
    assert isinstance(L, Link), 'L must be a Link'
    assert L in self.Queue, 'L must be in the Queue'
    self.Queue[x][0].append(x)
    return

  #----------------------------------------------------------------------------  
  def bind(self, L, vLinks = [], r = False):
    '''
    The Link L binds itself to an input of this Node.  An attempt to bind 
    more than once is considered an error.  If r is True, then inputs from
    L will go to the activator.
    '''
    assert isinstance(L, Link), 'L must be a Link'
    assert isinstance(vLinks, list), 'vLinks must be a list'
    assert all([isinstance(l, Link) for l in vLinks]), 'vLinks must be Links'
    assert isinstance(r, bool), 'r must be a bool'
    assert L not in self.Queue, 'Attempt by ' + str(L) + ' to bind twice'
    if L not in self.outputConnections:
      for l in vLinks:
        l.bind(self) #Bind to each of the links
    self.Queue[L] = [[], vLinks, r]
    return

  #----------------------------------------------------------------------------  
  def createConnection(self, L_out):
    '''
    Creates a connection from this Node to a Link.  All outputs from the
    activator will be sent to this link.
    '''
    assert isinstance(L_out, Link) or L_out == None, 'L_out must be a Link'
    assert L_out not in self.outputConnections, 'Attempt to make conn twice'
    if L_out not in self.Queue:
      L_out.bind(self) #Bind to the input of the Link
    self.outputConnections.append(L_out)
    return

#------------------------------------------------------------------------------
class Link():
  '''
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, W, T, name = None):
    '''
    W: Weight for affine transform W*x + T
    T: Weight for affine transfor W*x + t
    name: The name of this particular link
    '''
    assert isinstance(W, (float)), 'W must be a float'
    assert isinstance(T, (float)), 'T must be a float'
    assert isinstance(name, str) or name == None, 'name must be a string'
    
    self.inputNode = None #The node bound to this link
    self.outputNode = None #The node this link is bound to

    self.W = W
    self.T = T
    self.Queue = []
    self.name = name
    return

  #----------------------------------------------------------------------------  
  def __str__(self):
    return self.name
  def __repr__(self):
    return self.name

  #----------------------------------------------------------------------------  
  def activate(self):
    '''
    Applies the affine transform Wx + T to every value in the Queue and then
    pushes the values to the outputNode.
    '''
    while self.Queue != []:
      y = self.W*self.Queue.pop(0) + self.T
      self.outputNode.push(y)
    return

  #----------------------------------------------------------------------------  
  def push(self, N, x):
    '''
    The Node N pushes the float x to the queue of this Link.  The Node N
    must be bound to the Link and the register must be empty (contain None).
    '''
    assert isinstance(x, float), 'x must be a float'
    assert isinstance(N, InputNode, HiddenNode), 'N must be a Node'
    assert N == self.inputNode, str(N) + 'must be bound to this node'
    self.Queue.append(x)
    return
                        
  #----------------------------------------------------------------------------  
  def bind(self, N):
    '''
    The node N binds itself to the input of this Link.  The Link may only have
    one node bound to it at a time, and re-binding is considered an error.
    '''
    assert isinstance(N, (InputNode, HiddenNode)), 'N must be a node'
    assert self.inputNode == None, 'Attempt to re-bind to link'
    self.inputNode = N
    return

  #----------------------------------------------------------------------------  
  def setOutputNode(self, N):
    '''
    Sets the Node N to this Link's output node.  That is, the node to which
    this link writes it's output.  Attempting to change this connection
    is treated as an error.
    '''
    assert isinstance(N, HiddenNode), 'N must be a Node'
    assert self.outputNode == None
    N.bind(self) #Bind to the node
    self.outputNode = N
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
    return self.name

  #----------------------------------------------------------------------------  
  def activate(self, x):
    '''
    Calls the activation function f on x and returns f's return value.
    No error handling happens here.  It should be done inside the node that
    contains this activator.
    '''
    return self.f(x)

  #----------------------------------------------------------------------------  
  def iterate(self, x, xp):
    '''
    Calls the iterator function i on x and returns i's return value.
    No error handling happens here.  It should be done inside the Node 
    that contains this activator
    '''
    return self.i(x, xp)
