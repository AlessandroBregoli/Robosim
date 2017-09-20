"""Robosim Test.

Usage:
    test.py list 
    test.py show <test> [--step=<step_name>] [<seed>]
    test.py run <test> [<step_name>]
    test.py runall <test> <max_n> <giri> [--step=<step_name>] [--stubb=<stubborness>]
    test.py export_map <test>
"""
import draw
import model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import visualization
import random
import model
import numpy as np
from docopt import docopt
import sys

tests =  {
    "me" : {
        "seed" : 33456,
        "map" : "mappa_empty.txt",
        "n_agents" : 3,
        "stubborness": 0.5,
        "step_name": "simple"
    },
    "m1" : {
        "seed" : 33456,
        "map" : "mappa_1.txt",
        "n_agents" : 3,
        "stubborness": 0.5,
        "step_name": "simple"
    },
    "m2" : {
        "seed" : 33456,
        "map" : "mappa_2.txt",
        "n_agents" : 3,
        "stubborness": 0.5,
        "step_name": "simple"
    },
    "m3" : {
        "seed" : 33456,
        "map" : "mappa_3.txt",
        "n_agents" : 3,
        "stubborness": 0.5,
        "step_name": "simple"
    },
    "mc" : {
        "seed" : 33456,
        "map" : "mappa_corridoio.txt",
        "n_agents" : 3,
        "stubborness": 0.5,
        "step_name": "simple"
    },
    "mm" : {
        "seed" : 33456,
        "map" : "mappa_maze.txt",
        "n_agents" : 3,
        "stubborness": 0.5,
        "step_name": "simple"
    }
}


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Robosim Test')
    t = tests[arguments['<test>']]
    if arguments["--step"]:
        t["step_name"] = arguments["--step"]
    if arguments["--stubb"]:
        t["stubborness"] = float(arguments["--stubb"])
    if arguments["<seed>"]:
        t["seed"] = arguments["<seed>"]
        if arguments["<seed>"] == "no":
            t["seed"] = None
    if arguments['list']:
        print(tests.keys())
        sys.exit()
    if arguments['show']:
        mappa = model.load_map(t['map'])
        random.seed(t['seed'])
        #np.random.seed(t['seed'])
        visualization.visualize(mappa, t['n_agents'], t['stubborness'], seed = t['seed'], test_name=", test " + arguments['<test>'], step_name=t['step_name'])
    if arguments['run']:
        mappa = model.load_map(t['map'])
        random.seed(t['seed'])
        np.random.seed(t['seed'])
        modello = model.Robosim_model(3, mappa, t['stubborness'], seed=t["seed"], step_name=t["step_name"])
        modello.running = True
        i = 0
        while modello.running:
            i += 1
            modello.step()
        plt.plot(modello.datacollector.model_vars["Esplorate"])
        plt.title("Celle Esplorate")
        plt.savefig("Esplorate_" + arguments["<test>"] + "_" + t["step_name"] + ".svg")
        plt.close()
        plt.plot(modello.datacollector.model_vars["Comunicazioni"])
        plt.title("Comunicazioni")
        plt.savefig("Comunicazioni_" + arguments["<test>"] + t["step_name"]+ ".svg")
        plt.close()
        plt.plot(modello.datacollector.model_vars["Mosse utili"])
        plt.title("Mosse utili")
        plt.legend([x for x in range(10)], ncol=2)
        plt.savefig("Mosse_utili_" + arguments["<test>"] + t["step_name"] + ".svg")
        plt.close()
    if arguments['runall']:
        mappa = model.load_map(t['map'])
        tempi = {}
        tempipern = {}
        for n in range(1,int(arguments['<max_n>'])+1):
            n_step = 0
            print("n = " + str(n))
            for giro in range(int(arguments['<giri>'])):
                print("\tgiro = " + str(giro))
                modello = model.Robosim_model(n, mappa, 0.5, seed=None, step_name=t["step_name"])
                modello.running = True
                i = 0
                while modello.running:
                    i += 1
                    modello.step()
                n_step += i
            tempi[n] = n_step/int(arguments['<giri>'])
            tempipern[n] = tempi[n] * (n**0.5)
        plt.plot(list(tempi.keys()), list(tempi.values()))
        plt.plot(list(tempipern.keys()), list(tempipern.values()))
        plt.legend(["tempi", "tempi * sqrt(n)"])
        plt.title("Tempi al variare di n")
        plt.savefig("runall_" + arguments["<test>"] + "_" + t["step_name"] + ".svg")
        plt.close()

    if arguments['export_map']:
        mappa = model.load_map(t['map'])
        draw.draw_true_map(mappa, t['map'] + ".svg")
          