.PHONY: all
all: valist.txt perf.csv animation.gif
# all: pageid.dat pages/*.txt valist.txt perf.csv animation.gif

#pageid.dat: dlid.py
#	./dlid.py

#pages/*.txt: dlarticle.py pageid.dat
#	./dlarticle.py

valist.txt: selectva.py pages/*.txt
	./selectva.py

perf.csv: valist.txt
	./parsearticle.py

animation.gif: kaiseki.r perf.csv
	Rscript kaiseki.r

.PHONY: clean
clean:
	-rm -f valist.txt *.gif perf.csv *~

# .PHONY: delete
# delete:
# 	-rm -f pageid.dat valist.txt perf.csv *~
# 	-rm -rf pages/

.PHONY: donwload
download: pageid.dat
	rm -rf pages/
	./dlid.py
	./dlarticle.py
