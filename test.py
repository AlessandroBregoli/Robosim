"""Robosim Test.

Usage:
    test.py list 
    test.py show <test> [<step_name>]
    test.py run <test> [<step_name>]
    test.py export_map <test>
"""
import draw
import model

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

from docopt import docopt
import sys
if __name__ == '__main__':
    arguments = docopt(__doc__, version='Robosim Test')
    if arguments['list']:
        print(tests.keys())
        sys.exit()
    if arguments['show']:
        t = tests[arguments['<test>']]
        if arguments["<step_name>"]:
            t["step_name"] = arguments["<step_name>"]
        import visualization
        import random
        import numpy as np
        mappa = model.load_map(t['map'])
        random.seed(t['seed'])
        np.random.seed(t['seed'])
        visualization.visualize(mappa, t['n_agents'], t['stubborness'], seed = t['seed'], test_name=", test " + arguments['<test>'], step_name=t['step_name'])
    if arguments['run']:
        t = tests[arguments['<test>']]
        if arguments["<step_name>"]:
            t["step_name"] = arguments["<step_name>"]
        import visualization
        import random
        import model
        import numpy as np
        mappa = model.load_map(t['map'])
        random.seed(t['seed'])
        np.random.seed(t['seed'])
        modello = model.Robosim_model(3, mappa, 0.5)
        modello.running = True
        i = 0
        while modello.running:
            i += 1
            modello.step()
    if arguments['export_map']:
          t = tests[arguments['<test>']]
          mappa = model.load_map(t['map'])
          draw.draw_true_map(mappa, t['map'] + ".svg")
          