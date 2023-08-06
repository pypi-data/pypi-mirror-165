from flask import Blueprint

blueprint = Blueprint(
    'seetm_blueprint',
    __name__,
    url_prefix='/api/seetm',
    static_folder='static',
    template_folder='templates',
)
