#!/bin/bash

# start the vue service
if [ $1 = "production" ];
then
  ( cd views ; npm run build 1>/dev/null 2>/dev/null & )
else
  ( cd views ; npm run dev 1>/dev/null 2>/dev/null & )
fi

# start the fileHandler service
source venv/bin/activate
startFileHandler --clientId $2 --clientSecret $3

# kill the foreground vue process when completed
trap 'fg %1' INT
