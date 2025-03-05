from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ZodiacoForm(FlaskForm):
    nombre = StringField('Nombre', [
        DataRequired(message='El nombre es requerido'),
        Length(min=3, message='El mínimo es de 3 caracteres')
    ])
    apellido_paterno = StringField('Apellido Paterno', [
        DataRequired(message='El apellido paterno es requerido'),
        Length(min=3, message='El mínimo es de 3 caracteres')
    ])
    apellido_materno = StringField('Apellido Materno', [
        DataRequired(message='El apellido materno es requerido'),
        Length(min=3, message='El mínimo es de 3 caracteres')
    ])
    anio = IntegerField('Año de Nacimiento', [
        DataRequired(message='El año de nacimiento es requerido'),
        NumberRange(min=1900, max=2025, message='El año debe estar entre 1900 y 2025')
    ])
    mes = IntegerField('Mes de Nacimiento', [
        DataRequired(message='El mes de nacimiento es requerido'),
        NumberRange(min=1, max=12, message='Debe ser un mes válido (1-12)')
    ])
    dia = IntegerField('Día de Nacimiento', [
        DataRequired(message='El día de nacimiento es requerido'),
        NumberRange(min=1, max=31, message='Debe ser un día válido (1-31)')
    ])
    sexo = RadioField('Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M',
                      validators=[DataRequired(message='El sexo es requerido')])
    submit = SubmitField('Calcular')  # ✅ Agregamos un botón de envío
