# folders
SPLIT 		= pdf-split
TXT_EXTRACT	= text-extract
TXT_AUTO 	= text-autofix
IMG_EXTRACT	= image-extract
IMG_AUTO	= image-autofix
TXTIMG_LINK	= text-imagelink
FOR_HUMANS	= for-humans
PATCH 		= patch
FIXED 		= fixed

.PHONY: all pages patches human report clean clean-pages clean-split


###### PRE-MAKE (calls make on this again after splitting pages)
SOURCE = Exec_Summary_2015_05_31_web_o.pdf
all: $(SPLIT)/*.pdf
	$(MAKE) report
clean-split:
	rm -fr $(SPLIT)
$(SPLIT)/*.pdf: $(SOURCE)
	-mkdir -p $(SPLIT)
	pdftk $(SOURCE) burst output $(SPLIT)/page-%03d.pdf


###### REAL MAKE (called once we have all source pages ready)
SOURCES := $(wildcard $(SPLIT)/*.pdf)
TARGETS := $(SOURCES:$(SPLIT)/%.pdf=$(FIXED)/%.md)
AUX_DEPS = refs.txt abbrevs.md

pages: $(TARGETS)

$(TXT_EXTRACT)/%.txt: $(SPLIT)/%.pdf mkdirs
	pdftotext -enc UTF-8 $< $@

$(TXT_AUTO)/%.md: $(TXT_EXTRACT)/%.txt mkdirs
	python lib/autofixtext.py $< $@

$(IMG_EXTRACT)/%-0000.jpg: $(SPLIT)/%.pdf mkdirs
	pdfimages -j $< $(@D)/$*

.SECONDARY:
$(IMG_AUTO)/%.jpg: $(IMG_EXTRACT)/%-0000.jpg mkdirs
	-convert -negate $< $@

$(TXTIMG_LINK)/%.md: $(IMG_AUTO)/%.jpg $(TXT_AUTO)/%.md
	python lib/autolinkimage.py $^ $@

$(FIXED)/%.md: $(TXTIMG_LINK)/%.md $(PATCH)/%.patch mkdirs
	python lib/patch.py $(PATCH)/$*.patch $< $@


###### THE BIG DOC
GOAL = TRC-2015-Executive-Summary.md
report: $(GOAL)
$(GOAL): $(TARGETS)
	python lib/join-fixed.py $@ $(sort $^)

###### FOR HUMANS (get an editable copy)
HUMAN := $(TARGETS:$(FIXED)/%.md=$(FOR_HUMANS)/%.md)
human: $(HUMAN)
$(FOR_HUMANS)/%.md: $(TXTIMG_LINK)/%.md mkdirs
	python lib/patch.py $(PATCH)/$*.patch $< $@


###### FOR ROBOTS (generate patches from human fixing)
PATCH_TARGETS := $(HUMAN:$(FOR_HUMANS)/%.md=$(PATCH)/%.patch)
patches: $(PATCH_TARGETS)
$(PATCH)/%.patch: $(FOR_HUMANS)/%.md $(TXTIMG_LINK)/%.md
	python lib/mkpatch.py $(TXTIMG_LINK)/$(<F) $< $@


###### HOUSEKEEPING
mkdirs:
	mkdir -p $(TXT_EXTRACT)
	mkdir -p $(TXT_AUTO)
	mkdir -p $(IMG_EXTRACT)
	mkdir -p $(IMG_AUTO)
	mkdir -p $(TXTIMG_LINK)
	mkdir -p $(FOR_HUMANS)
	mkdir -p $(PATCH)
	mkdir -p $(FIXED)
clean-pages:
	-rm -fr $(TXT_EXTRACT)
	-rm -fr $(TXT_AUTO)
	-rm -fr $(IMG_EXTRACT)
	-rm -fr $(IMG_AUTO)
	-rm -fr $(TXTIMG_LINK)
	-rm -fr $(FOR_HUMANS)
	-rm -fr $(FIXED)
clean: clean-split clean-pages
