import numpy as np
import model
import collections
def dist(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**(1/2)

def find_path(explored_map, modello, start, goal, avoidCells):
    #trasformazione coordinate?
    openSet = collections.OrderedDict()
    closedSet = collections.OrderedDict()
    cameFrom = {}
    fScore = {}
    gScore = {}
    #print(explored_map.shape, goal)
    for x, cellContent in np.ndenumerate(explored_map):
        if cellContent == model.CellState.OBSTACLE or x[::-1] in avoidCells:
            avoidCells += [x[::-1]]
        n = x[::-1]
        openSet[n] = None
        fScore[n] = float('inf')
        gScore[n] = float('inf')
    gScore[start] = 0
    fScore[start] = estimate(start,goal)
    print(avoidCells)
    while len(openSet) > 0:
        current = min(openSet, key=lambda x: fScore[x])
        if current == goal:
            return reconstruct_path(cameFrom, current)
        #print(len(openSet))
        openSet.pop(current)
        #print(len(openSet))
        closedSet[current] = None
        xrange, yrange =  modello.get_map_range(1, current)
        neighbors = [(x,y) for x in xrange for y in yrange]
        for x in neighbors: 
            if x in closedSet or x is None or x in avoidCells or x == current:
                continue
            
            openSet[x] = None #potrebbe già essere presente ma tanto è un set
            tentative_gScore = gScore[ current] + dist(current, x)
            if tentative_gScore >= gScore[x]:
                continue
            cameFrom[x] = current
            gScore[x] = tentative_gScore
            fScore[x] = gScore[x] + estimate (x, goal)
    return None


def estimate(start,goal):
    return dist(start, goal)
    
def reconstruct_path(cameFrom,current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
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

