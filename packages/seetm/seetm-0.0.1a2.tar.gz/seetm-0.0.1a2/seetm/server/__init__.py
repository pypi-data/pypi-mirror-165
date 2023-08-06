import logging
import os.path
from importlib import import_module
from typing import Dict

import pkg_resources
from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
)
from flask_cors import (
    CORS,
    cross_origin,
)

from seetm.shared.constants import PACKAGE_VERSION
from seetm.utils.io import (
    dir_exists,
)

logger = logging.getLogger(__name__)


def register_blueprints(app):
    src_path = pkg_resources.resource_filename(__name__, "")
    dir_list = [dir_ for dir_ in pkg_resources.resource_listdir(__name__, "")
                if dir_exists(os.path.join(src_path, dir_))]
    pkg_list = [dir_ for dir_ in dir_list
                if dir_ not in [
                    'static',
                    'templates',
                    'frontend',
                    'react_frontend',
                    '__pycache__',
                    'utils'
                ]]

    for module_name in set(pkg_list):
        module = import_module(f'seetm.server.{module_name}.routes')
        app.register_blueprint(module.blueprint)


def create_app(configs: Dict = None):
    app = Flask(__name__, static_folder='frontend', template_folder='frontend')
    register_blueprints(app=app)

    if configs:
        for config_key, config_value in configs.items():
            app.config[config_key] = config_value

    # allowing all cross-origins
    CORS(app)

    @app.route("/", strict_slashes=False, methods=['GET'])
    @cross_origin()
    def root():
        logger.debug("Dashboard is served")
        return render_template("index.html"), 200

    @app.route("/status", strict_slashes=False, methods=['GET'])
    @cross_origin()
    def server_status():
        logger.info("Status route was called")
        return {
            "server": "seetm_server",
            "status": "ok",
            "version": PACKAGE_VERSION,
        }

    # redirecting to react routes
    # {none}

    # utilize since static files are being
    # served from the root of the server
    @app.route("/<path:path>", strict_slashes=False, methods=['GET'])
    @cross_origin()
    def static_files(path):
        logger.debug("Static files are being served...")
        return send_from_directory(directory=app.static_folder, path=path), 200

    @app.errorhandler(Exception)
    @cross_origin()
    def handle_exception(e):
        logger.error(f"Exception occurred while serving the pages. {e}")
        return redirect('/#/error')

    return app
