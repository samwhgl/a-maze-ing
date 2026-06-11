####### MAKEFILE ########

PYTHON	= python3
PIP		= pip

MAIN	= a_maze_ing.py

MYPY_FLAG	= --warn-return-any \
			  --warn-unused-ignores \
			  --ignore-missing-imports \
			  --disallow-untyped-defs \
			  --check-untyped-defs

all: run

install:
	${PIP} install --upgrade ${PIP}
	${PIP} install flake8 mypy

run:
	${PYTHON} ${MAIN} config.txt

debug:
	${PYTHON} -m pdb ${MAIN} config.txt

lint:
	flake8 .
	mypy . ${FLAGS}

lint-strict:
	flake8 .
	mypy . --strict

clean:
	rm -rf __pycache__ .my_pycache ${VENV}
	find . -type f -name "*.txt" ! -name "config.txt" -delete

.PHONY: all install run debug lint lint-strict clean
