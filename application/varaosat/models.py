from application import db
from application.models import Base
from application.models import Liitostaulu


class Varaosa(Base):

    partCode = db.Column(db.String(144), nullable=False)
    partType = db.Column(db.String(144), nullable=False)
    partBrand = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    tilaukset = db.relationship('Tilaus', secondary = 'liitostaulu')

    partTypeNames = {}
    partTypeNames['display'] = 'Näyttö'
    partTypeNames['mainboard'] = 'Piirikortti'
    partTypeNames['subboard'] = 'Alapiirilevy'
    partTypeNames['battery'] = 'Akku'
    partTypeNames['speaker'] = 'Kaiutin'
    partTypeNames['receiver'] = 'Kuuloke'
    partTypeNames['handset'] = 'Myyntipakkaus'
    partTypeNames['host'] = 'Vaihtolaite'
    partTypeNames['cable'] = 'Kaapeli'
    partTypeNames['charger'] = 'Laturi'
    partTypeNames['usbcable'] = 'Latausjohto'
    partTypeNames['other'] = 'Muu'

    partBrandNames = {}
    partBrandNames['huawei'] = 'Huawei'
    partBrandNames['samsung'] = 'Samsung'
    partBrandNames['oneplus'] = 'OnePlus'
    partBrandNames['apple'] = 'Apple'
    partBrandNames['nokia'] = 'Nokia'
    partBrandNames['sony'] = 'Sony'
    partBrandNames['xiaomi'] = 'Xiaomi'

    def __init__(self, partCode, partType, partBrand):
        self.partCode = partCode
        self.partType = partType
        self.partBrand = partBrand

