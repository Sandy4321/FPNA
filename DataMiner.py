#dataMiner.py
import numpy as np
import csv
import os
import random

#==============================================================================
#------------------------------------------------------------------------------
class DataMiner(object):
  '''
  Description--------------
  Pulls data in from a csv file and marshalls it into a dict with the classes
  and their names, as well as a np.ndarray.  np.save() and np.load() are used
  for marshalling the data.  Each DataMiner class is meant to be associated
  with one set of data.  That is, make a new DataMiner class for every new
  set of data.

  Functions----------------
  @todo Document functions here
  '''

#PUBLIC***********************************************************************
  #----------------------------------------------------------------------------
  def __init__(self, dataFile, marshallFile=None):
    '''
    Arguments----------------
    dataFile: The path to the file to read the raw data in from.  It will 
    then output to a file with a similar name with a .mined extension.  The
    input data must be a csv file. With parameter names in the top row, and a
    row named 'class' which will be used for classification.  If the 'class'
    header is not given, it will automatically create classes based on the
    last column.

    marshalledFile: The path to the file with which to marshall data.  It will
    be created if it does not already exist.

    Variables----------------
    dataFeatures: A np.array containing feature vectors.  

    dataClasses: A np.array containing (integer) class labels for the features.
    
    dataLabels: A list containing the labels for the features.  ie, what the
    number represent.

    classNameToInt: A dictionary indexed by string class names to give their
    integer representation

    classIntToName: A dictionary indexed by integers to output the class name
    represented by that number

    dataFile: The file from which the original data was mined

    marshallFile: The file to which the data is marshalled.
    '''
    
    #VARIABLES
    self.dataFeatures = np.array([])
    self.dataClasses = np.array([])
    self.dataLabels = []
    self.classNameToInt = {}
    self.classIntToName = {}
    self.dataFile = ''
    self.marshallFile = ''

    #Input Variables -----------------------        
    #Sanity Checks

    try:
      if dataFile[0:2] == './':
        dataFile = dataFile[2:]
    except IndexError:
      pass

    try:
      if(marshallFile != None):
        if marshallFile[0:2] == './':
          marshallFile = marshallFile[2:]
    except IndexError:
      pass

    #{ Checks that dataFile is a valid path
    if (os.path.exists('./' + dataFile)):
      if (not os.access(os.path.dirname('./' + dataFile), os.R_OK)):
        raise AssertionError('You need read access to ' +  dataFile)
      pass
    else:
      raise AssertionError(dataFile + ' does not exist!')
    #}

    #{ Checks that marshallFile is a valid path
    if(marshallFile != None):
      if (not os.access(os.path.dirname('./' + marshallFile), os.W_OK)):
        raise AssertionError('You need write access to: ' +  marshallFile)
    #}

    #{ Assigns arguments to class variables
    self.dataFile = dataFile
    self.marshallFile = marshallFile
    #}

    return

  #--------------------------------------------------------------------------
  def shuffleData(self):
    '''
    This function simply randomizes the order of all the data vectors.
    '''
    print 'Randomizing data ... ',
    temp = np.array([])
    temp = np.hstack((self.dataFeatures, self.dataClasses))
    np.random.shuffle(temp)
    self.dataFeatures, self.dataClasses = np.hsplit(temp, 
                                                    [np.shape(temp)[1]-1])
    print 'Done'
