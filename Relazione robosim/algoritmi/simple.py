def step_simple(analized_agent):
        goal = find_goal(analized_agent)
        analized_agent.old_goal = analized_agent.goal = goal
        
        direction_found = False
        #Si cerca una mossa da eseguire (anche stare fermi è un'opzione)
        while direzione non trovata:
            direction_found = True           
            x_range, y_range = vicinato di actual_agent
            for x in x_range:
                for y in y_range:
                    #Le smelly cells sono quelle celle su cui il robot è già
                    #passato perseguendo il goal attuale
                    if (x,y) in analized_agent.smelly_cells:
                        continue
                    #Si cerca la cella adiacente libera che minimizza la
                    #distanza geometrica dal goal    
                    if (x,y) è vuoto:
                        distance = geometric_distance((x,y), goal)
                        if distance < best_distance:
                            best_distance = distance
                            best_direction = (x,y)
            
            #Se le smelly_cells impediscono qualunque movimento si tenta di
            #simulare un cammino all'indietro fino a trovare una cella dove è
            #possibile scegliere un nuovo percorso
            if best_direction == None and goal != None and \
                    len(analized_agent.smelly_cells) != 0:
                cleaned = False
                for cella in analized_agent.smelly_cells[1:-1]:
                    x_range, y_range = vicinato di cella:
                    for x in x_range:
                        for y in y_range:
                            if Se la cella(x,y) è vuota e non è una smelly_cell:
                                cleaned = True
                    if cleaned:
                        analized_agent.smelly_cells.remove(cella)
                        break
                if cleaned:
                    continue

                analized_agent.old_goal = None
                goal = analized_agent.find_goal()
                analized_agent.old_goal = analized_agent.goal = goal
                direction_found = False    
        if è stata trovata una direzione:
            analized_agent.smelly_cells.append(analized_agent.pos)
            analized_agent.move_agent(analized_agent, best_direction)
