build:
	pylint pyx --disable=C --output-format=colorized --reports=n --score=n --jobs=0
	python3 -m zipapp pyx -o bin/pyx -p /usr/bin/python3 -c
