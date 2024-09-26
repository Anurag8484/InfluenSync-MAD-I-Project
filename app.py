from flask import Flask
from backend.models import *
from flask_login import *
app = None

def init_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'
    
    
    app.debug = True
    app.app_context().push()
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///InfluenSync.sqlite3"
    db.init_app(app)
    
    return app

app = init_app()
# db.create_all()
from backend.routes import *

if __name__ == "__main__":
     app.run()