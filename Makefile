
PDF = Exec_Summary_2015_05_31_web_o.pdf
PDFPAGES = pdf-pages/
PAGES = pages/
PRE = page-
EXT = .pdf
PAGENAMES=$(PRE)*
PDFS = $(PAGENAMES)$(EXT)
TXT = $(PAGES)$(PAGENAMES)/page.txt
TXTAUTO = $(PAGES)$(PAGENAMES)/autofix.txt
IMG = $(PAGES)$(PAGENAMES)/image-0000.jpg
IMGAUTO = $(PAGES)$(PAGENAMES)/img-*.jpg

SPLITPAGES = $(PAGES)$(PAGENAMES)/page.pdf
EXTRACTEDS = $(PAGES)$(PAGENAMES)/page.txt
AUTOFIXES = $(PAGES)$(PAGENAMES)/autofix.txt
IMAGES = $(PAGES)$(PAGENAMES)/image-0000.jpg
AUTOIMAGES = $(PAGES)$(PAGENAMES)/img-*.jpg
FIXMES = $(PAGES)$(PAGENAMES)/FIXME.md


define eachPage
	find $(PAGES) -type d -name $(PAGENAMES) -exec $(1) \;
endef


# Exec commands for find
define LINK =
	sh -c '\
		p={} \
		d=$(PAGES)$${p:$$(expr length $(PDFPAGES)):-$$(expr length $(EXT))}; \
		mkdir -p $$d; \
		ln -s ../../{} $$d/page.pdf\
	'
endef


# Tasks

all: $(FIXMES)

$(PDFPAGES): $(PDF)
	mkdir $(PDFPAGES)
	pdftk $(PDF) burst output $(PDFPAGES)$(PRE)%03d$(EXT)

$(PDFPAGES)$(PDFS): $(PDFPAGES)
	find $(PDFPAGES) -type f -name $(PDFS) -exec $(LINK) \;
	touch $(SPLITPAGES)  # make sure we don't re-run this later

$(TXT): $(PDFPAGES)$(PDFS)
	$(call eachPage,pdftotext -enc UTF-8 {}/page.pdf {}/page.txt )

$(TXTAUTO): $(TXT)
	$(call eachPage,python autofixtext.py {}/page.txt {}/autofix.txt )

$(IMG): $(PDFPAGES)$(PDFS)
	$(call eachPage,pdfimages -j {}/page.pdf {}/image )
	rm -f $(PAGES)$(PAGENAMES)/image*.ppm
	find $(PAGES)$(PAGENAMES) -type f -name image-0000.jpg -exec\
		convert -negate {} {} \;  # fix broken pdfimages output

$(AUTOIMAGES): $(IMG) $(TXTAUTO)
	$(call eachPage,python autolinkimage.py {}/image-0000.jpg {}/autofix.txt {}/autolink.md )
	touch $(AUTOIMAGES)

$(FIXMES): $(AUTOIMAGES)
	$(call eachPage,cp {}/autolink.md {}/FIXME.md)

clean:
	rm -rf $(PDFPAGES)
	rm -rf $(SPLITPAGES)
	rm -rf $(EXTRACTEDS)
	rm -rf $(AUTOFIXES)
	rm -rf $(IMAGES)
	rm -rf $(AUTOIMAGES)
