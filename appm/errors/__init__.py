from flask import Blueprint

bp = Blueprint('errors', __name__)

from appm.errors import handlers