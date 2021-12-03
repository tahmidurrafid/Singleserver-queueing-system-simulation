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

    infinite = 1000000000000


    def __init__(self, meanIntervalTime, meanServiceTime, noOfCustomers):
        self.meanIntervalTime = meanIntervalTime
        self.meanServiceTime = meanServiceTime
        self.totalCustomers = noOfCustomers

        self.simTime = 0
        self.qSize = 0
        self.serverState = ServerState.IDLE
        self.customers = []

        self.arrived = 0
        self.completed = 0


        self.inServerCustomer = -1
        self.nextDepartTime = 0

        self.totalDelay = 0
        self.totalNumberInQ = 0
        self.prevQTime = 0
        self.totalServerUtilization = 0
        self.averageDelay = 0
        self.averageNoInQ = 0

        self.initialize()
        self.triggerEvent()
        self.averageDelay = self.totalDelay/self.totalCustomers
        self.averageNoInQ = self.totalNumberInQ/self.simTime

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

    def showReport(self, out):
        out.write("Single-Server queueing system:\n")
        out.write("Mean interrarival time: " + str(self.meanIntervalTime) + "\n")
        out.write("Mean Service Time: " + str(self.meanServiceTime) + "\n")
        out.write("Number of customers: " + str(self.totalCustomers) + "\n\n")

        out.write("Average delay in queue: " + str(round(self.averageDelay, 3)) + "\n")
        out.write("Average number in queue: " + str(round(self.averageNoInQ, 3)) + "\n")
        out.write("Server utilization: " + str(round(self.totalServerUtilization, 3)) + "\n")
        out.write("Time simulation ended: " + str(round(self.simTime, 3)) + "\n")


input = open("in.txt")
meanInterarrivalTime = float(input.readline())
meanServiceTime = float(input.readline())
totalCustomers = int(input.readline())
input.close()

sim = Simulation(meanInterarrivalTime, meanServiceTime, totalCustomers)

out = open("out.txt", "w")
out.write("a) \n")
sim.showReport(out)

out.write("b.\n")

out.close()

csv = open("b.csv", "w")
csv.write("k,Avg. Delay,Avg. No.,Server Util.,Simlation Time\n")
ks = [.5, .6, .7, .8, .9]
for i in range(len(ks)):
    kSim = Simulation(meanInterarrivalTime, meanInterarrivalTime*ks[i], totalCustomers)
    csv.write(str(ks[i])+",")
    csv.write(str(round(kSim.averageDelay, 3)) + "," + str(round(kSim.averageNoInQ, 3)) + "," + 
        str(round(kSim.totalServerUtilization, 3)) + "," + str(round(kSim.simTime, 3)) + "\n")
csv.close()