#!/bin/bash

# create the symbolic link for the background images
ln -sf $(pwd)/backgroundImages views/

# create the virtual environment
python3 -m venv venv || python -m venv venv
source venv/bin/activate

# install the python libraries
python setup.py install
