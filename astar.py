import numpy as np
import model
import collections
def dist(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**(1/2)
class Node:
    def __init__(self, pos):
        self.neighbors = []
        self.gScore = float('inf')
        self.fScore = float('inf')
        self.pos = pos
    def __str__(self):
        return """pos: {},
gScore: {},
fScore: {}""".format(self.pos,
                     self.gScore,
                     self.fScore)
def find_path(explored_map, modello, start, goal, avoidCells):
    #trasformazione coordinate?
    openSet = collections.OrderedDict()
    closedSet = collections.OrderedDict()
    cameFrom = {}
    #print(explored_map.shape, goal)
    nodes = np.empty(explored_map.shape, dtype=np.object)
    for x, cellContent in np.ndenumerate(explored_map):
        if cellContent == model.CellState.OBSTACLE:
            continue
        if x[::-1] in avoidCells:
            #print("avoid", x[::-1])
            continue
        n = Node(x[::-1])
        nodes[x] = n
        openSet[n] = None
    for x, node in np.ndenumerate(nodes):
        if node is not None:
            node.neighbors = nodes[x[0]-1:x[0]+2, x[1]-1:x[1]+2].flatten()
    try:
        nodes[start[::-1]].gScore = 0
    except:
        print(avoidCells, start)
    nodes[start[::-1]].fScore = estimate(start,goal)
    while len(openSet) > 0:
        current = min(openSet, key=lambda x: x.fScore)
        if current == nodes[goal[::-1]]:
            return reconstruct_path(cameFrom, current)
        openSet.pop(current)
        closedSet[current] = None
        for x in current.neighbors: 
            if x in closedSet or x is None:
                continue
            
            openSet[x] = None #potrebbe già essere presente ma tanto è un set
            tentative_gScore = current.gScore + dist(current.pos, x.pos)
            if tentative_gScore >= x.gScore:
                continue
            cameFrom[x] = current
            x.gScore = tentative_gScore
            x.fScore = x.gScore + estimate (x.pos, goal)
    return None


def estimate(start,goal):
    return dist(start, goal)
    
def reconstruct_path(cameFrom,current):
    total_path = [current.pos]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current.pos)
    return total_path
#test
#import model
#mappa = model.load_map("mappa_3.txt")
#modello = model.Robosim_model(1, mappa, 0.5)
#path = find_path(modello.explored_map, (2,2), (6,17))
#print([x.pos for x in path])
#for x in path:
#    mappa[x.pos] = model.CellState.OBSTACLE
#model.print_map(mappa)

