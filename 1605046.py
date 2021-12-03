import math
import random
import enum
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)

class ServerState(enum.Enum):
    BUSY = 1
    IDLE = 2

class EventType(enum.Enum):
    ARRIVE = 1
    DEPART = 2
    FINISHED = 3

class Customer:
    def __init__(self, arrival, service, arrivalInterval, intervalRand, serviceTimeRand):
        self.arrivalTime = arrival
        self.serviceTime = service
        self.arrivalInterval = arrivalInterval
        self.intervalRand = intervalRand
        self.serviceTimeRand = serviceTimeRand

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

    def getRandomValue(self, mean, x):
        return -mean*math.log(x)

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
        intervalRand = 0
        serviceTimeRand = 0
        for i in range(0, self.totalCustomers):
            serviceTimeRand = random.random()
            serviceTime = self.getRandomValue(self.meanServiceTime, serviceTimeRand)

            intervalRand = random.random()
            interval = self.getRandomValue(self.meanIntervalTime, intervalRand)            

            totalServiceTime += serviceTime
            self.customers.append(Customer(arrivalTime, serviceTime, interval, intervalRand, serviceTimeRand))
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
        out.write("Time simulation ended: " + str(round(self.simTime, 3)) + "\n\n\n")

    def showStatistics(self, out):
        values = []
        plt.title("Exponential distribution")
        for i in range (0, self.totalCustomers):
            values.append(self.customers[i].arrivalInterval)
        self.computeDistribution(values, self.meanIntervalTime, "x", 
            "P(x)", "Exponential distribution for beta = " + str(self.meanIntervalTime), out)
        plt.show()

        values = []
        plt.title("Exponential distribution")
        for i in range (0, self.totalCustomers):
            values.append(self.customers[i].serviceTime)
        self.computeDistribution(values, self.meanServiceTime, "x", 
            "P(x)", "Exponential distribution for beta = " + str(self.meanServiceTime), out)
        plt.show()

        values = []
        for i in range (0, self.totalCustomers):
            values.append(self.customers[i].intervalRand)
        self.computeDistribution(values, self.meanIntervalTime, "x", "P(x)", "Uniform distribution", out, True)
        plt.show()

    def computeDistribution(self, values, mean, xLabel, yLabel, title, out,uniform = False):
        values.sort()
        median = 0
        if(len(values)%2 == 1):
            median = values[len(values)//2]
        else:
            median = (values[(len(values)-1)//2] + values[len(values)//2])/2 
        min = values[0]
        max = values[len(values)-1]
        out.write(title + "\n\n")
        out.write("Min: " + str(round(min, 7)) + "\n")
        out.write("Max: " + str(round(max, 7)) + "\n")
        out.write("Median: " + str(round(median, 7)) + "\n\n")
        x = [mean/2, mean, 2*mean, 3*mean]
        if(uniform == True):
            x = []
            for i in range(1, 11):
                x.append(i/10)
        y = []
        for i in range (0, len(x)):
            y.append(0)
        index = 0
        for i in range(0, len(values)):
            if values[i] <= x[index]:
                y[index] += 1
            else:
                index += 1
                if index >= len(x):
                    break
        total = 0                
        for i in range(0, len(y)):
            interval = x[i] - (0 if i == 0 else x[i-1])
            y[i] = y[i]/interval
            total += y[i]*interval

        # for i in range(0, len(y)):
        #     total += y[i]
        for i in range(0, len(y)):
            y[i] = y[i]/total
        
        plt.plot(x, y, label = title)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        for i in range(1, len(y)):
            y[i] += y[i-1]
        for i in range(0, len(y)):
            y[i] = y[i]/y[len(y)-1]
        plt.plot(x, y, label = "Cumulative " + title)
        plt.legend()

input = open("in.txt")
meanInterarrivalTime = float(input.readline())
meanServiceTime = float(input.readline())
totalCustomers = int(input.readline())
input.close()

sim = Simulation(meanInterarrivalTime, meanServiceTime, totalCustomers)

out = open("out.txt", "w")
out.write("a) \n")
sim.showReport(out)

out.write("c.\n")

sim.showStatistics(out)

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