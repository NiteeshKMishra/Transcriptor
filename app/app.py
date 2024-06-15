import os
import sys
import logging
from flask import Flask, jsonify, redirect

from app.routes import routes

def init_app():
    app = Flask(
        __name__,
        template_folder=os.path.join('..', 'templates'),
        static_folder=os.path.join('..', 'static'),
        static_url_path=""
        )
    # disable default werkzeug http log
    log = logging.getLogger('werkzeug')
    log.disabled = True
    logger = logging.getLogger()

    @app.route('/health', methods=["GET"])
    def health_check():
        return jsonify({"message": "Application running with status 200"})

    app.register_blueprint(routes)

    @app.errorhandler(404)
    def not_found(e):
        logger.error("route not found", repr(e))
        return redirect('/')

    return app