#    print self.dataFeatures
    return

  #--------------------------------------------------------------------------
  def getAllData(self):
    '''
    Returns the data stored in the dataMiner's class variables as a tuple.
    returns: (dataFeatures, dataClasses, classNameToInt, classIntToName,
    dataLabels)

    dataFeatures: The features of the data.

    dataClasses: The corresponding class labels for the data, as integers

    classNameToInt: A dictionary containing names of classes and their
    corresponding integer representation

    classIntToName: A dictionary containing integer representation of
    classes and their names
    '''
    return (self.dataFeatures, self.dataClasses,
            self.classNameToInt, self.classIntToName,
            self.dataLabels)

  #--------------------------------------------------------------------------  
  def getTrainData(self):
    '''
    Returns 70% of the data to form a training set.
    Returns a tuple containing ((70%) dataFeatures, (70%) dataClasses)
    '''
    
    dataLen = len(self.dataFeatures)
    returnAmount = np.ceil(dataLen*0.7)
    return self.dataFeatures[0:returnAmount], self.dataClasses[0:returnAmount]    

  #--------------------------------------------------------------------------
  def getTestData(self):
    '''
    Returns 20% of the data for a test set.
    Returns a tuple containing ((20%) dataFeatures, (20%) dataClasses)
    '''
    
    dataLen = len(self.dataFeatures)
    returnAmount = np.ceil(dataLen*0.2)
    trainAmount = np.ceil(dataLen*0.7)
    return (self.dataFeatures[trainAmount:trainAmount + returnAmount],
            self.dataClasses[trainAmount:trainAmount + returnAmount])

  #--------------------------------------------------------------------------
  def getValidationData(self):
    '''
    Returns 10% of the data for a validation set.
    Returns a tuple containing ((10%) dataFeatures, (10%) dataClasses)
    '''
    
    dataLen = len(self.dataFeatures)
    usedAmount = np.ceil(dataLen*0.7) + np.ceil(dataLen*0.2)
    return (self.dataFeatures[usedAmount:], self.dataClasses[usedAmount:])

  #--------------------------------------------------------------------------
  def mineData(self):
    '''
    Gathers data from the file given at initialization.  It is assumed to 
    be a comma seperated value file.  It also asks that the top row be 
    labels for the data.  Such as 'sepal length', 'colour' etc...
    And, that one of the lables be called 'class'.  This will give a name
    to each of the classes to which the data belongs.  In the future,
    support for un-labled data may be added, but I have no reason to do 
    so now.  Read access is necessary.
    '''
    
    print 'Gathering data from ', self.dataFile, ' ... ',
    numClasses = 0
    with open(self.dataFile, 'rb') as csvFile:
      csvReader = csv.reader(csvFile, delimiter=',')
      self.dataLabels = csvReader.next()
      try:
        classIndex = self.dataLabels.index('class')
      except ValueError:
        classIndex = len(self.dataLabels) - 1
    
      self.dataFeatures = np.zeros(shape = [1,len(self.dataLabels) - 1])
      self.dataClasses = np.zeros(shape = [1,1])
      for line in csvReader:
        if (line == []): continue #Incase there is a blank line...
        if (not line[classIndex] in self.classNameToInt.keys()):
          self.classNameToInt[line[classIndex]] = numClasses
          self.classIntToName[numClasses] = line[classIndex]
          numClasses += 1

        feature = map(float, [fl for fl in line
                              if line.index(fl) != classIndex])
        self.dataFeatures = np.vstack([self.dataFeatures, feature])
        self.dataClasses = np.vstack([self.dataClasses, 
                                     self.classNameToInt[line[classIndex]]])

      self.dataFeatures = self.dataFeatures[1:]
      self.dataClasses = self.dataClasses[1:]
      print 'Done'
      return

  #-------------------------------------------------------------------------
  def normalizeData(self):
    '''
    Normalizes the data by subtracting the mean value from each feature
    and then dividing by the standard deviation.
    '''
    print 'Normalizing data ... ',
    mean = np.mean(self.dataFeatures, axis = 0)
    SD = np.std(self.dataFeatures, axis = 0)
    self.dataFeatures = np.subtract(self.dataFeatures, mean)
    self.dataFeatures = np.divide(self.dataFeatures, SD)
    print 'Done'
    return

  #-------------------------------------------------------------------------
  def saveData(self):
    '''
    Saves the mined data in a marshalled file.  If a file name isn't
    specified at initialization it will remove the file extension(if there
    is one) of the input file, and add the '.marshalled' extension.  It 
    will also hide the .marshalled file by appending a '.'.  Write access
    is necessary.
    '''
    if self.marshallFile == None:
      fileName = self.dataFile.split('.')[0]
      fileName = '.' + fileName + '.marshalled'
    else:
      fileName = self.marshallFile
    
    if(not os.access(os.path.dirname('./' + fileName), os.W_OK)):
      raise AssertionError('You must have write access to this file: ' + 
                           fileName)

    print 'Saving data to ', fileName, ' ... ',
    f = open(fileName, 'w')
    data = (self.dataLabels, self.classNameToInt, self.classIntToName,
            self.dataClasses, self.dataFeatures)
    np.save(f, data)
    f.close()
    print 'Done'
    return

      
  #-------------------------------------------------------------------------
  #NOTE np.load() supports memory mapped files
  def loadData(self): 
    '''
    Loads data in from a marshalled file.  If a file name isn't
    specified at initialization it will remove the file extension (if there
    is one) and add a '.marshalled' extension, and append a '.'.  Read
    access is necessary.
    '''
    if self.marshallFile == None:
      fileName = self.dataFile.split('.')[0]
      fileName = '.' + fileName + '.marshalled'
    else:
      fileName = self.marshallFile
    
    if(not os.path.isfile('./' + fileName)):
      raise AssertionError('File does not exist for loading: ' + fileName)
         
      
    if(not os.access(os.path.dirname('./' + fileName), os.R_OK)):
      raise AssertionError('You must have read access to this file: ' +
                           fileName)

    print 'Loading data from ', fileName, ' ... ',

    f = open(fileName, 'r')
    #Throws a cPickle error if the file is corrupt
    (self.dataLabels, self.classNameToInt, self.classIntToName,
     self.dataClasses, self.dataFeatures) = np.load(f)
    f.close()
    print 'Done'
    return

#PRIVATE**********************************************************************

#Unit Tests
#==============================================================================
#@todo Learn about unit tests and put them here...
miner = DataMiner('iris.data')
miner.mineData()
miner.normalizeData()
miner.shuffleData()
miner.saveData()
