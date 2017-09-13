"""Robosim Test.

Usage:
    test.py list 
    test.py show <test> [<seed>]
    test.py run <test> <iterations>
"""

tests =  {
    "primo" : {
        "seed" : 33456,
        "map" : "mappa_3.txt",
        "n_agents" : 3,
        "stubborness": 0.5
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
        import visualization
        import random
        import model
        import numpy as np
        mappa = model.load_map(t['map'])
        random.seed(t['seed'])
        np.random.seed(t['seed'])
        visualization.visualize(mappa, t['n_agents'], t['stubborness'], seed = t['seed'], test_name=", test " + arguments['<test>'])