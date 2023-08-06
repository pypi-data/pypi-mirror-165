# # # # # # # # # # # # # # # # # # # #
# Pape (a Python package)
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

both:
	@echo "Verify that this version number is current: "
	@python setup.py --version
	@read
	$(MAKE) bdist_wheel
	$(MAKE) sdist
	@echo "\nTo upload to PyPI, do:"
	@echo "make distribute"

bdist_wheel:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

distribute:
	python -m twine upload dist/*

debug_install:
	pip install -e .
