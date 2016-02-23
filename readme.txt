Developed in python 2.7@lubuntu

Libraries used:
	pysoundfile
	numpy
	scipy

Install instructions for debian/ubuntu based distros:

1) pysoundfile

requires:
	pip (sudo apt-get install python-pip)
	libsndfile (sudo apt-get install libsndfile1)
	numpy (sudo apt-get install python-numpy)
	cffi (sudo apt-get install python-dev && sudo apt-get install python-cffi)

install with:
	pip install pysoundfile

2) numpy: should be installed as a requisite for pysoundfile in step 1.

3) scipy: sudo apt-get install python-scipy
