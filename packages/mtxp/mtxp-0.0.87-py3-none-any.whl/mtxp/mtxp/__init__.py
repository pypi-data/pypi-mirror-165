from flask import Blueprint
mtxp_blue = Blueprint('mtxp', __name__, url_prefix='/mtxp')
from . import views