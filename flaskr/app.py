import os

from dotenv import load_dotenv
load_dotenv() #take environment variables from .env

from flask import Flask, render_template, url_for

def create_app(test_config=None):
    #create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        #DATABASE = os.path.join(app.instance_path, 'flask.sqlite')
        DATABASE = 'postgres://kkvzpfulpiexaz:ae934bb5565d4c8953199de10153385b1a63fb2a6ce66b7b25c9928cea3fec31@ec2-54-152-28-9.compute-1.amazonaws.com:5432/d8qk2788k8333i',
    )
    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_mapping(test_config)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

