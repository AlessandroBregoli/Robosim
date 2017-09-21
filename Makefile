
COSESIMPLE = test.py model.py agent.py
COSEASTAR = $(COSE) astar.py
TESTSIMPLE = unbuffer python3 test.py runall 
TESTASTAR = unbuffer python3 test.py runall --step=astar
MAPPESIMPLE = m1 m2 me
MAPPEASTAR = $(MAPPESIMPLE) m3 mc
TARGETSSIMPLE = $(addprefix runall_, $(addsuffix _simple.svg,  $(MAPPEASTAR)))
TARGETSASTAR = $(addprefix runall_, $(addsuffix _astar.svg,  $(MAPPEASTAR)))

all: $(TARGETSSIMPLE) $(TARGETSASTAR)

$(TARGETSSIMPLE): runall_%_simple.svg: $(COSEASTAR)
	$(TESTSIMPLE) $* 10 5 --stubb=0.02 > log/output_$*_simple.log

$(TARGETSASTAR): runall_%_astar.svg: $(COSEASTAR)
	$(TESTASTAR) $* 10 5 > log/output_$*_astar.log
