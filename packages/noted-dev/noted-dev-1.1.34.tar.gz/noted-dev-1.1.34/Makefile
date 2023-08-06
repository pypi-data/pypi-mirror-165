# © Copyright 2022 CERN. This software is distributed under the terms of
# the GNU General Public Licence version 3 (GPL Version 3), copied verbatim
# in the file "LICENCE.txt". In applying this licence, CERN does not waive
# the privileges and immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.

# Create virtual environment:
# python3 -m venv venv-noted
# . venv-noted/bin/activate
# ./venv-noted/bin/python3 -m pip install --upgrade pip

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install wheel
	python3 -m pip install build

clean:
	sudo rm -rf build/
	sudo rm -rf dist/

run:
	sudo python3 setup.py bdist_wheel
	sudo python3 setup.py install

build_linux:
	sudo python3 setup.py sdist

build_centos:
	sudo python3 setup.py bdist_rpm

check:
	python3 -m twine check dist/*

upload_testpypi:
	python3 -m twine upload --repository testpypi dist/*

upload_pypi:
	python3 -m twine upload dist/*
