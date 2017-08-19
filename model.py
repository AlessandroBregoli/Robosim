from mesa import Model
from mesa.time import RandomActivation
from agent import Robosim_agent
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
from enum import Enum
class Robosim_model(Model):
    def __init__(self, num_agents, simulation_map):
        super().__init__()
        assert isinstance(simulation_map, np.ndarray)
        self.simulation_map = simulation_map
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)

        height = self.simulation_map.shape[0]
        width = self.simulation_map.shape[1]

        self.explored_map = np.empty(self.simulation_map.shape, dtype=np.object)
        self.explored_map.fill(CellState.UNEXPLORED)

        self.grid = SingleGrid(width, height, False)
        for i in range(self.num_agents):
            a = Robosim_agent(i, self)
            self.schedule.add(a)
            free_cell = False
            while not free_cell:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                if self.grid.is_cell_empty((x,self.simulation_map.shape[0] - y -1 )) and self.simulation_map[y][x] == CellState.EMPTY:
                    self.grid.place_agent(a, (x ,self.simulation_map.shape[0] - y -1))
                    free_cell = True
        
        self.border_cell = []
        self.datacollector = DataCollector(
            model_reporters={"Esplorate": conta_esplorate})

    def step(self):
        for agent in self.schedule.agents:
            self.look(agent)
        self.find_border_cell()
        if len(self.border_cell) == 0:
            self.running = False
            return
        self.schedule.step()
        self.datacollector.collect(self)
        print_map(self.explored_map)

    #Controlla se esistono celle esplorate che confinano con celle non esplorate
    def find_border_cell(self):
        self.border_cell.clear()
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.explored_map[y][x] != CellState.EMPTY:
                    continue
                x_range, y_range = self.get_map_range(1, (x,y))
                is_border_cell = False
                for x1 in x_range:
                    if is_border_cell:
                        break
                    for y1 in y_range:
                        if x != x1 and y != y1:
                            if self.explored_map[y1][x1] == CellState.UNEXPLORED:
                                is_border_cell = True
                                break
                if is_border_cell:
                    self.border_cell.append((x,y))
    
    #Dato un raggio e una posizione genera 2 range che rappresentano in quadrato di lato radius             
    def get_map_range(self,radius, pos):
        x = pos[0]
        y = pos[1]
        y_max, x_max = self.simulation_map.shape
        x_l = x - radius if x - radius > 0 else 0
        x_u = x + radius if x + radius < x_max else x_max - 1 
        y_l = y - radius if y - radius > 0 else 0
        y_u = y + radius if y + radius < y_max else y_max - 1 
        return (range(x_l, x_u + 1), range(y_l, y_u + 1))

    #Dato un agente la funzione esplora la mappa nel suo raggio visivo
    def look(self, agent):
         x_range, y_range = self.get_map_range(1, (agent.pos[0], self.simulation_map.shape[0] - agent.pos[1] - 1))
         for x1 in x_range:
             for y1 in y_range:
                 self.explored_map[y1][x1] = self.simulation_map[y1][x1]

class CellState(Enum):
    UNEXPLORED = 0
    EMPTY = 1
    OBSTACLE = 2

def conta_esplorate(model): 
	mappa = model.explored_map
	return np.count_nonzero(mappa != CellState.UNEXPLORED)
def load_map(path):
    tmp_ret = []
    with open(path) as mappa:
        for line in mappa.readlines():
            l = []
            line = line[:-1]
            for c in line:
                if c == "#":
                    l.append(CellState.OBSTACLE)
                elif c == ".":
                    l.append(CellState.EMPTY)
            tmp_ret.append(l)
    return np.array(tmp_ret)
        
def print_map(mappa):
    assert isinstance(mappa, np.ndarray)
    for y in range(mappa.shape[0]):
        for x in range(mappa.shape[1]):
            if mappa[y][x] == CellState.EMPTY:
                print(".", end='')
            elif mappa[y][x] == CellState.UNEXPLORED:
                print("-", end='')
            elif  mappa[y][x] == CellState.OBSTACLE:
                print("#", end='')
        print()


