from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    dimension = db.Column(db.String(20), unique=False, nullable=False)
    alive = db.Column(db.Boolean(), unique=False, nullable=False)
    species = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "dimension" : self.dimension,
            "alive" : self.alive
        }

class Episodes (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    air_date = db.Column(db.String(20), unique=False, nullable=False)
    alive = db.Column(db.Boolean(), unique=False, nullable=False)
    species = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<Episodes %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "name": self.title
        }

class Fav_characters (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String(120), db.ForeignKey('user.email'))
    char_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    rel_user = db.relationship('User')
    rel_char = db.relationship('Characters')
        
    def __repr__(self):
        return '<Fav_Character %r>' % self.email

    def serialize(self):
        return {
            "email": self.email,
            "Char_ID": self.char_id
        }

class Fav_episodes (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String(120), db.ForeignKey('user.email'))
    title = db.Column(db.String(120), db.ForeignKey('episodes.title'))
    rel_user = db.relationship('User')
    rel_episodes = db.relationship('Episodes')
        
    def __repr__(self):
        return '<Fav_Episodes %r>' % self.email

    def serialize(self):
        return {
            "email": self.email,
            "Title": self.title
        }