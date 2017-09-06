from mesa import Agent
import model

class Robosim_agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step_old(self):
        goal = self.find_goal()
        best_direction = None
        best_distance = 99999
        x_range, y_range = self.model.get_map_range(1,(self.pos[0], self.model.simulation_map.shape[0] - self.pos[1] - 1))
        for x in x_range:
            for y in y_range:
                if x == self.pos[0] and y == self.model.simulation_map.shape[0] - self.pos[1] - 1:
                    continue
                if self.model.grid.is_cell_empty((x,self.model.simulation_map.shape[0] - y - 1)) and self.model.simulation_map[y][x] != model.CellState.OBSTACLE:
                    distance = self.geometric_distance((x,y), goal)
                    if distance < best_distance:
                        best_distance = distance
                        best_direction = (x,y)
        if best_direction != None:
            best_direction = (best_direction[0], self.model.simulation_map.shape[0] - best_direction[1] - 1)
            self.model.grid.move_agent(self, best_direction)

    def step(self):
        goal = self.find_goal()
        if goal == None:
            return
        print(goal)
        path = self.modded_dijkstra(goal)
        #print(path)
        direction = goal
        while path[direction] != (self.pos[0], self.model.simulation_map.shape[0] - self.pos[1] - 1):
            print(direction)
            direction = path[direction]
        direction = (direction[0], self.model.simulation_map.shape[0] - direction[1] - 1)
        self.model.grid.move_agent(self, direction)
        
    def find_goal(self):
        best_goal = None
        best_score = 0
        for x,y in self.model.border_cell:
            score = self.geometric_distance((x,y), (self.pos[0], self.model.simulation_map.shape[0] - self.pos[1] - 1))**2
            for agent in self.model.schedule.agents:
                score -= self.geometric_distance((x,y), (agent.pos[0], self.model.simulation_map.shape[0] - agent.pos[1] - 1)) **2
            if score < best_score or best_goal == None:
                best_score = score
                best_goal = (x,y)
        return best_goal
    
    def modded_dijkstra(self, goal):
        path = {}
        dist = {}
        v_set = []
        for x in range(self.model.explored_map.shape[1]):
            for y in range(self.model.explored_map.shape[0]):
                dist[(x,y)] = float("inf")
                v_set.append((x,y))
        
        #v_set.append(self.pos)
        dist[(self.pos[0], self.model.simulation_map.shape[0] - self.pos[1] - 1)] = 0
        while len(v_set) != 0:
            u = min(dist, key=lambda k: dist[k] if k in v_set else float("inf"))
            if dist[u] == float("inf"):
                return path
            print(u, dist[u])
            v_set.remove(u)
            x_range, y_range = self.model.get_map_range(1, u)
            for x in x_range:
                for y in y_range:
                    alt = dist[u] + 1
                    if (x,y) == u:
                        continue
                    if (not(self.model.grid.is_cell_empty((x,self.model.simulation_map.shape[0] - y - 1))) and alt == 1) or self.model.simulation_map[y][x] == model.CellState.OBSTACLE:
                        continue
                    
                    if alt < dist[(x,y)]:
                            dist[(x,y)] = alt
                            path[(x,y)] = u
            #if u == goal:
            #    return path
        return path
        


    def geometric_distance(self, pos1, pos2):
        return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**(1/2)