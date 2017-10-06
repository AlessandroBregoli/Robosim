
COSESIMPLE = test.py model.py agent.py
COSEASTAR = $(COSESIMPLE) astar.py
TESTSIMPLE = unbuffer python3 test.py runall 
TESTASTAR = unbuffer python3 test.py runall --step=astar
MAPPESIMPLE = m1 m2 me
MAPPEASTAR = $(MAPPESIMPLE) m3 mc
TARGETSSIMPLE = $(addprefix runall_, $(addsuffix _simple.json,  $(MAPPEASTAR)))
TARGETSASTAR = $(addprefix runall_, $(addsuffix _astar.json,  $(MAPPEASTAR)))
GRAFICI1 = $(addprefix runall_, $(addsuffix _tempi.pdf,  $(MAPPEASTAR)))
#GRAFICI2 = $(addprefix runall_, $(addsuffix _espl.pdf,  $(MAPPEASTAR)))
#GRAFICI3 = $(addprefix runall_, $(addsuffix _comun.pdf,  $(MAPPEASTAR)))

all: $(TARGETSSIMPLE) $(TARGETSASTAR) $(GRAFICI1)

$(TARGETSSIMPLE): runall_%_simple.json: $(COSEASTAR)
	$(TESTSIMPLE) $* 10 5 --stubb=0.3 > log/output_$*_simple.log

$(TARGETSASTAR): runall_%_astar.json: $(COSEASTAR)
	$(TESTASTAR) $* 10 5 > log/output_$*_astar.log

.SECONDEXPANSION:
$(GRAFICI1): runall_%_tempi.pdf: $$(wildcard runall_%_simple.json runall_%_astar.json)
	python3 grafichino.py gf $*
	inkscape --export-pdf=runall_$*_tempi_simple.pdf runall_$*_tempi_simple.svg 
	inkscape --export-pdf=runall_$*_tempi_astar.pdf runall_$*_tempi_astar.svg 
	inkscape --export-pdf=runall_$*_espl.pdf runall_$*_espl.svg 
	inkscape --export-pdf=runall_$*_comun.pdf runall_$*_comun.svg 
	inkscape --export-pdf=runall_$*_std_tempi.pdf runall_$*_std_tempi.svg 
