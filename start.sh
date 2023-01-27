#!/bin/bash

export VITE_CLIENT_ID=$1
export VITE_CLIENT_SECRET=$2

# start the vue service
cd views
npm run build
npm run preview &

cd ..
# start the fileHandler service
source venv/bin/activate
startFileHandler --clientId $1 --clientSecret $2

# kill the foreground vue process when completed
trap 'fg %1' INT
