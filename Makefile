# folders
IATI_FOLDER = .

# useful constants
LINE_SEP = ---

all: test lint


lint: $(IATI_FOLDER)
	-make pylint
	echo $(LINE_SEP)
	-make flake8
	echo $(LINE_SEP)
	-make pydocstyle


pylint: $(IATI_FOLDER)
	pylint $(IATI_FOLDER)


flake8: $(IATI_FOLDER)
	flake8 $(IATI_FOLDER)


pydocstyle: $(IATI_FOLDER)
	pydocstyle $(IATI_FOLDER)


test: $(IATI_FOLDER)
	pytest --disable-warnings $(IATI_FOLDER)
