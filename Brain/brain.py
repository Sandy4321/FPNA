o#Brain.py
#The Node classes would benefit slightly from inheritance, but I think it 
#will keep things simple if they are all seperate.  It is a small system,
#inheritance won't make that big of a difference.

#This is currently a sequential implementation

from tissue import InputNode, HiddenNode, OutputNode, Link, Activator

#------------------------------------------------------------------------------
class Brain():
  '''
  The 'Brain' is the controller for all the pieces of the FPNA.  The Nodes
  and the Links.  The brain essentially just calls the activate method of the
  nodes and links in the correct order for proper operation.  It is basically
  just a state machine that drives the nodes and links.
  '''
  #----------------------------------------------------------------------------  
  def __init__(self, name = None):
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
  def bind(self, From, To):
    '''
    Binds the output of element 'From' to the input of the element 'To'.
    Outputs are always bound to inputs, inputs don't need to be bound in the
    other direction.
    '''
    return

#==============================================================================
l = Link(1.0, 2.0)
