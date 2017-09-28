from mesa import Model
#from mesa.time import RandomActivation
from mesa.time import BaseScheduler
from agent import Robosim_agent
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
import astar
from enum import Enum
from types import MethodType
class Robosim_model(Model):
    def __init__(self, num_agents, simulation_map, stubborness, seed = None, step_name = None):
        super().__init__()
        assert isinstance(simulation_map, np.ndarray)
        self.simulation_map = simulation_map
        self.num_agents = num_agents
        self.stubborness = stubborness
        self.schedule = BaseScheduler(self)
        self.communications = 1
        self.usefull_moves = []
        if seed is not None:
            random.seed(seed)

        height = self.height = self.simulation_map.shape[0]
        width = self.width = self.simulation_map.shape[1]
        self.explored_map = np.empty(self.simulation_map.shape, dtype=np.object)
        self.explored_map.fill(CellState.UNEXPLORED)

        self.grid = SingleGrid(width, height, False)
        Robosim_agent.step = Robosim_agent.step_pesante if step_name == "pesante" else \
                             Robosim_agent.step_astar if step_name == "astar" else \
                             Robosim_agent.step_simple if step_name == "simple" else None
        for i in range(self.num_agents):
            a = Robosim_agent(i, self, self.stubborness)
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
            model_reporters={"Esplorate": self.conta_esplorate, "Comunicazioni": self.get_communications, "Mosse utili":self.get_usefull_moves})

    def step(self):
        self.communications = 0
        self.usefull_moves = 0
        for agent in self.schedule.agents:
            self.look(agent)
        self.find_border_cell()
        if len(self.border_cell) == 0:
            self.running = False
            return
        self.schedule.step()
        self.datacollector.collect(self)
        #print_map(self.explored_map)

    #Controlla se esistono celle esplorate che confinano con celle non esplorate
    def find_border_cell(self):
        self.border_cell.clear()
        for (y,x), val in np.ndenumerate(self.explored_map):
            if val != CellState.EMPTY:
                continue
            vicinato = self.explored_map[y-1 : y+2, x-1 : x+2].flatten()
            if CellState.UNEXPLORED in vicinato:
                self.border_cell += [(x,y)]
        #for x in range(self.grid.width):
        #    for y in range(self.grid.height):
        #        if self.explored_map[y][x] != CellState.EMPTY:
        #            continue
        #        x_range, y_range = self.get_map_range(1, (x,y))
        #        is_border_cell = False
        #        for x1 in x_range:
        #            if is_border_cell:
        #                break
        #            for y1 in y_range:
        #                if x != x1 and y != y1:
        #                    if self.explored_map[y1][x1] == CellState.UNEXPLORED:
        #                        is_border_cell = True
        #                        break
        #        if is_border_cell:
        #            self.border_cell.append((x,y))
                #print(self.border_cell, )
        #print(len(self.border_cell), len(asd))
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
        explored_cells = 0
        self.communications += 1
        x_range, y_range = self.get_map_range(1, (agent.pos[0], self.simulation_map.shape[0] - agent.pos[1] - 1))
        for x1 in x_range:
            for y1 in y_range:
                if self.explored_map[y1][x1] == CellState.UNEXPLORED:
                    self.communications += 1
                    explored_cells += 1
                self.explored_map[y1][x1] = self.simulation_map[y1][x1]
        
        self.usefull_moves += explored_cells
    def norm2mesa(self, pos): 
        return (pos[0], (self.simulation_map.shape[0] - pos[1] - 1))
    def mesa2norm(self, pos):
        return self.norm2mesa(pos)
    def get_communications(self, model):
        return self.communications
    def conta_esplorate(self, model): 
        mappa = self.explored_map
        return np.count_nonzero(mappa != CellState.UNEXPLORED)
    def get_usefull_moves(self, model):
        return self.usefull_moves / self.num_agents
class CellState(Enum):
    UNEXPLORED = 0
    EMPTY = 1
    OBSTACLE = 2

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


