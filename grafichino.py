"""Grafichino.

Usage:
    grafichino.py gf <mappa>
"""

import docopt
import matplotlib.pyplot as plt
import json
import numpy as np

def dict_yx(dicty):
    lists = sorted(dicty.items())
    return zip(*lists)
    

if __name__ == "__main__":
    args = docopt.docopt(__doc__, version="-1")
    mappa = args["<mappa>"]
    with open("runall_" + mappa + "_simple.json") as f:
        dati_simple = json.load(f)

    with open("runall_" + mappa + "_astar.json") as f:
        dati_astar = json.load(f)

    step_simple = {int(key):np.mean([len(giro["Comunicazioni"]) for giro in dati_simple[key]]) for key in dati_simple}
    step_astar = {int(key):np.mean([len(giro["Comunicazioni"]) for giro in dati_astar[key]]) for key in dati_astar}
    
    plt.plot(*dict_yx(step_simple))
    plt.plot(*dict_yx(step_astar))
   
    y,x = dict_yx(step_simple)
    plt.plot(y,np.multiply(np.sqrt(y), x))
    y,x = dict_yx(step_astar)
    plt.plot(y,np.multiply(np.sqrt(y),x))
    
    plt.legend(["Step simple", "Step A*", "Step simple per sqrt(n)", "Step A* per sqrt(n)"])
    plt.title("Tempi al variare di n")
    plt.savefig("runall_" + mappa + "_tempi.svg")
    plt.close()
    

    step_std_simple = {int(key):np.std([len(giro["Comunicazioni"]) for giro in dati_simple[key]]) for key in dati_simple}
    step_std_astar = {int(key):np.std([len(giro["Comunicazioni"]) for giro in dati_astar[key]]) for key in dati_astar}
    plt.plot(*dict_yx(step_std_simple))
    plt.plot(*dict_yx(step_std_astar))
    plt.legend(["Step simple", "Step A*"])
    plt.title("Deviazione standard dei tempi al variare di n")
    
    plt.savefig("runall_" + mappa + "_std_tempi.svg")
    plt.close()

    espl_simple = {int(key):np.mean([np.mean(list(giro["Mosse utili"].values())) for giro in dati_simple[key]]) for key in dati_simple}
    espl_astar = {int(key):np.mean([np.mean(list(giro["Mosse utili"].values())) for giro in dati_astar[key]]) for key in dati_astar}
    plt.plot(*dict_yx(espl_simple))
    plt.plot(*dict_yx(espl_astar))
    plt.title("Media di celle esplorate per robot")
    plt.legend(["Step simple", "Step A*"])
    plt.savefig("runall_" + mappa + "_espl.svg")
    plt.close()
    
    com_simple = {int(key):np.mean([np.mean(list(giro["Comunicazioni"].values())) for giro in dati_simple[key]]) for key in dati_simple}
    com_astar = {int(key):np.mean([np.mean(list(giro["Comunicazioni"].values())) for giro in dati_astar[key]]) for key in dati_astar}
    
    plt.plot(*dict_yx(com_simple))
    plt.plot(*dict_yx(com_astar))
    plt.title("Media delle comunicazioni")
    plt.legend(["Step simple", "Step A*"])
    plt.savefig("runall_" + mappa + "_comun.svg")
    plt.close()
