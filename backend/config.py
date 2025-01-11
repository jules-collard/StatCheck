import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE=os.path.join(basedir, 'statcheck.db')