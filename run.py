#!/usr/bin/env/python

from app import app
from app.routes.routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
