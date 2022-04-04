#!/usr/bin/env/python
import os
from app import app
from app.routes.routes import *

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host="0.0.0.0", port=port)
