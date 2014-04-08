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
  def __str__(self):
    return self.ID
  def __repr__(self):
    return self.ID

  #----------------------------------------------------------------------------
  def activate(self):
    '''
    This is the function that will run as a seperate process.  Everything
    else in the class just access data.  Call this function when
    everything is connected and finalized.
    '''
    self.PID = os.getpid()
    while True:
      x, ID = self.dataQueue.get()
      print '%s Got queue data (%f, %s)' %(self.ID, x, ID)
      self.ACK(ID)
      xp = self.W*x + self.T
      assert self.ACKCount.value == 0, 'ACKCount not 0 prior to outputting'
      for ID in self.outputList:
        self.push(xp, ID)
      if self.ACKMax.value > 0:
        self.ACKEvent.wait()
        print '%s Got all ACK' %self.ID
        self.ACKEvent.clear()
    return

  #----------------------------------------------------------------------------
  def appendOutput(self, R):
    '''
    Simply appends the resource R to the outputList.
    '''
    self.outputList[R.ID] = {'dataQueue': R.dataQueue}
    return

  #----------------------------------------------------------------------------
  def appendInput(self, R):
    '''
    Simply appends the resource R to the inputList.
    '''
    self.inputList[R.ID] = {'ACKCount': R.ACKCount,
                            'ACKEvent': R.ACKEvent,
                            'ACKMax': R.ACKMax,
                            }
    return

  #----------------------------------------------------------------------------
  def push(self, x, ID):
    '''
    Pushes the value x to ID's dataQueue
    '''
    if not ID in self.outputList:
      raise RuntimeError('%s is not in the outputList' %ID)
    else:
      self.outputList[ID]['dataQueue'].put((x, self.ID))
    return

  #----------------------------------------------------------------------------
  def ACK(self, ID):
    '''
    '''
    if not ID in self.inputList:
      raise RuntimeError('%s is not in the inputList' %ID)
    else:
      with self.inputList[ID]['ACKCount'].get_lock():
        self.inputList[ID]['ACKCount'].value += 1
        if (self.inputList[ID]['ACKCount'].value ==
            self.inputList[ID]['ACKMax'].value):
          self.inputList[ID]['ACKCount'].value = 0
          self.inputList[ID]['ACKEvent'].set()
    return

