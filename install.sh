#!/bin/bash

# install all the javascript packages
cd views
npm install
cd ..

# create the virtual environment
python3 -m venv venv || python -m venv venv
source venv/bin/activate

# install the python libraries
python3 setup.py install || python setup.py install
