#!/bin/bash 

python -V
. ./venv/bin/activate
python -V

# pip3 install flask
# pip3 install neo4j

export FLASK_APP=be
export FLASK_ENV=development
flask run  --host 0.0.0.0 --port 4666


