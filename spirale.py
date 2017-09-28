import numpy as np

def spirale(raggio = 5):
    if raggio%2!=1:
        raise Exception("il raggio deve essere dispari per qualche motivo")
    spirale = np.ones((raggio*2+1, raggio*2+1), dtype=int)
    centro = (raggio, raggio)
    spirale[centro] = 0
    pos = centro
    passo = 2
    direz = [0, 1]
    for x in range(raggio - 1):
        for x in range(passo):
            pos = (pos[0] + direz[0], pos[1] + direz[1])
            spirale[pos] = 0
        direz[0],direz[1] = -direz[1], direz[0]
        for x in range(passo):
            pos = (pos[0] + direz[0], pos[1] + direz[1])
            spirale[pos] = 0
        direz[0], direz[1] = direz[1], direz[0]
        passo += 2
    #terminare la spirale
    for x in range(passo-2):
        pos = (pos[0] + direz[0], pos[1] + direz[1])
        spirale[pos] = 0
    return spirale

s = spirale(15)
for (y,x), val in np.ndenumerate(s):
    print("#" if val else ".",end="")
    if x == s.shape[1]-1: print()
