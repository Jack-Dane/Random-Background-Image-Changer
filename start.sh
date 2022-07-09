#!/bin/bash

export VITE_CLIENT_ID=$2
export VITE_CLIENT_SECRET=$3

# start the vue service
cd views
if [ $1 = "production" ];
then
  npm run build
  npm run preview &
else
  npm run dev &
fi
cd ..

# start the fileHandler service
source venv/bin/activate

if [ $1 = "production" ];
then
  gunicorn -w 4 "randomBackgroundChanger.scripts:startProductionServer('--clientId', '${2}', '--clientSecret', '${3}')" --bind 0.0.0.0:5000
else
  startFileHandler --clientId $2 --clientSecret $3
fi

# kill the foreground vue process when completed
trap 'fg %1' INT
