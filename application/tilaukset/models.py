from application import db
from application.models import Base
from application.models import Liitostaulu



class Tilaus(Base):
        
    orderPlace = db.Column(db.String(144), nullable=False)
    orderStatus = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    orderStatusNames = {}
    orderStatusNames['draft'] = 'Luonnos'
    orderStatusNames['in-progress'] = 'Käsittelyssä varastossa'
    orderStatusNames['waiting'] = 'Odottaa varaosaa/toimenpiteitä'
    orderStatusNames['cancelled'] = 'Toimitushäiriö'
    orderStatusNames['sent'] = 'Lähetetty'

    orderPlaceNames = {}
    orderPlaceNames['hes-helsinki'] = 'HES Helsinki'
    orderPlaceNames['hcsc-tampere'] = 'HCSC Tampere'
    orderPlaceNames['dna-sello'] = 'DNA Sello'
    orderPlaceNames['dna-hameenkatu'] = 'DNA Hämeenkatu'

    varaosat = db.relationship('Varaosa', secondary = 'liitostaulu')

    
    def __init__(self, orderPlace, orderStatus):
        self.orderPlace = orderPlace
        self.orderStatus = orderStatus



'''
class TilausVaraosa(Base):
        
    orderPart = db.Column(db.String(144), nullable=False)
    # Relaatio Tilaukseen

    parent_id = db.Column(db.Integer, db.ForeignKey('tilaus.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, orderPart):
        self.orderPart = orderPart
'''