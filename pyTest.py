import math
import random
import enum
import sys
sys.setrecursionlimit(10000)

class ServerState(enum.Enum):
    BUSY = 1
    IDLE = 2

class EventType(enum.Enum):
    ARRIVE = 1
    DEPART = 2
    FINISHED = 3

meanIntervalTime = 1
meanServiceTime = .5
totalCustomers = 1000

simTime = 0
qSize = 0
serverState = ServerState.IDLE
customers = []

arrived = 0
completed = 0

infinite = 1000000000000

inServerCustomer = -1
nextDepartTime = 0

totalDelay = 0
totalNumberInQ = 0
prevQTime = 0
totalServerUtilization = 0

def getRandomValue(mean):
    return -mean*math.log(random.random())

class Customer:
    def __init__(self, arrival, service, arrivalInterval):
        self.arrivalTime = arrival
        self.serviceTime = service
        self.arrivalInterval = arrivalInterval
    def printCustomer():
        print("This is me")

def queueUp():
    global totalNumberInQ, prevQTime, qSize
    totalNumberInQ += (simTime - prevQTime)*qSize
    prevQTime = simTime
    qSize += 1

def queueDown():
    global totalNumberInQ, prevQTime, qSize
    totalNumberInQ += (simTime - prevQTime)*qSize
    prevQTime = simTime
    qSize -= 1

def arrive(customerNo):
    global arrived, simTime, nextDepartTime, qSize, inServerCustomer, serverState
    # print("customer " + str(customerNo) + " arrived at " + str(simTime))
    arrived += 1
    if(serverState == ServerState.IDLE):
        nextDepartTime = simTime + customers[customerNo].serviceTime
        inServerCustomer = customerNo
        serverState = ServerState.BUSY
    else:
        queueUp()

def depart():
    global simTime, completed, serverState, qSize, inServerCustomer, totalDelay, totalServerUtilization, nextDepartTime
    # print("customer " + str(inServerCustomer) + " departed at " + str(simTime))
    totalServerUtilization += customers[inServerCustomer].serviceTime
    completed += 1
    if qSize > 0:
        queueDown()
        inServerCustomer = completed
        totalDelay += simTime - customers[inServerCustomer].arrivalTime
        nextDepartTime = simTime + customers[inServerCustomer].serviceTime
    else:
        serverState = ServerState.IDLE


def triggerEvent():
    global simTime
    event = EventType.FINISHED
    minTime = infinite
    if(arrived < totalCustomers and minTime > customers[arrived].arrivalTime):
        event = EventType.ARRIVE
        minTime = customers[arrived].arrivalTime
    if(serverState == ServerState.BUSY and minTime > nextDepartTime):
        event = EventType.DEPART
        minTime = nextDepartTime
    if(event != EventType.FINISHED):   
        simTime = minTime

    if(event == EventType.ARRIVE):
        arrive(arrived)
    elif (event == EventType.DEPART):
        depart()
    else:
        return
    triggerEvent()
    

def initialize():
    global inServerCustomer, serverState, arrived
    arrivalTime = 0
    interval = 0
    totalServiceTime = 0
    for i in range(0, totalCustomers):
        serviceTime = getRandomValue(meanServiceTime)
        totalServiceTime += serviceTime
        customers.append(Customer(arrivalTime, serviceTime, interval))
        interval = getRandomValue(meanIntervalTime)
        arrivalTime += interval
    serverState = ServerState.IDLE
    arrived = 0

initialize()
triggerEvent()
print(totalDelay/totalCustomers)
print(totalNumberInQ/simTime)
print(totalServerUtilization)