import svgwrite
import model
import numpy as np

cellsize = 20
cellpadding = 1
celltot = cellsize+cellpadding
fontsize = 12

def draw_map(modello):
    explored_map = modello.explored_map
    h,w = explored_map.shape
    svg = svgwrite.Drawing()
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
    svg.save()