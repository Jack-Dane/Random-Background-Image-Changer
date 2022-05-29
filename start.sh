#!/bin/bash

# start the vue service
( cd views ; npm run dev 1>/dev/null 2>/dev/null & )

# start the fileHandler service
source venv/bin/activate
startFileHandler --clientId $1 --clientSecret $2
