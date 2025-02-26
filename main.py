from flask import Flask, render_template, request, jsonify, flash, g
from datetime import datetime
import forms
import re
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "esta es una clave secreta"
csrf = CSRFProtect(app)  # 🔹 Corrección en la inicialización de CSRFProtect

# 🔹 Configuración para la compra de boletos
PRECIO_BOLETO = 12
MAX_BOLETOS_POR_PERSONA = 7

@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html'), 404  # 🔹 Corrección en `render_templeate`

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
zodiac_signs = {
    0: "Mono", 1: "Gallo", 2: "Perro", 3: "Cerdo", 4: "Rata", 5: "Buey",
    6: "Tigre", 7: "Conejo", 8: "Dragón", 9: "Serpiente", 10: "Caballo", 11: "Cabra"
}

# 🔹 Página principal
@app.route('/')
def index():
    grupo = "IDGS801"
    lista = ["Juan", "Pedro", "Mario"]
    nom = g.user
    print("Index 2{}".format(g.user))
    return render_template('index.html', grupo=grupo, nom=nom, lista=lista)

# 🔹 Página del cine (frontend y backend en una sola ruta)
@app.route('/cine', methods=['GET', 'POST'])
def cine():
    if request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        personas = int(data.get('personas'))
        boletos = int(data.get('boletos'))
        metodo_pago = data.get('metodo_pago')

        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre):
            return jsonify({'error': 'El nombre no puede contener números ni caracteres especiales'}), 400
        if boletos > personas * MAX_BOLETOS_POR_PERSONA:
            return jsonify({'error': f'No puedes comprar más de {personas * MAX_BOLETOS_POR_PERSONA} boletos'}), 400
        if metodo_pago not in ["efectivo", "tarjeta cineco"]:
            return jsonify({'error': 'Método de pago inválido'}), 400

        total_a_pagar = calcular_precio(boletos, metodo_pago)
        return jsonify({'total_a_pagar': total_a_pagar})

    return render_template('cine.html')

# 🔹 Página del Zodiaco Chino
@app.route('/zodiaco', methods=['GET', 'POST'])
def zodiaco():
    resultado = None
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido_paterno = request.form["apellido_paterno"]
        apellido_materno = request.form["apellido_materno"]
        dia = int(request.form["dia"])
        mes = int(request.form["mes"])
        anio = int(request.form["anio"])
        sexo = request.form["sexo"]

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

    return render_template("zodiaco.html", resultado=resultado)

# 🔹 Página de operaciones básicas
@app.route("/OperasBas")
def operas():
    return render_template("OperasBas.html")

@app.route('/OperasBas', methods=['POST'])
def resultado():
    resultado = ''
    
    if request.method == 'POST':
        n1 = int(request.form.get('n1'))
        n2 = int(request.form.get('n2'))
        operacion = request.form.get('operacion')
        
        if operacion == 'suma':
            resultado = n1 + n2
        elif operacion == 'resta':
            resultado = n1 - n2
        elif operacion == 'multiplicacion':
            resultado = n1 * n2
        elif operacion == 'division':
            if n2 != 0:
                resultado = n1 / n2
            else:
                resultado = 'No se puede dividir entre 0'
    
    return render_template('OperasBas.html', resultado=resultado)

@app.route("/Alumnos", methods=["GET", "POST"])  # 🔹 Corrección en la ruta
def alumnos():
    mat = 0
    nom = ''
    ape = ''
    email = ''
    alumno_clas = forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clas.validate():
        mat = alumno_clas.matricula.data
        nom = alumno_clas.nombre.data
        ape = alumno_clas.apellido.data
        email = alumno_clas.correo.data

        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje)

    return render_template("Alumnos.html", form=alumno_clas, mat=mat, nom=nom, ape=ape, email=email)

# 🔹 Páginas de ejemplo
@app.route('/ejemplo1')
def ejemplo1():
    return render_template('ejemplo1.html')

@app.route('/ejemplo2')
def ejemplo2():
    return render_template('ejemplo2.html')

# 🔹 Rutas dinámicas
@app.route("/hola")
def hola():
    return "Hola!!!!"

@app.route("/user/<string:user>")
def user(user):
    return f"Hola {user}!!!"

@app.route("/numero/<int:n>")
def numero(n):
    return f"Numero {n}"

@app.route("/user/<string:user>/<int:id>")
def username(user, id):
    return f"Nombre: {user} ID: {id}!!!"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"La suma es: {n1 + n2}!!"

# 🔹 Formulario simple
@app.route("/form1")
def form1():
    return '''
        <form>
            <label>Nombre:</label>
            <input type="text" name="nombre" placeholder="Nombre">
            </br>
            <label>Apellido:</label>
            <input type="text" name="apellido" placeholder="Apellido">
            </br>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=3000)
