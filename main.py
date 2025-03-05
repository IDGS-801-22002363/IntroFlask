from flask import Flask, render_template, request, jsonify, flash, g
from datetime import datetime
import re
import forms_zodiaco
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "esta es una clave secreta"
csrf = CSRFProtect(app)

# 🔹 Configuración para la compra de boletos
PRECIO_BOLETO = 12
MAX_BOLETOS_POR_PERSONA = 7

@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    g.user = "mario"
    print("before request ejecutado")

def calcular_precio(boletos, metodo_pago):
    total = boletos * PRECIO_BOLETO
    if metodo_pago == "tarjeta cineco":
        if boletos > 5:
            total *= 0.85  # 15% descuento
        elif 3 <= boletos <= 5:
            total *= 0.90  # 10% descuento
        total *= 0.90  # 10% adicional por tarjeta
    return round(total, 2)

# 🔹 Diccionario de signos del zodiaco chino
zodiac_signs = [
    "Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente",
    "Caballo", "Cabra", "Mono", "Gallo", "Perro", "Cerdo"
]

@app.route('/')
def index():
    grupo = "IDGS801"
    lista = ["Juan", "Pedro", "Mario"]
    nom = g.user
    return render_template('index.html', grupo=grupo, nom=nom, lista=lista)

@app.route('/cine', methods=['GET', 'POST'])
def cine():
    if request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        personas = int(data.get('personas'))
        boletos = int(data.get('boletos'))
        metodo_pago = data.get('metodo_pago')

        if not nombre.isalpha():
            return jsonify({'error': 'El nombre no puede contener números ni caracteres especiales'}), 400
        if boletos > personas * MAX_BOLETOS_POR_PERSONA:
            return jsonify({'error': f'No puedes comprar más de {personas * MAX_BOLETOS_POR_PERSONA} boletos'}), 400
        if metodo_pago not in ["efectivo", "tarjeta cineco"]:
            return jsonify({'error': 'Método de pago inválido'}), 400

        total_a_pagar = calcular_precio(boletos, metodo_pago)
        return jsonify({'total_a_pagar': total_a_pagar})

    return render_template('cine.html')
@app.route('/zodiaco', methods=['GET', 'POST'])
def zodiaco():
    form = forms_zodiaco.ZodiacoForm()  # ✅ Aseguramos que se crea correctamente
    resultado = None

    if request.method == 'POST' and form.validate_on_submit():  # ✅ Cambiar a validate_on_submit()
        nombre = form.nombre.data
        apellido_paterno = form.apellido_paterno.data
        apellido_materno = form.apellido_materno.data
        anio = form.anio.data
        mes = form.mes.data
        dia = form.dia.data
        sexo = form.sexo.data

        # Cálculo de edad
        fecha_nacimiento = datetime(anio, mes, dia)
        edad = datetime.now().year - fecha_nacimiento.year
        if (datetime.now().month, datetime.now().day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1

        signo_chino = zodiac_signs[anio % 12]

        resultado = {
            "nombre_completo": f"{nombre} {apellido_paterno} {apellido_materno}",
            "edad": edad,
            "signo_chino": signo_chino,
            "sexo": "Masculino" if sexo == "M" else "Femenino"
        }

    return render_template("zodiaco.html", form=form, resultado=resultado)  # ✅ Asegurar que form se pase correctamente


if __name__ == '__main__':
    app.run(debug=True, port=3000)