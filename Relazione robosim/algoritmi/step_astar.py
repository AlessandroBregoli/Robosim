def step_astar(agent):
    goal = find_goal(agent)
    if goal == None:
        return
    pos = get_position(position)
    while True:
        #quando cambia il goal, bisogna ricalcolare il path
        if goal != get_old_goal(agent) or path is None:
            path = A*(pos, goal)
            if path is None:
                return
        direction = path.pop()
        if the cell at direction is empty:
            if direction == goal:
                #il goal è raggiunto
                goal = find_goal(agent)
        else:
            path = ricalcola path evitando la cella
            continue
        model.grid.move_agent(agent, direction)
