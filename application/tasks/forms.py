from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class TaskForm(FlaskForm):
    name = StringField("Varaosa", [validators.Length(min=2)])
    done = BooleanField("Toimitettu?")
  
    class Meta:
        csrf = False
