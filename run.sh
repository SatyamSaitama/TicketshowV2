#!/bin/bash


redis-server &
python app.py &
python image.py &
cd v2-frontend ;npm run serve &
