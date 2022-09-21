"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    return "All the Characters"



@app.route('/characters/<int:char_id>', methods=['GET'])
def get_one_character(char_id):
    return "One of the  Characters"


@app.route('/episodes', methods=['GET'])
def get_episodes():
    return "All the Episodes"


@app.route('/pisodes/<int:episode_id>', methods=['GET'])
def get_one_episode(episode_id):
    return "One of the  Episodes"

@app.route('/users/favorites', methods=['GET'])
def et_user_favorites():
    return "All the current user favorites"

@app.route('/favorite/character/<int:char_id>', methods=['POST'])
def post_fav_character(char_id):
    return "Add character 'char ID' to user's favorites" 

@app.route('/favorite/episode/<int:episode_id>', methods=['POST'])
def post_fav_episode(episode_id):
    return "Add a episode 'Episode_id' to user's favorites" 

______
@app.route('/favorite/character/<int:char_id>', methods=['DELETE'])
def delete_fav_character(char_id):
    return "REMOVE character 'char ID' from user's favorites" 

@app.route('/favorite/episode/<int:episode_id>', methods=['DELETE'])
def delete_fav_episode(episode_id):
    return "REMOVE  episode 'Episode_id' from user's favorites" 




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
