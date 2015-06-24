# folders
SPLIT 		= pdf-split
TXT_EXTRACT	= text-extract
TXT_AUTO 	= text-autoclean
IMG_EXTRACT	= image-extract
IMG_AUTO	= image-fix
TXTIMG_LINK	= text-imagelink
IMG_RENAME	= image-rename
PATCH 		= patch
FIXED 		= text-fixed

.PHONY: all pages clean

###### PRE-MAKE (calls make on this again after splitting pages)
SOURCE = Exec_Summary_2015_05_31_web_o.pdf
all: $(SPLIT)/*.pdf
	$(MAKE) pages
$(SPLIT)/*.pdf: $(SOURCE)
	-mkdir -p $(SPLIT)
	pdftk $(SOURCE) burst output $(SPLIT)/page-%03d.pdf

###### REAL MAKE (called once we have all source pages ready)
SOURCES := $(wildcard $(SPLIT)/*.pdf)
TARGETS := $(SOURCES:$(SPLIT)/%.pdf=$(FIXED)/%.md)

pages: $(TARGETS)

$(TXT_EXTRACT)/%.txt: $(SPLIT)/%.pdf
	-mkdir -p $(TXT_EXTRACT)
	pdftotext -enc UTF-8 $< $@

$(FIXED)/%.md: $(TXT_EXTRACT)/%.txt
	-mkdir -p $(FIXED)
	cp $< $@

clean:
	-rm -fr $(SPLIT)
	-rm -fr $(TXT_EXTRACT)
	-rm -fr $(TXT_AUTO)
	-rm -fr $(IMG_EXTRACT)
	-rm -fr $(IMG_AUTO)
	-rm -fr $(TXTIMG_LINK)
	-rm -fr $(IMG_RENAME)
	-rm -fr $(FIXED)
