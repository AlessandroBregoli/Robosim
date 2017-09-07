from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

import model
import numpy as np
import collections

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal

mappa = model.load_map("mappa_3.txt")
class MyCanvas(CanvasGrid):
    def render(self, mod):
        agenti = super().render(mod)
        mappa = mod.explored_map
        assert isinstance(mappa, np.ndarray)
        objs = []
        for y in range(mappa.shape[0]):
            for x in range(mappa.shape[1]):
                if mappa[y][x] == model.CellState.OBSTACLE:
                    objs += [{"Shape": "rect",
                             "Color": "#444",
                             "Filled": "true",
                             "Layer": 0,
                             "h": 1,
                             "w": 1,
                             "x": x,
                             "y": mappa.shape[0]-y-1}]
                elif mappa[y][x] == model.CellState.UNEXPLORED:
                    objs += [{"Shape": "rect",
                             "Color": "#dadada",
                             "Filled": "true",
                             "Layer": 0,
                             "h": 1,
                             "w": 1,
                             "x": x,
                             "y": mappa.shape[0]-y-1}]
        agenti[0] = objs + agenti.get(0)
        return agenti

grid = MyCanvas(agent_portrayal, mappa.shape[1], mappa.shape[0], 400, 400)
chart = ChartModule([{"Label": "Esplorate",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

stub_slider = UserSettableParameter('slider', "Stubborness", 0.5, 0, 1, 0.05)

server = ModularServer(model.Robosim_model,
                       [grid, chart],
                       "Money Model",
                       {"num_agents": 3,"simulation_map":mappa, "stubborness": stub_slider})
server.launch()
