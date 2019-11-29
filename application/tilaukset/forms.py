from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, FieldList, FormField, Form, validators


class TilausForm(Form):
    
    orderPlace = SelectField("Toimipaikka", choices=[('hes-helsinki', 'Huawei Experience Store Helsinki'),
     ('hcsc-tampere', 'Huawei Customer Service Center Tampere'), 
     ('dna-sello', 'DNA Sello'), 
     ('dna-hameenkatu', 'DNA Hämeenkatu')])

    orderStatus = SelectField("Tilauksen vaihe", choices=[('draft', 'Luonnos'),
     ('in-progress', 'Käsittelyssä varastossa'), 
     ('waiting', 'Odottaa varaosaa/toimenpiteitä'), 
     ('cancelled', 'Toimitushäiriö'), 
     ('sent', 'Lähetetty')])



    class Meta:
        csrf = False


class TilausAddForm(Form):
    
    orderPart = StringField("Osakoodi", [validators.Length(min=2)])

    class Meta:
        csrf = False