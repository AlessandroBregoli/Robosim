from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import model

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal

mappa = model.load_map("mappa_1.txt")

grid = CanvasGrid(agent_portrayal, mappa.shape[1], mappa.shape[0], 500, 500)


server = ModularServer(model.Robosim_model,
                       [grid],
                       "Money Model",
                       {"num_agents": 3,"simulation_map":mappa})
server.launch()