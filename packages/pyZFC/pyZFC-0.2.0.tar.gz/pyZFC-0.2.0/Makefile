build:
	python -m build --wheel --sdist --outdir dist/

build-dependencies:
	python -m pip install --upgrade pip
	python -m pip install "build>=0.8" --user

clean:
	rm -rf dist

install:
	python -m pip install --upgrade pip
	python -m pip install .

lint-dependencies:
	python -m pip install --upgrade pip
	python -m pip install .[lint]

lint:
	isort . --check-only --diff
	black . --check
	flake8 . --max-line-length 88 --extend-ignore E203 --statistics
	mypy src/zfc

unittest:
	coverage run --source zfc --parallel-mode -m unittest
	coverage combine
	coverage xml -i

unittest-dependencies:
	python -m pip install --upgrade pip
	python -m pip install .[unittest]
