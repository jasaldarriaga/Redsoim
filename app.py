import hashlib
from flask import Flask,render_template,request,session, redirect
from flask_wtf import CSRFProtect
#Importa la libreria de SQLITE
import sqlite3


app=Flask(__name__)
app.secret_key = 'Santiago_Martha22'
csrf = CSRFProtect(app)
num_elements_to_generate = 500

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
        # return "Contraseña no coincide"
        return render_template("ventana_modal.html",datos ="contraseña no coincide!!")
    
    if not nombre:
        # return "Debe digitar un Usuario"
        return render_template("ventana_modal.html",datos ="Debe digitar un usuario!")
    
    if not contrasena:
        # return "Debe digitar una Contraseña"
        return render_template("ventana_modal.html",datos ="Dede digitar una contraseña!")

    clave = hashlib.sha256(contrasena.encode())
    pwd= clave.hexdigest()
    
    #conexion base de datos
    with sqlite3.connect("redsoim.db") as con:
        cur=con.cursor()
        #consultar si usuario ya existe
        cur.execute("SELECT email FROM usuarios WHERE email=?",[email])
        if cur.fetchone():
            # return "El usuario ya existe!"
            return render_template("ventana_modal.html",datos ="El usuario ya existe!")
        #crea el nuevo usuario
        cur.execute("INSERT INTO usuarios(nombre,email,contrasena) VALUES(?,?,?)",[nombre,
        email,pwd])
        #
        con.commit()
        return render_template("ventana_modal.html",datos ="Usuario creado, Bienvenido!!")

@app.route("/login", methods=['post'])
def login():
    #captura datos enviados
    nombre=request.form["txtNombre"]
    contrasena=request.form["txtContrasena"]
    #validaciones
    if not nombre or not contrasena:
        # return "Usuario/Contraseña son requeridos"
        return render_template("ventana_modal.html",datos ="Usuario/Contraseña son requeridos!!")
    if len(nombre)>10:
        # return "Nombre Usuario excede la longitud maxima"
        return render_template("ventana_modal.html",datos ="Nombre Usuario excede la longitud maxima!!")

    clave = hashlib.sha256(contrasena.encode())
    pwd= clave.hexdigest()

    with sqlite3.connect("redsoim.db") as con:
        cur=con.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE nombre=? AND contrasena = ?",[nombre,pwd])
        if cur.fetchone():
            session["usuario"]=nombre
            return render_template("inicio_seccion.html",usuario=nombre)
            # return "Bienvenido"
        
    return render_template("ventana_modal.html",datos ="Usuario Invalido")

@app.route("/logout")
def logout():
   # remueve el usuario de la seccion
   session.pop('usuario', None)
   return redirect("/")

app.run(debug=True)