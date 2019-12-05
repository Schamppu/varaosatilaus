from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    role = db.Column(db.String(144), nullable=False)

    varaosa = db.relationship("Varaosa", backref='account', lazy=True)
  
    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def get_id(self):
        return self.id
  
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def has_role(self, role):
        return self.role

    def roles(self):
        return [self.role]



    @staticmethod
    def find_new_orders():
        stmt = text("SELECT Tilaus.id, Tilaus.date_created, Account.name FROM Tilaus"
                    " LEFT JOIN Account ON Account.id = Tilaus.account_id"
                    " ORDER BY Tilaus.date_created DESC"
                    " LIMIT 5")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"tilaus":row[0], "aika":row[1], "tunnus":row[2]})

        return response


    @staticmethod
    def find_users_with_most_orders():
        stmt = text("SELECT Account.name, COUNT(Tilaus.id) FROM Account"
                    " LEFT JOIN Tilaus ON Tilaus.account_id = Account.id"
                    " GROUP BY Account.id"
                    " ORDER BY COUNT(Tilaus.id) DESC")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"tunnus":row[0], "lkm":row[1]})

        return response
        