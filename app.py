from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models
import config

from resources.users import users_api
from resources.posts import posts_api

login_manager = LoginManager()
## sets up our login for the app



app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager.init_app(app)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(posts_api, url_prefix='/api/v1')

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)