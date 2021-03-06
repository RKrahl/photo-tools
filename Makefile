PYTHON   = python3
BUILDLIB = $(CURDIR)/build/lib


build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -f *~ photo/*~ photo/qt/*~ tests/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST .version
	rm -f photo-tools/__init__.py
	rm -rf .cache
	rm -rf photo/__pycache__ photo/qt/__pycache__ tests/__pycache__
	rm -rf dist

init_py:
	$(PYTHON) setup.py init_py


.PHONY: build test sdist clean distclean init_py
