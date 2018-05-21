from flask import Blueprint

bp = Blueprint('main', __name__)

from appm.main import routes