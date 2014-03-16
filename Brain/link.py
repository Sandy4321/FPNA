#Link.py
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
