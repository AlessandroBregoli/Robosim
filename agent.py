from mesa import Agent
import model

class Robosim_agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        goal = self.find_goal()
        best_direction = None
        best_distance = 99999
        x_range, y_range = self.model.get_map_range(1,self.pos)
        for x in x_range:
            for y in y_range:
                if x == self.pos[0] and y == self.pos[1]:
                    continue
                if self.model.grid.is_cell_empty((x,y)) and self.model.simulation_map[y][x] != model.CellState.OBSTACLE:
                    distance = self.geometric_distance((x,y), goal)
                    if distance < best_distance:
                        best_distance = distance
                        best_direction = (x,y)
        if best_direction != None:
            self.model.grid.move_agent(self, best_direction)

    def find_goal(self):
        best_goal = None
        best_score = 0
        for x,y in self.model.border_cell:
            score = self.geometric_distance((x,y), self.pos)**2
            for agent in self.model.schedule.agents:
                score -= self.geometric_distance((x,y), agent.pos) **2
            if score < best_score or best_goal == None:
                best_score = score
                best_goal = (x,y)
        return best_goal


    def geometric_distance(self, pos1, pos2):
        return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**(1/2)