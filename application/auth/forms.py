from flask_wtf import FlaskForm, Form
from wtforms import PasswordField, StringField, SelectField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False

class ManageForm(Form):
    
    role = SelectField("Käyttäjäryhmä", choices=[('admin', 'Järjestelmänvalvoja (admin)'),
     ('warehouse', 'Varastotyöntekijä'), 
     ('retail', 'Myymälätyöntekijä')])


    name = StringField("Nimi")
    username = StringField("Käyttäjätunnus")
    password = PasswordField(
        "Salasana",
        [
            validators.Length(min=2),
            validators.Required(),
            validators.EqualTo('passwordCheck', message='Salasanojen tulee täsmätä!')

        ])
    passwordCheck = PasswordField("Salasana uudelleen")

    class Meta:
        csrf = False