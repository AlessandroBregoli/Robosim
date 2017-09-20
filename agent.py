from mesa import Agent
import model
import astar

class Robosim_agent(Agent):
    def __init__(self, unique_id, model, agent_stubborness = 0.75):
        super().__init__(unique_id, model)
        self.old_goal = None
        self.path = None
        self.smelly_cells = []
        self.agent_stubborness = agent_stubborness
        self.goal = None
    def step_simple(self):
        goal = self.find_goal()
        self.old_goal = self.goal = goal
        best_direction = None
        best_distance = 99999
        normpos = self.model.mesa2norm(self.pos)
        x_range, y_range = self.model.get_map_range(1, normpos)
        direction_found = False
        while not direction_found:
            direction_found = True           
            for x in x_range:
                for y in y_range:
                    if (x,y) == normpos:
                        continue
                    if (x,y) in self.smelly_cells:
                        continue
                    mesaxy = self.model.norm2mesa((x,y))
                    if self.model.grid.is_cell_empty(mesaxy) and self.model.simulation_map[y][x] != model.CellState.OBSTACLE:
                        distance = self.geometric_distance((x,y), goal)
                        if distance < best_distance:
                            best_distance = distance
                            best_direction = (x,y)
            if best_direction == None and goal != None and len(self.smelly_cells) != 0:
                #print(self.unique_id)
                self.old_goal = None
                goal = self.find_goal()
                self.old_goal = self.goal = goal
                direction_found = False
        if best_direction != None:
            self.smelly_cells.append(self.model.mesa2norm(self.pos))
            #best_direction = (best_direction[0], self.model.simulation_map.shape[0] - best_direction[1] - 1)
            best_direction = self.model.norm2mesa(best_direction)
            self.model.grid.move_agent(self, best_direction)
    def step_astar(self):
        goal = self.find_goal()
        if goal == None:
            return
        path = self.path
        #explored_map: coordinate normali
        #self.pos: coordinate mesa
        #goal: coordinate normali
        avoidCells = [] #coordinate normali
        normpos = self.model.mesa2norm(self.pos)
        ricalcolo = 0
        while True:
            if goal != self.old_goal or path is None:
                print("calcolo path")
                path = astar.find_path(self.model.explored_map, self.model,
                                       normpos, goal, avoidCells)
                if path is None:
                    return
                path.pop() #togliere primo passo perché è cella attuale
            if len(path) < 1:
                return
            direction = path.pop()
            mesadirection = self.model.norm2mesa(direction)
            if not self.model.grid.is_cell_empty(mesadirection) or self.model.simulation_map[direction[::-1]] == model.CellState.OBSTACLE:
                if direction == goal:
                    goal = self.find_goal()
                avoidCells += direction
                #print("occupata cella", direction)
                #print("path", path, direction)
                path = None
                ricalcolo += 1
                if ricalcolo < 4:
                    continue
                else:
                    return
            self.model.grid.move_agent(self, mesadirection)
            self.path = path
            self.old_goal = self.goal = goal
            break
    def step_pesante(self):
        goal = self.find_goal()
        if goal == None:
            return
        print(goal)
        path = self.path
        if goal != self.old_goal:
            path = self.modded_dijkstra(goal)
        #print(path)
        is_cell_empty = False
        normpos = self.model.mesa2norm(self.pos)
        while not is_cell_empty:
            is_cell_empty = True
            direction = goal
        
            while path[direction] != normpos:
                #print(direction)
                direction = path[direction]
            #direction = (direction[0], self.model.simulation_map.shape[0] - direction[1] - 1)
            direction = self.model.mesa2norm(direction)
            if not self.model.grid.is_cell_empty(direction):
                path = self.modded_dijkstra(goal)
                is_cell_empty = False
        self.path = path
        self.old_goal = goal
        self.model.grid.move_agent(self, direction)
        
    def find_goal(self):
        best_goal = None
        best_score = 0
        recalculated_old_goal_score = float("inf")
        normpos = self.model.mesa2norm(self.pos)
        for x,y in self.model.border_cell:
            score = self.geometric_distance((x,y), normpos)**2
            for agent in self.model.schedule.agents:
                if agent.unique_id == self.unique_id:
                    continue
                agentnormpos = self.model.mesa2norm(agent.pos)
                score -= self.geometric_distance((x,y), agentnormpos) **2
            if score < best_score or best_goal == None:
                best_score = score
                best_goal = (x,y)
            if (x,y) == self.old_goal:
                recalculated_old_goal_score = score
        if (recalculated_old_goal_score * self.agent_stubborness < best_score  or self.old_goal == best_goal) and self.old_goal != None:
            return self.old_goal
        #self.old_goal = best_goal
        self.smelly_cells = []
        #print("Best goal:" , best_goal)
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
        normpos = self.model.mesa2norm(self.pos)
        dist[normpos] = 0
        while len(v_set) != 0:
            u = min(dist, key=lambda k: dist[k] if k in v_set else float("inf"))
            if dist[u] == float("inf"):
                return path
            #print(u, dist[u])
            v_set.remove(u)
            x_range, y_range = self.model.get_map_range(1, u)
            for x in x_range:
                for y in y_range:
                    alt = dist[u] + 1
                    if (x,y) == u:
                        continue
                    mesaxy = self.model.norm2mesa((x,y))
                    if (not(self.model.grid.is_cell_empty(mesaxy)) and alt == 1) or self.model.simulation_map[y][x] == model.CellState.OBSTACLE:
                        continue
                    
                    if alt < dist[(x,y)]:
                            dist[(x,y)] = alt
                            path[(x,y)] = u
            #if u == goal:
            #    return path
        return path

    def geometric_distance(self, pos1, pos2):
        return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**(1/2)
