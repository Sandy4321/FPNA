#Activator.py
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
