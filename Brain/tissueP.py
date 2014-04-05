#Parallel implementation
from multiprocessing import Queue, Lock, Event
import os, time

#------------------------------------------------------------------------------
class Link():
  '''
  The Link resource.  It is connected to and from nodes and other Links.
  '''
  #----------------------------------------------------------------------------
  def __init__(self, W, T, ACKCount, ACKEvent, ACKMax, dataQueue,
               ID):
    '''
    (float)W: A weight a the affine transform Wx + T
    (float)T: T A weight a the affine transform Wx + T
    (int)ID: To identify different processes
    -> All of the following are from the multiprocessing module
    (Value)ACKCount: A counter for the number of acknowledgements
    (Event)ACKEvent: An event for when ACKCount = ACKMax
    (Value)ACKMax: The number of output connections.  ie, number of ACKs to get
    (Queue)dataQueue: A queue for data input
    (Event)queueEvent: An event for when the dataQueue is not empty
    '''
    assert isinstance(W, float), 'W must be an float'
    assert isinstance(T, float), 'T must be a float'

    self.ACKCount = ACKCount
    self.ACKEvent = ACKEvent
    self.ACKMax = ACKMax #This needs to be set to len(outputList)

    self.dataQueue = dataQueue

    self.outputList = {}
    self.inputList = {}
    
    self.W = W
    self.T = T

    self.PID = 0
    self.ID = ID
    return

  #----------------------------------------------------------------------------
  def activate(self):
    '''
    This is the function that will run as a seperate process.  Everything
    else in the class just access data.  Call this function when
    everything is connected and finalized.
    '''
    self.PID = os.getpid()
#    print ('=====================================================\n' +
#           'Process ' + str(self.ID) + ' Running \n' +
#           'PID: ' + str(os.getpid()) + '\n' +
#           'outputList: ' + str(self.outputList) + '\n' +
#           'inputList: ' + str(self.inputList) + '\n\n'
#          )
    while True:
      x, ID = self.dataQueue.get()
      print 'ID %d Got queue data (%f, %d)' %(self.ID, x, ID)  
      if ID != 0:
        self.ACK(ID)
      xp = self.W*x + self.T
      assert self.ACKCount.value == 0, 'ACKCount not 0 prior to outputting'
      for ID in self.outputList:
        self.push(xp, ID)
      self.ACKEvent.wait()
      self.ACKEvent.clear()
      print 'ID %d got ACKEvent' %self.ID
    return

  #----------------------------------------------------------------------------
  def appendOutput(self, R):
    '''
    Simply appends the resource R to the outputList.  This is mostly for 
    checking for programmer errors, it isn't necessary.  I may remove this
    method in the future.
    '''
    self.outputList[R.ID] = {'ACKCount': R.ACKCount,
                             'ACKEvent': R.ACKEvent,
                             'ACKMax': R.ACKMax,
                             'dataQueue': R.dataQueue
                             }
    return

  #----------------------------------------------------------------------------
  def appendInput(self, R):
    '''
    Simply appends the resource R to the inputList.  This is mostly for 
    checking for programmer errors, it isn't necessary.  I may remove this
    method in the future.
    '''
    self.inputList[R.ID] = {'ACKCount': R.ACKCount,
                            'ACKEvent': R.ACKEvent,
                            'ACKMax': R.ACKMax,
                            'dataQueue': R.dataQueue,
                            }
    return

  #----------------------------------------------------------------------------
  def push(self, x, ID):
    '''
    Pushes the value x to ID's dataQueue
    '''
    if not ID in self.outputList:
      raise RuntimeError('%d is not in the outputList' %ID)
    else:
      self.outputList[ID]['dataQueue'].put((x, self.ID))
    return

  #----------------------------------------------------------------------------
  def ACK(self, ID):
    '''
    '''
    if not ID in self.inputList:
      raise RuntimeError('%d is not in the inputList' %ID)
    else:
      with self.inputList[ID]['ACKCount'].get_lock():
        self.inputList[ID]['ACKCount'].value += 1
        if (self.inputList[ID]['ACKCount'].value ==
            self.inputList[ID]['ACKMax'].value):
          self.inputList[ID]['ACKCount'].value = 0
          self.inputList[ID]['ACKEvent'].set()
    return
