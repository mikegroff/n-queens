from collections import deque
import time
import copy
import numpy as npy
import matplotlib.pyplot as plt

def author():
    return 'mgroff3'

class Node:
    def __init__(self, label, row, col):
        self.label = label
        self.row = row
        self.col = col
        self.neighbors = set()
        self.ns = 0
        self.ndoms = []

class Graph:
    # literally just a dictionary mapping nodes to string labels
    def __init__(self,nodes,rows):
        self.nodes = nodes
        self.rows = rows

def printindex(list,graph):# prints node indecies from search returned list
    for l in list:
        v = graph.nodes.get(l)
        print(v.row,v.col)

def Board(n):
    #a complete graph where all positions on the board are connected
    map = {}
    rows = npy.array(npy.zeros(n))
    for i in range(0,n):
        row = []
        for j in range(0,n):
            k = i*n+j #unique label for each row/col positions
            v = Node(k,i,j)
            v.neighbors = set(range(0,n*n)) - set([k])
            map[k] = v
            row.append(k)
        row = npy.array(row)
        rows = npy.vstack((rows,row))
    v = Node(-1,-1,-1) # inital node that lets us pick a starting point in the graph
    v.neighbors = set(range(0,n*n))
    map[-1] = v
    return Graph(map,rows[1:,:])

def val(pos,graph):
    for a in pos:
        p = graph.nodes.get(a)
        for b in (pos-set([a])):
            r = graph.nodes.get(b)
            if ( r.row == p.row or r.col ==p.col or (r.col - r.row) == (p.col - p.row) or (r.col + r.row) == (p.col + p.row)):
                return False
    return True

def removen(label,graph):
    r = graph.nodes.get(label)
    nbh = copy.copy(r.neighbors)
    for n in nbh:
        p = graph.nodes.get(n)
        if ( r.row == p.row or r.col ==p.col or (r.col - r.row) == (p.col - p.row) or (r.col + r.row) == (p.col + p.row)):
            r.neighbors.remove(p.label)
    r.ns = len(r.neighbors)

def bt(size):
    s = time.clock()
    Graph = Board(size)
    stack = [[-1]]
    stack = deque(stack) #this is the queue
    n = stack.pop()
    next = n[-1]
    nbh = Graph.nodes.get(next).neighbors
    for nb in nbh:
        np = copy.copy(n)
        np.append(nb) # generating path
        stack.append(np) # adding to stack

    while stack: # keeps running while thre are paths to consider
        #print stack
        n = stack.pop()
        nn = set(n) - set([-1])
        next = n[-1]
        #print (next)
        if (len(nn) < len(n)-1) or (val(nn,Graph) == False): #check for validity of path
            continue
        if len(n) == size+1: #if valid and has n queens + start position
            return n[1:]
        nbh = Graph.nodes.get(next).neighbors
        for nb in nbh:
            np = copy.copy(n)
            np.append(nb) # generating path
            stack.append(np) # adding to stack
        if (time.clock()-s) > 600:
            break
    return []

def ss(size):
    s = time.clock()
    Graph = Board(size)
    stack = [[-1]]
    stack = deque(stack) #this is the queue
    n = stack.pop()
    next = n[-1]
    nbh = Graph.nodes.get(next).neighbors
    for nb in nbh:
        np = copy.copy(n)
        np.append(nb) # generating path
        stack.append(np) # adding to stack

    while stack: # keeps running while thre are paths to consider
        #print stack
        n = stack.pop()
        nn = set(n) - set([-1])
        next = n[-1]
        if len(n) == size+1: #if valid and has n queens + start position
            if (len(nn) < len(n)-1) or (val(nn,Graph) == False): #check for validity of path
                continue
            else:
                return n[1:]
        nbh = Graph.nodes.get(next).neighbors
        for nb in nbh:
            np = copy.copy(n)
            np.append(nb) # generating path
            stack.append(np) # adding to stack
        if (time.clock()-s) > 600:
            break
    return []

def btfc(size):
    s = time.clock()
    Graph = Board(size)
    stack = [[-1]]
    stack = deque(stack) #this is the queue
    n = stack.pop()
    next = n[-1]
    nbh = Graph.nodes.get(next).neighbors
    for nb in nbh:
        removen(nb,Graph)
        np = copy.copy(n)
        np.append(nb) # generating path
        stack.append(np) # adding to stack

    while stack: # keeps running while thre are paths to consider
        #print stack
        n = stack.pop()
        nn = set(n) - set([-1])
        next = n[-1]
        #print (next)

        if len(n) == size+1: #if valid and has n queens + start position
            return n[1:]
        nbh =(intsec(nn,size,Graph) & Graph.nodes.get(next).neighbors) - set(n)
        for nb in nbh:
            np = copy.copy(n)
            np.append(nb) # generating path
            stack.append(np) # adding to stack
        if (time.clock()-s) > 600:
            break
    return []

