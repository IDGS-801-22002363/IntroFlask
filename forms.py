from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms import validators

class UserForm(Form):
    matricula = IntegerField('matricula', [
        validators.DataRequired(message='El campo es requerido'),  
        validators.Length(min=3, max=10, message='de 3 a 10 caracteres')
    ])
    nombre = StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),  
        validators.Length(min=3, max=20, message='de 3 a 20 caracteres')
    ])
    apellido = StringField('apellido',[
        validators.DataRequired(message='El campo es requerido'),  
        validators.Length(min=3, max=20, message='de 3 a 20 caracteres')
    ])
    correo = EmailField('correo',[
        validators.DataRequired(message='El campo es requerido'),  
        validators.Length(min=3, max=20, message='de 3 a 20 caracteres')
    ])