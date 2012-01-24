#
#	virtualenv --no-site-package --clear mypython
#	source mypython/bin/activate
#

.PHONY: evn test

env:
	pip install -r freeze.txt

test:
	python mypython/bin/nosetests
