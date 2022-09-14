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
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "dimension" : self.dimension,
            "alive" : self.alive
        }

class Episodes (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    air_date = db.Column(db.String(20), unique=False, nullable=False)
    alive = db.Column(db.Boolean(), unique=False, nullable=False)
    species = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "name": self.title
        }