#------------------------------------------------------------------------------
class Activator():
  '''
  The Activator resource.  It is connected to and from Links.
  '''
  #----------------------------------------------------------------------------
  def __init__(self, i, f, ACKCount, ACKEvent, ACKMax, dataQueue,
               ID, iterateMax, theta):
    '''
    (function)i: The iteration function
    (function)f: The activation function
    (int)ID: To identify different processes
    -> All of the following are from the multiprocessing module
    (Value)ACKCount: A counter for the number of acknowledgements
    (Event)ACKEvent: An event for when ACKCount = ACKMax
    (Value)ACKMax: The number of output connections.  ie, number of ACKs to get
    (Queue)dataQueue: A queue for data input
    '''
    assert hasattr(i, '__call__'), 'i must be a function'
    assert hasattr(f, '__call__'), 'f must be a function'
    assert isinstance(theta, float), 'theta must be a float'

    self.ACKCount = ACKCount
    self.ACKEvent = ACKEvent
    self.ACKMax = ACKMax

    self.dataQueue = dataQueue

    self.outputList = {}
    self.inputList = {}
    
    self.i = i
    self.f = f

    self.iterateMax = iterateMax
    self.iterateCount = 0
    self.x = theta
    self.theta = theta
    self.PID = 0
    self.ID = ID
    return

  #----------------------------------------------------------------------------
  def __str__(self):
    return self.ID
  def __repr__(self):
    return self.ID

  #----------------------------------------------------------------------------
  def activate(self):
    '''
    This is the function that will run as a seperate process.  Everything
    else in the class just access data.  Call this function when
    everything is connected and finalized.
    '''
    self.PID = os.getpid()
    while True:
      x, ID = self.dataQueue.get()
      print '%s Got queue data (%f, %s)' %(self.ID, x, ID)
      self.ACK(ID)
      self.x = self.i(self.x, x)
      self.iterateCount += 1
      if self.iterateCount == self.iterateMax:
        xp = self.f(self.x)
        self.iterateCount = 0
        self.x = self.theta
        assert self.ACKCount.value == 0, 'ACKCount not 0 prior to outputting'
        for ID in self.outputList:
          print '%s pushing %f to ID %s' %(self.ID, xp, ID)
          self.push(xp, ID)
        if self.ACKMax.value > 0:
          self.ACKEvent.wait()
          print '%s Got all ACK' %self.ID
          self.ACKEvent.clear()
    return

  #----------------------------------------------------------------------------
  def appendOutput(self, R):
    '''
    Simply appends the resource R to the outputList.
    '''
    assert isinstance(R, Link), 'R must be a Link'
    self.outputList[R.ID] = {'dataQueue': R.dataQueue}
    return

  #----------------------------------------------------------------------------
  def appendInput(self, R):
    '''
    Simply appends the resource R to the inputList. 
    '''
    assert isinstance(R, Link), 'R must be a Link'
    self.inputList[R.ID] = {'ACKCount': R.ACKCount,
                            'ACKEvent': R.ACKEvent,
                            'ACKMax': R.ACKMax,
                            }
    return

  #----------------------------------------------------------------------------
  def push(self, x, ID):
    '''
    Pushes the value x to ID's dataQueue
    '''
    if not ID in self.outputList:
      raise RuntimeError('%s is not in the outputList' %ID)
    else:
      self.outputList[ID]['dataQueue'].put((x, self.ID))
    return

  #----------------------------------------------------------------------------
  def ACK(self, ID):
    '''
    '''
    if not ID in self.inputList:
      raise RuntimeError('%s is not in the inputList' %ID)
    else:
      with self.inputList[ID]['ACKCount'].get_lock():
        self.inputList[ID]['ACKCount'].value += 1
        if (self.inputList[ID]['ACKCount'].value ==
            self.inputList[ID]['ACKMax'].value):
          self.inputList[ID]['ACKCount'].value = 0
          self.inputList[ID]['ACKEvent'].set()
    return

#------------------------------------------------------------------------------
class InputNode():
  '''
  The InputNode resource.  It is connected from the Brain to a link.
  '''
  #----------------------------------------------------------------------------
  def __init__(self, ACKCount, ACKEvent, ACKMax, dataQueue,
               ID, brainACKCount, brainACKEvent, brainACKMax,
               n):
    '''
    (int)ID: To identify different processes
    (int)n: The number of inputs to the node for each NN input vector
    -> All of the following are from the multiprocessing module
    (Value)ACKCount: A counter for the number of acknowledgements
    (Event)ACKEvent: An event for when ACKCount = ACKMax
    (Value)ACKMax: The number of output connections.  ie, number of ACKs to get
    (Queue)dataQueue: A queue for data input
    (Value)brainACKCount: The Brain's ACK counter
    (Event)brainACKEvent: The Brain's ACK Event
    (Value)brainACKMax: The Brains's max ACK counter
    '''
    self.ACKCount = ACKCount
    self.ACKEvent = ACKEvent
    self.ACKMax = ACKMax

    self.brainACKCount = brainACKCount
    self.brainACKEvent = brainACKEvent
    self.brainACKMax = brainACKMax

    self.dataQueue = dataQueue

    self.outputList = {}

    self.n = n
    self.PID = 0
    self.ID = ID
    return

  #----------------------------------------------------------------------------
  def __str__(self):
    return self.ID
  def __repr__(self):
    return self.ID

  #----------------------------------------------------------------------------
  def activate(self):
    '''
    This is the function that will run as a seperate process.  Everything
    else in the class just access data.  Call this function when
    everything is connected and finalized.
    '''
    self.PID = os.getpid()
    while True:
      X = self.dataQueue.get() #X will be a tuple of values
      if len(X) != self.n:
        raise ValueError('Input X must have length %d' %self.n)
      print '%s Got queue data ' %self.ID + str(X)
      self.ACK()
      for x in X:
        assert self.ACKCount.value == 0, 'ACKCount not 0 prior to outputting'
        print '%s outputting %f' %(self.ID, x)
        for ID in self.outputList:
          self.push(x, ID)
        self.ACKEvent.wait()
        print '%s Got all ACK' %self.ID
        self.ACKEvent.clear()
    return

  #----------------------------------------------------------------------------
  def appendOutput(self, R):
    '''
    Simply appends the resource R to the outputList.
    '''
    assert isinstance(R, Link), 'R must be a Link'
    self.outputList[R.ID] = {'dataQueue': R.dataQueue}
    return

  #----------------------------------------------------------------------------
  def push(self, x, ID):
    '''
    Pushes the value x to ID's dataQueue
    '''
    if not ID in self.outputList:
      raise RuntimeError('%s is not in the outputList' %ID)
    else:
      self.outputList[ID]['dataQueue'].put((x, self.ID))
    return

  #----------------------------------------------------------------------------
  def ACK(self):
    '''
    '''
    with self.brainACKCount.get_lock():
      self.brainACKCount.value += self.n
      if (self.brainACKCount.value == self.brainACKMax.value):
        self.brainACKCount = 0
        self.brainACKEvent.set()
    return

