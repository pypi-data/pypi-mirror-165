python setup.py sdist --formats=gztar,zip
python -m build
python -m twine upload dist/*