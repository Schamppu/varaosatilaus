from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, validators

class VaraosaForm(FlaskForm):
    partCode = StringField("Osakoodi", [validators.Length(min=2)])
    partType = SelectField("Tyyppi", choices=[('display', 'Näyttö'),
     ('mainboard', 'Piirikortti'), 
     ('subboard', 'Alapiirilevy'), 
     ('battery', 'Akku'), 
     ('speaker', 'Kaiutin'), 
     ('receiver', 'Kuuloke'), 
     ('handset', 'Myyntipakkaus'), 
     ('host', 'Vaihtolaite'), 
     ('cable', 'Kaapeli'), 
     ('charger', 'Laturi'), 
     ('usbcable', 'Latausjohto'), 
     ('other', 'Muu')])
    partBrand = SelectField("Merkki", choices=[('huawei', 'Huawei'),
     ('samsung', 'Samsung'), 
     ('oneplus', 'OnePlus'), 
     ('apple', 'Apple'), 
     ('nokia', 'Nokia'), 
     ('sony', 'Sony'), 
     ('cat', 'Cat'), 
     ('xiaomi', 'Xiaomi')])
  
    class Meta:
        csrf = False
