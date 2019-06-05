# folders
IATI_FOLDER = .

# useful constants
LINE_SEP = ---

all: test lint


lint: $(IATI_FOLDER)
	-make flake8
	echo $(LINE_SEP)
	-make pydocstyle


flake8: $(IATI_FOLDER)
	flake8 $(IATI_FOLDER)


pydocstyle: $(IATI_FOLDER)
	pydocstyle $(IATI_FOLDER)


test: $(IATI_FOLDER)
	pytest $(IATI_FOLDER)
