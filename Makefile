CONTEXT=algorithmics
PROJECT=segmentation
VERSION=1
AUTHOR=dmitrimelnikov
DIST=$(PROJECT)
FINAL=$(DIST).pdf
TITLE=title

all: 
	mkdir -p out
	cp latex/* out/ -r
	cd out; pdflatex $(TITLE).tex && cp $(TITLE).pdf ../$(FINAL)
init: 
	mkdir -p latex

tarball: all
	mkdir -p $(DIST) 
	cp -r Makefile latex $(FINAL) $(DIST) 
	tar -czf $(CONTEXT)-$(DIST).tar.gz $(DIST)
	rm -fr $(DIST)

zip: all
	mkdir -p $(DIST) 
	cp -r Makefile latex $(FINAL) $(DIST) 
	zip -r $(CONTEXT)-$(DIST).zip $(DIST)
	rm -fr $(DIST)

clean:
	rm -fr out
	rm $(FINAL)
