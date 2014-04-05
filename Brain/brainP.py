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
    self.LinkList = []
    self.ActList = []
    self.E = []
    self.IDCount = 1
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
#    PID = Value('I', self.PIDCount)
    ID = self.IDCount
    self.IDCount += 1

    #Create the Link
    newLink = Link(W, T, ACKCount, ACKEvent, ACKMax, dataQueue, ID)

    #Append the Link to the list
    self.LinkList.append(newLink)
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
    R1.ACKMax.value += 1
    R2.appendInput(R1)
    self.E.append((R1, R2))
    return

B = Brain()
L1 = B.createLink(1.0, 1.0)
L2 = B.createLink(2.0, 2.0)
L3 = B.createLink(3.0, 3.0)

B.createConnection(L1, L2)
B.createConnection(L2, L1)
B.createConnection(L1, L3)
B.createConnection(L3, L1)
#B.createConnection(L2, L3)
#B.createConnection(L3, L2)

P1 = Process(target=L1.activate)
P2 = Process(target=L2.activate)
P3 = Process(target=L3.activate)

L1.dataQueue.put((1.0, 0))

P1.start()
P2.start()
P3.start()

time.sleep(1)

