#Parallel FPNA implementation
from tissueP import Link, Activator, InputNode
from multiprocessing import Process, Queue, Lock, Event, Value
import time, math

#------------------------------------------------------------------------------
class Brain():
  '''
  The Brain.  This contains and controls the Links and Activators.  It also 
  handles building the network.
  '''
  #----------------------------------------------------------------------------
  def __init__(self):
    '''
    '''
    self.LinkList = []
    self.ActList = []
    self.inputList = []
    self.outputList = []
    self.E = []
    self.IDCount = 1

    self.ACKCount = Value('I', 0)
    self.ACKEvent = Event()
    self.ACKMax = Value('I', 0)
    return

  #----------------------------------------------------------------------------
  def createLink(self, W, T):
    '''
    '''
    #Values are automatically locked.  You can use:
    #with ACKCount.get_lock():
    #  ACKCount += 1
    ACKCount = Value('I', 0) #Unsigned int
    ACKEvent = Event()
    ACKMax = Value('I', 0)
    dataQueue = Queue()
    ID = self.IDCount
    self.IDCount += 1

    #Create the Link
    newLink = Link(W, T, ACKCount, ACKEvent, ACKMax, dataQueue, ID)

    #Append the Link to the list
    self.LinkList.append(newLink)
    return newLink

  #----------------------------------------------------------------------------
  def createActivator(self, i, f, iterateMax, theta):
    '''
    '''
    ACKCount = Value('I', 0)
    ACKEvent = Event()
    ACKMax = Value('I', 0)
    dataQueue = Queue()
    ID = self.IDCount
    self.IDCount += 1
    
    newAct = Activator(i, f, ACKCount, ACKEvent, ACKMax, dataQueue,
                             ID, iterateMax, theta)
                             
    self.ActList.append(newAct)
    return newAct

  #----------------------------------------------------------------------------
  def createInputNode(self, n):
    '''
    Creates an InputNode.  This is a node that communicates with the Brain.  It
    does not compute any activation function.
    
    (int) n: The number of input's this InputNode will receive.  It should be 
    passed as an n-length tuple
    '''
    
    #The brain has a 'global' ACK count for every input node.  Since each input
    #node may receive multiple values for each input vector.  This is a 
    #performance bottleneck as each InputNode must share the same lock on the
    #Brain's ACK counter.

    ACKCount = Value('I', 0)
    brainACKCount = self.ACKCount
    ACKEvent = Event()
    brainACKEvent = self.ACKEvent
    ACKMax = Value('I', 0)
    brainACKMax = self.ACKMax
    dataQueue = Queue()
    ID = self.IDCount
    self.IDCount += 1
    
    newInput = InputNode(ACKCount, ACKEvent, ACKMax, dataQueue,
                         ID, brainACKCount, brainACKEvent, brainACKMax,
                         n)
    self.ACKMax.value += n
    self.inputList.append(newInput)
    return newInput

  #----------------------------------------------------------------------------
  def addOutputNode(self):
    '''
    '''
    return

  #----------------------------------------------------------------------------
  def createConnection(self, R1, R2):
    '''
    '''
    assert not (isinstance(R1, Activator) and isinstance(R2, Activator))
    R1.appendOutput(R2)
    R1.ACKMax.value += 1
    R2.appendInput(R1)
    self.E.append((R1, R2))
    return

  #----------------------------------------------------------------------------
  def activate(self, X):
    '''
    (List of tuples of floats)x: The input vector.  The i'th element will be
    passed to the i'th InputNode.  Each element of x should be a tuple of
    length n of floats which will be sent to the InputNode.
    '''
    assert sum([len(x) for x in X]) == self.ACKMax.value
    assert isinstance(X, list)
    for i in range(len(self.inputList)):
      print 'pushing ' + str(X[i]) + ' to InputNode ' + str(self.inputList[i])
      self.inputList[i].dataQueue.put(X[i])
    self.ACKEvent.wait()
    print 'Brain received all ACKs'
    return


def i(x, xp):
  '''
  '''
  return x + xp

def f(x):
  '''
  '''
  return 1.0 / (1.0 + math.exp(-x)) #Sigmoid function

B = Brain()

L1 = B.createLink(1.0, 0.0)

A1 = B.createActivator(i, f, 1, 0.0)

I1 = B.createInputNode(2)
I2 = B.createInputNode(3)

B.createConnection(L1, A1)
B.createConnection(I1, L1)
B.createConnection(I2, L1)

P1 = Process(target = L1.activate)
P2 = Process(target = A1.activate)
P3 = Process(target = I1.activate)
P4 = Process(target = I2.activate)

P1.start()
P2.start()
P3.start()
P4.start()

B.activate([(1,1,1), (1,1)])