#------------------------------------------------------------------------------
class OutputNode():
  '''
  The OutputNode resource.  It is connected from a Link to the Brain
  '''
  #----------------------------------------------------------------------------
  def __init__(self, i, f, ACKEvent, dataQueue, ID, iterateMax, theta,
               index, brainDataQueue):
    '''
    (function)i: The iteration function
    (function)f: The activation function
    (int)ID: To identify different processes
    (int)index: The index of this output node in the Brain's list.  It is
    returned with the value computed so the Brain can properly assemble the
    output vector
    -> All of the following are from the multiprocessing module
    (Event)ACKEvent: An event for when ACKCount = ACKMax
    (Queue)dataQueue: A queue for data input
    (Queue)brainDataQueue: The Brain's Queue for data
    '''
    assert hasattr(i, '__call__'), 'i must be a function'
    assert hasattr(f, '__call__'), 'f must be a function'

    self.ACKEvent = ACKEvent

    self.dataQueue = dataQueue
    self.brainDataQueue = brainDataQueue

    self.inputList = {}
    
    self.i = i
    self.f = f

    self.index = index
    self.iterateMax = iterateMax
    self.iterateCount = 0
    self.x = theta
    self.theta = theta
    self.PID = 0
    self.ID = ID

    return

  #----------------------------------------------------------------------------
  def __str__(self):
    return self.ID
  def __repr__(self):
    return self.ID

  #----------------------------------------------------------------------------
  def activate(self):
    '''
    This is the function that will run as a seperate process.  Everything
    else in the class just access data.  Call this function when
    everything is connected and finalized.
    '''
    self.PID = os.getpid()
    while True:
      x, ID = self.dataQueue.get()
      print '%s Got queue data (%f, %s)' %(self.ID, x, ID)
      self.ACK(ID)
      self.x = self.i(self.x, x)
      self.iterateCount += 1
      if self.iterateCount == self.iterateMax:
        xp = self.f(self.x)
        self.iterateCount = 0
        self.x = self.theta
        print '%s outputting %f' %(self.ID, xp)
        self.push(xp)
        self.ACKEvent.wait()
        print '%s Got all ACK' %self.ID
        self.ACKEvent.clear()
    return

  #----------------------------------------------------------------------------
  def appendInput(self, R):
    '''
    Simply appends the resource R to the inputList.
    '''
    assert isinstance(R, Link), 'R must be a Link'
    self.inputList[R.ID] = {'ACKCount': R.ACKCount,
                            'ACKEvent': R.ACKEvent,
                            'ACKMax': R.ACKMax,
                            }
    return

  #----------------------------------------------------------------------------
  def push(self, x):
    '''
    Pushes the value x to the Brain
    '''
    self.brainDataQueue.put((x, self.index))
    return

  #----------------------------------------------------------------------------
  def ACK(self, ID):
    '''
    '''
    if not ID in self.inputList:
      raise RuntimeError('%s is not in the inputList' %ID)
    else:
      with self.inputList[ID]['ACKCount'].get_lock():
        self.inputList[ID]['ACKCount'].value += 1
        if (self.inputList[ID]['ACKCount'].value ==
            self.inputList[ID]['ACKMax'].value):
          self.inputList[ID]['ACKCount'].value = 0
          self.inputList[ID]['ACKEvent'].set()
    return
