rm dist/*
python -m build
python -m twine upload --repository testpypi dist/*
python -m venv ./test_virtualenv