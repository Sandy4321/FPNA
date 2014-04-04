#Parallel FPNA implementation
import tissue
from multiprocessing import Process

L1 = tissue.Link(1.0, 1.0)
L2 = tissue.Link(2.0, 2.0)

L1.appendOutput(L2)
L2.appendInput(L1)

if __name__ == '__main__':
 #fork Processes...
