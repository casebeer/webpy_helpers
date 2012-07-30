
all:

clean:
	rm -rf build/ dist/ webpy_helpers.egg-info/
	rm -f distribute-*.tar.gz 
	rm -rf *.egg
	find . -type f -name '*.pyc' | xargs rm -f
