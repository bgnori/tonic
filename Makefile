#
#	virtualenv --no-site-package --clear mypython
#	source mypython/bin/activate
#

.PHONY: evn test clean

env:
	pip install -r freeze.txt

clean:
	rm setup.py

test:
	python mypython/bin/nosetests

setup.py: freeze.txt
	python make_setup.py > setup.py

freeze.txt:
	pip freeze > freeze.txt
