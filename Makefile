# folders
IATI_FOLDER = iati/
TEST_FOLDER = $(IATI_FOLDER)tests/

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


test: $(TEST_FOLDER)
	pytest $(TEST_FOLDER)about_functional_tests.py
	pytest $(TEST_FOLDER)events_functional_tests.py
	pytest $(TEST_FOLDER)guidance_unit_tests.py
	pytest $(TEST_FOLDER)home_functional_tests.py
	pytest $(TEST_FOLDER)iati_standard_functional_tests.py
	pytest $(TEST_FOLDER)management_unit_tests.py
	pytest $(TEST_FOLDER)news_functional_tests.py
	pytest $(TEST_FOLDER)redirects_unit_tests.py
	pytest $(TEST_FOLDER)using_data_functional_tests.py
