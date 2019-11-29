from application import db
from application.models import Base

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Tilaus(db.Model):

    __tablename__ = 'tilaukset'
    id = db.Column(db.Integer, primary_key=True)

class TilausVaraosa(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'tilausvaraosa'
    orderCode = db.Column(db.String(144), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    tilaus_id = db.Column(db.Integer, db.ForeignKey('tilaukset.id'))

    def __init__(self, orderCode):
        self.orderCode = orderCode

    # Relationship
    tilaus = db.relationship(
        'Tilaus',
        backref=db.backref('tilausvaraosa', lazy='dynamic', collection_class=list)
    )