from flask import Blueprint

bp = Blueprint('auth', __name__)

from appm.auth import routes
