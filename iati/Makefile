# folders
# IATI_FOLDER = iati/
# TEST_FOLDER = $(IATI_FOLDER)tests/

# useful constants
LINE_SEP = ---

all: test lint


lint: $(CURDIR)
	-make pylint
	echo $(LINE_SEP)
	-make flake8
	echo $(LINE_SEP)
	-make pydocstyle


pylint: $(CURDIR)
	pylint $(CURDIR)


flake8: $(CURDIR)
	flake8 $(CURDIR)


pydocstyle: $(CURDIR)
	pydocstyle $(CURDIR)


test: $(CURDIR)
	pytest $(CURDIR)