def intsec(st,n,g):
    sect = set(range(0,n*n))
    for s in st:
        sect = sect & g.nodes.get(s).neighbors
    return sect

def btfcdo(size):
    #ordering will be based on mcv and lcv
    s = time.clock()
    Graph = Board(size)
    stack = [[-1]]
    stack = deque(stack) #this is the queue
    n = stack.pop()
    next = n[-1]
    nbh = Graph.nodes.get(next).neighbors
    nbs = []
    for nb in nbh:
        removen(nb,Graph)# forward checking one step in advance as we have to order by lcv
        z = len(Graph.nodes.get(nb).neighbors)
        nbs.append(z)
    nbs = npy.array(nbs)
    ind = npy.argsort(nbs)
    nbh = list(npy.take(npy.array(list(nbh)),ind))
    nbh.reverse()
    for nb in nbh:
        np = copy.copy(n)
        np.append(nb) # generating path
        stack.append(np) # adding to stack

    while stack: # keeps running while there are paths to consider
        n = stack.pop()
        nn = set(n) - set([-1])
        #print(nn)
        next = n[-1]
        if len(n) == size+1: #if valid and has n queens + start position
            return n[1:]
        nbh = (intsec(nn,size,Graph) & Graph.nodes.get(next).neighbors) - set(n)
        lengths = []
        for i in range(0,size):
            row = set([int(x) for x in list(Graph.rows[i,:])])
            row = row & nbh
            lengths.append(len(row))
        lengths = npy.argsort(npy.array(lengths))
        lengths = npy.flip(lengths)
        for j in lengths:
            domres = []
            row = set([int(x) for x in list(Graph.rows[j,:])]) & nbh
            #orows = set([int(x) for x in list(Graph.rows[0:j,:].flatten())]).union(set([int(x) for x in list(Graph.rows[j+1:,:].flatten())])) & nbh
            lrow = list(row)
            #print(lrow)
            for k in lrow:
                domres.append(len((nbh-row) & Graph.nodes.get(k).neighbors))
            domres = npy.argsort(npy.array(domres))
            #domres = npy.flip(domres)
            lrow = list(npy.take(npy.array(lrow), domres))
            for nb in lrow:
                np = copy.copy(n)
                np.append(nb) # generating path
                stack.append(np) # adding to stack
        if (time.clock()-s) > 600:
            break
    return []



if __name__=="__main__":
    #note that if a solution does not exist wewill return and empty list for all searches
    #also note that this is only true for n=2,3
    """
    print("N Queens")
    s = time.clock()
    print(bt(10))
    print(time.clock()-s)
    """
    t = 600 #tenminutes
    i = 1
    label1 = []
    times1 = []
    tot = 0
    while tot < t:
        s = time.clock()
        sol = ss(i)
        tot = time.clock()-s
        print(tot)
        label1.append(i)
        times1.append(npy.log(tot))
        i +=1
    i = 1
    label2 = []
    times2 = []
    tot = 0
    while tot < t:
        s = time.clock()
        sol = bt(i)
        tot = time.clock()-s
        print(tot)
        label2.append(i)
        times2.append(npy.log(tot))
        i +=1
    i = 1
    label3 = []
    times3 = []
    tot = 0
    while tot < t:
        s = time.clock()
        sol = btfc(i)
        tot = time.clock()-s
        print(tot)
        label3.append(i)
        times3.append(npy.log(tot))
        i +=1
    i = 1
    label4 = []
    times4 = []
    tot = 0
    while tot < t:
        s = time.clock()
        sol = btfcdo(i)
        tot = time.clock()-s
        print(tot)
        label4.append(i)
        times4.append(npy.log(tot))
        i +=1
    bar = npy.log(t*npy.ones(len(label4)))
    plt.plot(label1,times1,label2,times2,label3,times3,label4,times4, label4, bar,'--')
    plt.xlabel("# of Queens n")
    plt.ylabel("Computation time(s) (logarithmic)")
    plt.legend(["Standard", "BT","BT w/ FC", "BT w/ FC + DO"])
    plt.show()













    print("finished")
