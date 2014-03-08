#FPNNSequential.py
#------------------------------------------------------------------------------
class Link():
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
class Node():
  def __init__(self):
    return

#program entry
#==============================================================================
