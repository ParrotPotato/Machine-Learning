# Assignment 1 - Decision tree
# Name    : Nitesh Meena
# Roll    : 16CS30023
# Execute : python3.6 16CS30023_a1.py 
#           in the same folder as the data1_19.csv is stored
#
# Program developed for Python 3.6 
# The program implements a decision tree for the given data given in file data1_19.csv 

import math as mt 
import random 

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value= value
        self.child= []

    def draw(self, spacecount = 0):
        
        for i in range(spacecount):
            print("\t", end = "")

        if spacecount == 0:
            print("Root : ")
        else:
            print(self.name + ":" + self.value)

        if self.name == "Leaf":
            return
        
        for i in self.child:
            i.draw(spacecount + 1)

        return
    
    def test(self, datapoint):
        
        if self.child[0].name == "Leaf":
            if self.child[0].value == datapoint[len(datapoint) - 1]:
                return True
            return False
        
        valueindex = g_col.index(self.child[0].name)
 
        for c in self.child:
            if c.value == datapoint[valueindex]:
                return c.test(datapoint)

        return False

def loadDataset():
    emptylist = []

    with open ("data1_19.csv", "r") as inputfile:
        emptylist = inputfile.readlines()
    
    lines = [i.strip().split(',') for i in emptylist]
    return lines


def getEntropy(dataset):
    yes = 0
    no = 0

    for i in dataset:
        if i[-1] == "yes":
            yes = yes + 1    
        else:
            no = no  + 1

    if yes == 0:
        return 0.0
    if no == 0:
        return 0.0

    total = yes + no
    return -1 * ((yes / total) * mt.log2((yes / total)) + (no / total) * mt.log2((no / total)))

def splitDatasetAtAttr(data, attr):
    index = g_col.index(attr)
    uniquelist = []

    for i in data:
        if i[index] in uniquelist:
            continue
        else:
            uniquelist.append(i[index])

    spliteddataset = [[] for i in range(len(uniquelist))]

    for i in data:
        spliteddataset[uniquelist.index(i[index])].append(i)
    
    return spliteddataset

def getInformationGain(data, attr):

    totalentropy = getEntropy(data)

    spliteddataset = splitDatasetAtAttr(data, attr)
    
    informationgain = 0.0

    for i in spliteddataset:
        informationgain = informationgain + len(i)/len(data) * getEntropy(i)
    
    returnvalue = totalentropy - informationgain

    return returnvalue

def generateLeaf(data):
    yescounter = 0 
    nocounter = 0

    for i in data:
        if i[-1] == "yes":
            yescounter = yescounter + 1 
        else:
            nocounter = nocounter + 1 
    
    if yescounter > nocounter:
        return Node("Leaf", "yes")
    return Node("Leaf", "no")

def generateTree(data, name, value, functionskippable ):
    # get the maximum information gain 
    maxinformationgainattr = ""
    maxinformationgain = -1.0
    
    localskippable = []
    for i in functionskippable:
        localskippable.append(i)

    for attr in g_col:
        if attr in localskippable:
            continue

        informationgain = getInformationGain(data, attr) 
        if informationgain > maxinformationgain:
            maxinformationgain = informationgain
            maxinformationgainattr = attr

    if maxinformationgain == -1.0:
        returnnode = Node(name, value)
        returnnode.child.append(generateLeaf(data))
        return returnnode
    
    splitted = splitDatasetAtAttr(data, maxinformationgainattr)

    localskippable.append(maxinformationgainattr)

    treenode = Node(name, value)

    for datasubset in splitted:
        treenode.child.append(generateTree(datasubset, maxinformationgainattr, datasubset[0][g_col.index(maxinformationgainattr)] , localskippable))

    return treenode

def testTree(treenode, testdata):
    counter = 0

    for datapoint in testdata:
        returnvalue = treenode.test(datapoint)
        if returnvalue == True:
            counter = counter + 1
    
    return (float(counter) / float(len(testdata)))

# loading data from file 

lines = loadDataset()
g_col = lines[0]

# seperating this into modeling and testing data

newlines = lines[1:]

g_data = []
g_test = []

random.seed(2308)

testpointcount = 200

uniquelist = []
i = 0 
while i < testpointcount:
    temp = random.randint(0, len(newlines) - 1)
    if temp in uniquelist:
        continue
    
    uniquelist.append(temp)
    g_test.append(newlines[temp])
    i = i + 1

for row in newlines:
    if newlines.index(row) in uniquelist:
        continue    
    g_data.append(row)

skippable = []
skippable.append(g_col[-1])

treeroot = generateTree(g_data, "", "", skippable)
treeroot.draw()

print("Test Accuracy : " + str(testTree(treeroot, g_test) * 100) + "%")
