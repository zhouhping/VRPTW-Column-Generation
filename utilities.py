import numpy as np

def readData(filename, n):
    stream = ""
    with open(filename, "r") as file:
        stream = file.readlines()
    if stream == "":
        print("Error in reading file")

    vehicleNumber, capacity = [int(i) for i in stream[4].split()]
    fields = stream[7].split()

    data = list()
    for i in range(9, len(stream)):
        if stream[i] == "\n":
            continue

        val = stream[i].split()
        if len(val) != len(fields):
            print("Error in reading data")
            continue

        customer = dict(zip(fields, val))
        data.append(customer)

    # Consider only depot + 50 customers
    data = data[0:n+1]
    data.append(data[0]) # The depot is represented by two identical
                         # nodes: 0 and n+1
    data[-1]["CUST-NO."] = "51"

    x = []; y = []; q = []; a = []; b = []
    for customer in data:
        x.append(int(customer["XCOORD."]))
        y.append(int(customer["YCOORD."]))
        q.append(int(customer["DEMAND"]))
        a.append(int(customer["READY-TIME"]))
        b.append(int(customer["DUE-DATE"]))

    return vehicleNumber, capacity, x, y, q, a, b


def createDistanceMatrix(x, y):
    # TODO: arrotondare distanze a prima cifra decimale
    n = len(x)
    d = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            p1 = np.array([x[i], y[i]])
            p2 = np.array([x[j], y[j]])
            d[i,j] = round(np.linalg.norm(p1-p2), 1)
    return d


"""
Create some dummy feasible paths for initializing the master problem. For each
customer, create a path that starts from the depot, visits the customer and
returns to the depot. This violates the maximum number oh vehicles, but actually
we don't have a constraint about that.
"""
def initializeDummyPaths(d, n):
    a = np.zeros((1,n+2, n+2))          # path matrix
    a[0,0,1] = 1
    a[0,1,-1] = 1
    c = np.array([d[0,1] + d[1, -1]])   # costs array

    for i in range(2, n+1):
        path = np.zeros((1,n+2,n+2))
        path[0,0,i] = 1
        path[0,i,-1] = 1
        a = np.append(a, path, axis=0)
        c = np.append(c, d[0,i] + d[i,-1])

    return a, c


def printPath(path, dim, filename):
    nodes = list()
    nodes.append(0)
    actualNode = 0
    while True:
        thereIsOne = False
        for j in range(dim):
            if path[actualNode, j] == 1:
                nodes.append(j)
                actualNode = j
                thereIsOne = True
                break

        if not thereIsOne:
            break

    if len(nodes) > 3:
        with open(filename, "a") as f:
            f.write(str(nodes))
            f.write("\n")

    return