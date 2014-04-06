#Parallel FPNA implementation
from tissueP import Link, Activator
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
    self.InputList = []
    self.OutputList = []
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
    '''
    ACKCount = Value('I', 0)
    brainACKCount = self.ACKCount
    ACKEvent = Event()
    brainACKEvent = Event()
    ACKMax = self.ACKMax
    brainACKMax = self.ACKMax
    dataQueue = Queue()
    ID = self.IDCount
    self.IDCount += 1
    
    newInput = InputNode(ACKCount, ACKEvent, ACKMax, dataQueue,
                         ID, brainACKCount, brainACKEvent, brainACKMax,
                         n)
    self.ACKMax += n
    self.inputList.append(newInput)
    return

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

B.createConnection(L1, A1)

P1 = Process(target = L1.activate)
P2 = Process(target = A1.activate)

P1.start()
P2.start()

L1.dataQueue.put((1.0, 0))
