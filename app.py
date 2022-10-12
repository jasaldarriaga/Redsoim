import hashlib
from flask import Flask,render_template,request
#Importa la libreria de SQLITE
import sqlite3


app=Flask(__name__)

# Endpoint para cargar formulario Estudiantes
@app.route("/")
def home():
    return render_template("home.html")
#Endpoint para procesar los datos del formulario reguistrarse
@app.route("/usuario/crear", methods=["post"])
def crear():
    nombre = request.form["txtNombre"]
    email = request.form["txtEmail"]
    contrasena=request.form["txtContraseña"]
    confirmar=request.form["txtConfirmar"]

    if(contrasena != confirmar):
        return "Contraseña no coincide"
    
    if not nombre:
        return "Debe digitar un Usuario"
    
    if not contrasena:
        return "Debe digitar una Contraseña"

    clave = hashlib.sha256(contrasena.encode())
    pwd= clave.hexdigest()
    
    #conexion base de datos
    with sqlite3.connect("redsoim.db") as con:
        cur=con.cursor()
        #consultar si usuario ya existe
        cur.execute("SELECT email FROM usuarios WHERE email=?",[email])
        if cur.fetchone():
            return "El usuario ya existe!"
        #crea el nuevo usuario
        cur.execute("INSERT INTO usuarios(nombre,email,contrasena) VALUES(?,?,?)",[nombre,
        email,pwd])
        #
        con.commit()
        return "Usuario Creado, Bienvenido a RedSoim"

@app.route("/login", methods=['post'])
def login():
    #captura datos enviados
    nombre=request.form["txtNombre"]
    contrasena=request.form["txtContrasena"]
    #validaciones
    if not nombre or not contrasena:
        return "Usuario/Contraseña son requeridos"
    if len(nombre)>10:
        return "Nombre Usuario excede la longitud maxima"

    clave = hashlib.sha256(contrasena.encode())
    pwd= clave.hexdigest()

    with sqlite3.connect("redsoim.db") as con:
        cur=con.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE nombre=? AND contrasena = ?",[nombre,pwd])
        if cur.fetchone():
            # seccion["usuario"]=nombre
            # return render_template("inicio_seccion.html",usuario=nombre)
            return "Bienvenido"
        
    return "Usuario invalido!!!"
app.run(debug=False,port=5500)