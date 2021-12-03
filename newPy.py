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

class Customer:
    def __init__(self, arrival, service, arrivalInterval):
        self.arrivalTime = arrival
        self.serviceTime = service
        self.arrivalInterval = arrivalInterval
    def printCustomer():
        print("This is me")


class Simulation:
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

    def getRandomValue(self, mean):
        return -mean*math.log(random.random())

    def queueUp(self):
        self.totalNumberInQ += (self.simTime - self.prevQTime)*self.qSize
        self.prevQTime = self.simTime
        self.qSize += 1

    def queueDown(self):
        self.totalNumberInQ += (self.simTime - self.prevQTime)*self.qSize
        self.prevQTime = self.simTime
        self.qSize -= 1

    def arrive(self, customerNo):
        # print("customer " + str(customerNo) + " self.arrived at " + str(self.simTime))
        self.arrived += 1
        if(self.serverState == ServerState.IDLE):
            self.nextDepartTime = self.simTime + self.customers[customerNo].serviceTime
            self.inServerCustomer = customerNo
            self.serverState = ServerState.BUSY
        else:
            self.queueUp()

    def depart(self):
        # print("customer " + str(self.inServerCustomer) + " departed at " + str(self.simTime))
        self.totalServerUtilization += self.customers[self.inServerCustomer].serviceTime
        self.completed += 1
        if self.qSize > 0:
            self.queueDown()
            self.inServerCustomer = self.completed
            self.totalDelay += self.simTime - self.customers[self.inServerCustomer].arrivalTime
            self.nextDepartTime = self.simTime + self.customers[self.inServerCustomer].serviceTime
        else:
            self.serverState = ServerState.IDLE


    def triggerEvent(self):
        event = EventType.FINISHED
        minTime = self.infinite
        if(self.arrived < self.totalCustomers and minTime > self.customers[self.arrived].arrivalTime):
            event = EventType.ARRIVE
            minTime = self.customers[self.arrived].arrivalTime
        if(self.serverState == ServerState.BUSY and minTime > self.nextDepartTime):
            event = EventType.DEPART
            minTime = self.nextDepartTime
        if(event != EventType.FINISHED):   
            self.simTime = minTime

        if(event == EventType.ARRIVE):
            self.arrive(self.arrived)
        elif (event == EventType.DEPART):
            self.depart()
        else:
            return
        self.triggerEvent()
        

    def initialize(self):
        arrivalTime = 0
        interval = 0
        totalServiceTime = 0
        for i in range(0, self.totalCustomers):
            serviceTime = self.getRandomValue(self.meanServiceTime)
            totalServiceTime += serviceTime
            self.customers.append(Customer(arrivalTime, serviceTime, interval))
            interval = self.getRandomValue(self.meanIntervalTime)
            arrivalTime += interval
        self.serverState = ServerState.IDLE
        self.arrived = 0


sim = Simulation()
sim.initialize()
sim.triggerEvent()
print(sim.totalDelay/sim.totalCustomers)
print(sim.totalNumberInQ/sim.simTime)
print(sim.totalServerUtilization)
print(sim.simTime)
# initialize()
# triggerEvent()
# print(totalDelay/totalCustomers)
# print(totalNumberInQ/simTime)
# print(totalServerUtilization)