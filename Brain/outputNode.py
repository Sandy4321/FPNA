#OutputNode.py
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
