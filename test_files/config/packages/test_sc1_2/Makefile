%.pdf:
	latexmk -pdf $*.tex

%.docx:
	pandoc -o $*.docx $*.tex

PDFTARGETS=template.pdf

WORDTARGETS=template.docx

pdf: $(PDFTARGETS) junk

docx: $(WORDTARGETS)


clean:
	ls template.* | grep -vE "^template\.(bib|tex)$$" | xargs -r rm -rf

junk:
	rm -rf *.aux *.log

# if you wish to compile word targets as well, put "docx" into the "all" target below.

all: pdf junk


watch:
	latexmk -pdf -pvc
	
.PHONY: %.docx %.pdf pdf docx all clean junk watch
