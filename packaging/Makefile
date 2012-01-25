
.PHONY: test clean
test:
	virtualenv --clear --no-site-package mypython;\
	source mypython/bin/activate;\
	pip install git+ssh://git@github.com/bgnori/tonic.git > log;\
	deactivate;

clean:
	rm -rf mypython
