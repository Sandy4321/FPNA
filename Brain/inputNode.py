#InputNode.py
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
