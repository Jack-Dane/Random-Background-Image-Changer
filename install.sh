#!/bin/bash

# install all the javascript packages
cd views
npm install
cd ..

# create the virtual environment
python3 -m venv venv || python -m venv venv
source venv/bin/activate

pip install wheel

# install the python requirements
pip install -r requirements.txt

createTables
