#dataMiner.py
import numpy as np
import csv
import os

#----------------------------------------------------------------------------------
class DataMiner(object):
  '''
  Description--------------
  Pulls data in from a csv file and marshalls it into a dict with the classes
  and their names, as well as a np.ndarray.  np.save() and np.load() are used for
  marshalling the data

  Functions----------------
  @todo Document functions here

  '''

#PUBLIC***********************************************************************
  #-------------------------------------------------------------------------
  def __init__(self, inputFile, outputFile):
    '''
    Arguments----------------
    inputFile: The path to the file to read the data in from
    outputFile: The path to the file to output the marshalled data
    '''
    
    #VARIABLES
    self.data = np.ndarray
    self.classes = {}
    self.inputFile = ''
    self.outputFile = ''

    #Input Variables -----------------------        
    #Sanity Checks

    #{ Checks that inputFile is a valid path
    if (inputFile not isinstance(inputFile, str)):
      raise AssertionError('inputFile must be a string')
    if os.path.exists(filePath):
      pass
    elif os.access(os.path.dirname(inputFile), os.W_OK):
      pass
    else:
      raise AssertionError('You cannot write to the path specified by inputFile')
    #}

    #{ Checks that outputFile is a valid path
    if (outputFile not isinstance(outputFile, str)):
      raise AssertionError('outputFile must be a string')
    if os.path.exists(filePath):
      pass
    elif os.access(os.path.dirname(outputFile), os.W_OK):
      pass
    else:
      raise AssertionError('You cannot write to the path specified by outputFile')
    #}
    
    #{ Assigns arguments to class variables
    self.intputFile = inputFile
    self.outputFile = outputFile
    #}

#program entry
#==================================================================================
