from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import recipes
from flask_app.models import user

if __name__=="__main__":
    app.run(debug=True, port=5001)