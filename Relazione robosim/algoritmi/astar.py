def A*(start, goal)
    # L'insieme dei nodi analizzati
    closedSet = {}

    # L'insieme dei nodi scoperti ma non ancora analizzati.
    # All'inizio contiene solo il nodo di start.
    openSet = {start}

    # Per ogni nodo, memorizziamo il nodo da cui può essere raggiunto più
    # efficientente. Se un nodo può essere raggiunto da più nodi, cameFrom
    # conterrà il più efficiente.
    cameFrom = the empty map

    # Per ogni nodo, il costo di raggiungerlo dal nodo iniziale.
    gScore = map with default value of Infinity

    # Il costo per andare dallo start allo start è 0.
    gScore[start] = 0

    # Per ogni nodo, il costo totale per arrivare dal nodo iniziale al goal
    # passando da quel nodo. Questo valore è parzialmente noto, e in parte
    # stimato.
    fScore = map with default value of Infinity

    # Per il primo nodo, tale valore è del tutto euristico.
    fScore[start] = heuristic_cost_estimate(start, goal)

    while openSet is not empty
        current = the node in openSet having the lowest fScore[] value
        if current = goal
            # siamo arrivati a destinazione: ricostruiamo il path
            return reconstruct_path(cameFrom, current)
        
        openSet.Remove(current)
        closedSet.Add(current)

        for each neighbor of current
            if neighbor in closedSet
                continue        # Ignora i vicini già analizzati.

            if neighbor not in openSet    # Scoperto un nuovo nodo
                openSet.Add(neighbor)
            
            # Distanza dallo start al vicino analizzato
            tentative_gScore = gScore[current] + dist_between(current, neighbor)
            if tentative_gScore >= gScore[neighbor]
                continue        # Il path scoperto non è migliore.

            # Il path è il migliore
            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + 
                                         heuristic_cost_estimate(neighbor, goal) 

    return failure

def reconstruct_path(cameFrom, current)
    total_path = [current]
    while current in cameFrom.Keys:
        current = cameFrom[current]
        total_path.append(current)
    return total_path
