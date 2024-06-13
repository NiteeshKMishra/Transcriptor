import os
import sys
import logging
from flask import Flask, jsonify

from app.routes import routes

def init_app():
    app = Flask(
        __name__,
        template_folder=os.path.join('..', 'templates'),
        static_folder=os.path.join('..', 'static'),
        )
    # disable default werkzeug http log
    log = logging.getLogger('werkzeug')
    log.disabled = True
    logging.basicConfig(
        format='%(json_formatted)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    @app.route('/health', methods=["GET"])
    def health_check():
        return jsonify({"message": "Application running with status 200"})

    app.register_blueprint(routes)

    return app
