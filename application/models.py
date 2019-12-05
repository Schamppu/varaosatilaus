from application import db

class Base(db.Model):

    __abstract__ = True
  
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

class Liitostaulu(db.Model):
    __tablename__ = 'liitostaulu'
    varaosa_id = db.Column(db.Integer, db.ForeignKey('varaosa.id'), primary_key = True)
    tilaus_id = db.Column(db.Integer, db.ForeignKey('tilaus.id'), primary_key = True)

