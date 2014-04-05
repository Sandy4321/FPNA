#Parallel FPNA implementation
from tissueP import Link
from multiprocessing import Process, Queue, Lock, Event, Value
import time

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
    self.LinkList = {}
    self.ActList = {}
    self.PIDCount = 0
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
    queueEvent = Event()
    PID = Value('I', self.PIDCount)
    self.PIDCount += 1

    #Create the Link
    newLink = Link(W, T, ACKCount, ACKEvent, ACKMax, dataQueue, queueEvent,
                   PID)

    #Append the Link to the list
    self.LinkList[PID] = newLink
    return newLink

  #----------------------------------------------------------------------------
  def addInputNode(self):
    '''
    '''
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
    R1.appendOutput(R2)
    R2.appendInput(R1)
    return

B = Brain()
L1 = B.createLink(1.0, 1.0)
L2 = B.createLink(2.0, 2.0)
B.createConnection(L1, L2)

P1 = Process(target=L1.activate)
P2 = Process(target=L2.activate)

P1.start()
P2.start()


