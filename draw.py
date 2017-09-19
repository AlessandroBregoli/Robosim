import svgwrite
import model
import numpy as np
from mesa.visualization.modules import ChartModule
import json

cellsize = 20
cellpadding = 1
celltot = cellsize+cellpadding
fontsize = 12

def draw_map(modello,filename):
    explored_map = modello.explored_map
    h,w = explored_map.shape
    svg = svgwrite.Drawing(size=(w*celltot,h*celltot))
    bgrect = svg.rect((0,0), (w*celltot, h*celltot), fill="#eee")
    svg.add(bgrect)
    for (y,x), content in np.ndenumerate(explored_map):
        bg = "#ddd" if content == model.CellState.UNEXPLORED else  \
             "#555" if content == model.CellState.OBSTACLE else \
             "#fff"
        cell = svg.rect((celltot*x,celltot*y),(cellsize,cellsize),fill=bg)
        svg.add(cell)
    for ag in modello.schedule.agents:
        normpos = modello.mesa2norm(ag.pos)
        atxt = svg.text(ag.unique_id, (normpos[0]*celltot, normpos[1] * celltot + fontsize), fill="#f00", font_size= str(fontsize)+ "px")
        svg.add(atxt)
        if ag.goal is not None:
            goal = ag.goal
            gtxt = svg.text(ag.unique_id, (goal[0] *celltot, goal[1]  * celltot + fontsize), fill="#00f", font_size= str(fontsize)+ "px")
            svg.add(gtxt)
    svg.saveas(filename)

def draw_true_map(mappa, filename):
    explored_map = mappa
    h,w = explored_map.shape
    svg = svgwrite.Drawing(size=(w*celltot,h*celltot))
    bgrect = svg.rect((0,0), (w*celltot, h*celltot), fill="#eee")
    svg.add(bgrect)
    for (y,x), content in np.ndenumerate(explored_map):
        bg = "#ddd" if content == model.CellState.UNEXPLORED else  \
             "#555" if content == model.CellState.OBSTACLE else \
             "#fff"
        cell = svg.rect((celltot*x,celltot*y),(cellsize,cellsize),fill=bg)
        svg.add(cell)
    svg.saveas(filename)

class Dict_chart(ChartModule):
    def __init__(self, series, canvas_height=200, canvas_width=500, data_collector_name="datacollector"):
        self.name = series[0]["Label"]
        self.series = [{'Label': x, 'Color': "rgb("+str(int(x*255/10))+","+str(int((x+5)%10*255/10))+","+ str(int((x+7)%10*255/10)) + ")"} for x in range(10)]
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.data_collector_name = data_collector_name

        series_json = json.dumps(self.series)
        new_element = "new ChartModule({}, {},  {})"
        new_element = new_element.format(series_json, canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"


    def render(self, model):
        current_values = []
        data_collector = getattr(model, self.data_collector_name)

        for x in range(10):
            name = self.name
            try:
                val = data_collector.model_vars[name][-1][x]  # Latest value
            except:
                val = 0
            current_values.append(val)
        return current_values

    