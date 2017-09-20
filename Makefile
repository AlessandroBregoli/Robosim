
COSESIMPLE = test.py model.py agent.py
COSEASTAR = $(COSE) astar.py
TESTSIMPLE = python test.py runall 
TESTASTAR = python test.py runall --step=astar
MAPPESIMPLE = m1 m2 me
MAPPEASTAR = $(MAPPESIMPLE) m3 mm
TARGETSSIMPLE = $(addprefix runall_, $(addsuffix _simple.svg,  $(MAPPESIMPLE)))
TARGETSASTAR = $(addprefix runall_, $(addsuffix _astar.svg,  $(MAPPEASTAR)))

all: $(TARGETSSIMPLE) $(TARGETSASTAR)

$(TARGETSSIMPLE): runall_%_simple.svg: $(COSESIMPLE)
	$(TESTSIMPLE) $* 10 2

$(TARGETSASTAR): runall_%_astar.svg: $(COSEASTAR)
	$(TESTASTAR) $* 10 2