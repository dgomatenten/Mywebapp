import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db1 = SQLAlchemy()

def create_app(test_config=None):

    """Create and configure an instance of the Flask application."""
    #app = Flask(__name__, instance_relative_config=True) creates the Flask instance
    # __name__ is the name of the current Python module. The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
    # instance_relative_config=True tells the app that configuration files are relative to the instance folder. 
    # The instance folder is located outside the application(mywebapp) package and can hold local data that shouldn’t be committed to version control, 
    # such as configuration secrets and the database file.

    app = Flask(__name__, instance_relative_config=True)

    #app.config.from_mapping() sets some default configuration that the app will use:
    #SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during development, 
    # but it should be overridden with a random value when deploying.
    #DATABASE is the path where the SQLite database file will be saved. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder. 
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "mywebapp.sqlite"),
        # Flight Price DB
        FLIGHTDB="C:/Users/dgoma/python/webcrawl/FLIGHT.sqlite",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "flascards.sqlite"),
        )

#app.config.from_pyfile() overrides the default configuration with values taken from the config.py file in the instance folder if it exists. 
# For example, when deploying, this can be used to set a real SECRET_KEY.
# test_config can also be passed to the factory, and will be used instead of the instance configuration. 
# This is so the tests you’ll write later in the tutorial can be configured independently of any development values you have configured.


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #@app.route() creates a simple route so you can see the application working before getting into the rest of the tutorial. 
    # It creates a connection between the URL /hello and a function that returns a response, the string 'Hello, World!' in this case.

    @app.route("/hello")
    def hello():
        return "Hello, World!"


    # register the database commands
    from Mywebapp import db

    db.init_app(app)
    db1.init_app(app)

    # apply the blueprints to the app
    from Mywebapp import auth, blog,flight,flashcards,eng

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(flight.bp)
    app.register_blueprint(flashcards.bp)
    app.register_blueprint(eng.bp)
    
    

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
