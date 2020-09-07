from flask import Flask, jsonify
import os

def create_app(test_config=None):
    # create and configure
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, it if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

# a simple page that says hello
    @app.route('/')
    def hello():
        return jsonify({'message': 'HELLO WORLD'})

    @app.route('/smiley')
    def smiley():
        return ':)'

    return app