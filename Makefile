SHELL=/bin/bash

env: requirements.txt
	virtualenv --python=python3 env
	source env/bin/activate; pip3 install --requirement=requirements.txt

test: env
	-pylint -E httpnext
	source env/bin/activate; ./test/test.py -v

release: docs
	python setup.py sdist upload -s -i D2069255

init_docs:
	cd docs; sphinx-quickstart

docs:
	$(MAKE) -C docs html

install:
	./setup.py install

.PHONY: test release docs
