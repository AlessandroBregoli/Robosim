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
    
   
    y,x = dict_yx(step_simple)

    A = np.vstack([[x[0]/y[x1] - x[0] for x1 in range(len(x))]]).T
    p= np.linalg.lstsq(A,[x[y1]-x[0] for y1 in range(len(y))])[0]
    plt.plot(y,[(1-p)*x[0]+p*x[0]/yi for yi in y])
    plt.legend(["Step simple", "Legge di Amdhal"])
    plt.title("Tempi al variare di n")
    plt.xticks(y)
    plt.savefig("runall_" + mappa + "_tempi_simple.svg")
    plt.close()
    plt.plot(*dict_yx(step_astar))
    y,x = dict_yx(step_astar)
    
    A = np.vstack([[x[0]/y[x1] - x[0] for x1 in range(len(x))]]).T
    p= np.linalg.lstsq(A,[x[y1]-x[0] for y1 in range(len(y))])[0]
    plt.plot(y,[(1-p)*x[0]+p*x[0]/yi for yi in y])
    
    plt.legend(["Step A*", "Legge di Amdhal"])
    plt.title("Tempi al variare di n")
    plt.xticks(y)
    plt.savefig("runall_" + mappa + "_tempi_astar.svg")
    plt.close()
    

    step_std_simple = {int(key):np.std([len(giro["Comunicazioni"]) for giro in dati_simple[key]]) for key in dati_simple}
    step_std_astar = {int(key):np.std([len(giro["Comunicazioni"]) for giro in dati_astar[key]]) for key in dati_astar}
    plt.plot(*dict_yx(step_std_simple))
    plt.plot(*dict_yx(step_std_astar))
    plt.legend(["Step simple", "Step A*"])
    plt.title("Deviazione standard dei tempi al variare di n")
    plt.xticks(y)
    plt.savefig("runall_" + mappa + "_std_tempi.svg")
    plt.close()

    espl_simple = {int(key):np.mean([np.mean(list(giro["Mosse utili"].values())) for giro in dati_simple[key]]) for key in dati_simple}
    espl_astar = {int(key):np.mean([np.mean(list(giro["Mosse utili"].values())) for giro in dati_astar[key]]) for key in dati_astar}
    plt.plot(*dict_yx(espl_simple))
    plt.plot(*dict_yx(espl_astar))
    plt.title("Media di celle esplorate per robot")
    plt.legend(["Step simple", "Step A*"])
    plt.xticks(y)
    plt.savefig("runall_" + mappa + "_espl.svg")
    plt.close()
    
    com_simple = {int(key):np.mean([np.mean(list(giro["Comunicazioni"].values())) for giro in dati_simple[key]]) for key in dati_simple}
    com_astar = {int(key):np.mean([np.mean(list(giro["Comunicazioni"].values())) for giro in dati_astar[key]]) for key in dati_astar}
    
    plt.plot(*dict_yx(com_simple))
    plt.plot(*dict_yx(com_astar))
    plt.title("Media delle comunicazioni")
    plt.legend(["Step simple", "Step A*"])
    plt.xticks(y)
    plt.savefig("runall_" + mappa + "_comun.svg")
    plt.close()
