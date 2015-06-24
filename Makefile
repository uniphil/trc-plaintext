ORIGINAL = Exec_Summary_2015_05_31_web_o.pdf

SPLIT 		= pdf-split
TXT_EXTRACT	= text-extract
TXT_AUTO 	= text-autoclean
IMG_EXTRACT	= image-extract
IMG_AUTO	= image-fix
TXTIMG_LINK	= text-imagelink
IMG_RENAME	= image-rename
PATCH 		= patch
FIXED 		= text-fixed

PRE = page-

$(SPLIT)/$(PRE)*.pdf: $(ORIGINAL)
	mkdir -p $(SPLIT)
	pdftk $(ORIGINAL) burst output $(SPLIT)/$(PRE)%03d.pdf
