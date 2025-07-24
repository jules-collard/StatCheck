from flask import Blueprint

bp = Blueprint('api', __name__)

from app import db
from app.api import errors, players, teams