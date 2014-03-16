#HiddenNode.py
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
