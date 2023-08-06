export PROJECT := tuxtrigger
export TUXTRIGGER_MIN_COVERAGE := 80

style:
	black --check --diff .
flake8:
	flake8 .

htmlcov:
	python3 -m pytest --cov=tuxtrigger --cov-report=html

stylecheck: style flake8 

typecheck:
	mypy .

spellcheck:
	codespell \
		--check-filenames \
		--skip '.git,public,dist,*.sw*,*.pyc,tags,*.json,.coverage,htmlcov,*.jinja2'

doc: docs/index.md
	mkdocs build

docs/index.md: README.md scripts/readme2index.sh
	scripts/readme2index.sh $@

doc-serve:
	mkdocs serve

