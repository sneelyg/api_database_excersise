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
from models import db, User, Characters, Episodes, Fav_characters, Fav_episodes 
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

@app.route('/user', methods=['GET'])
def get_user():
    usuarios = User.query.all()
    response_body = list(map (lambda user : user.serialize(), usuarios))
    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    all_characters = list(map (lambda char : char.serialize(), all_characters))
    return jsonify(all_characters)



@app.route('/characters/<int:char_id>', methods=['GET'])
def get_one_character(char_id):
    one_character = Characters.query.get(char_id)
    return jsonify(one_character.serialize())


@app.route('/episodes', methods=['GET'])
def get_episodes():
    all_episodes = Episodes.query.all()
    all_episodes = list(map (lambda episode : episode.serialize(),  all_episodes))
    return jsonify( all_episodes)


@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_one_episode(episode_id):
    one_episode = Episodes.query.get(episode_id)
    return jsonify(one_episode.serialize())

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    usuario = User.query.get(1) #luego sacarle el mail, porque el favorito está con el mail.
    mail_usuario = usuario.email
    fav_episodes = Fav_episodes.query.filter_by(email = mail_usuario)
    fav_characters = Fav_characters.query.filter_by(email = mail_usuario) #Esto me entrega los registros de la tabla
    id_fav_char = list(map (lambda favo : favo.char_id,  fav_characters)) #Aca saco cada char_ID de cada registro
    #Ahora, de cada uno de esos numeros, voy a buscarlo en la tabal de Characters.
    toda_la_info_de_chars = []
    for ids in id_fav_char:
        aux = Characters.query.get(ids)
        toda_la_info_de_chars.append(aux)

    favoritos_todos = [*toda_la_info_de_chars ,  *fav_episodes] #Eso une ambos arreglos de favoritos
    favoritos_todos = list(map (lambda favo : favo.serialize(),  favoritos_todos))
    return jsonify(favoritos_todos)





###
"""De acá hacia abajo son los métodos POST y DELETE.
HAcia ARRIBA son todos GET
"""
@app.route('/favorites/character/<int:char_id>', methods=['POST'])
def post_fav_character(char_id):
    one = Characters.query.get(char_id)
    if (one):
        new_fav = Fav_characters()
        new_fav.email = User.query.get(1).email
        new_fav.char_id = char_id

        db.session.add (new_fav)
        db.session.commit()
        return "Agregado!" 
    else:
        raise APIException("Personaje no existe", status_code=404 )



@app.route('/favorite/episode/<int:episode_id>', methods=['POST'])
def post_fav_episode(episode_id):
    return "Add a episode 'Episode_id' to user's favorites" 

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
