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
                 "r": 0,
                 "text": agent.unique_id
                 }
    return portrayal

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
        for ag in mod.schedule.agents:
            if ag.goal is not None:
                goal = mod.norm2mesa(ag.goal)
                asd = [{
                    "Shape": "rect",
                    "Color" : "#0000ff",
                    "Filled" : "false",
                    "text" : str(ag.unique_id),
                    "text_color" : "#0000ff",
                    "Layer" : 0,
                    "x" : goal[0],
                    "y" : goal[1],
                    "h" : 0,
                    "w" : 0
                }]
                objs += asd
        agenti[0] = objs + agenti.get(0)
        return agenti

def visualize(mappa, num_agents=3, stubborness=0.5, seed= None, test_name= "", step_name=None):
    grid = MyCanvas(agent_portrayal, mappa.shape[1], mappa.shape[0], mappa.shape[1]*12, mappa.shape[0]*12)
    chart = ChartModule([{"Label": "Esplorate",
                        "Color": "Black"},
                        {"Label": "Comunicazioni", "Color" : "Red"}],
                        data_collector_name='datacollector')

    stub_slider = UserSettableParameter('slider', "Stubborness", stubborness, 0, 1, 0.05)
    agent_slider = UserSettableParameter('slider', "Number of agents", num_agents,1,50,1)

    server = ModularServer(model.Robosim_model,
                        [grid, chart],
                        "Robosim" + test_name,
                        {"num_agents": agent_slider,"simulation_map":mappa, "stubborness": stub_slider,"seed": seed,"step_name": step_name})
    server.launch()
if __name__ == '__main__':
    mappa = model.load_map("mappa_3.txt")
    visualize(mappa)

