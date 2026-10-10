from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.usuario import Usuario
from flask_app import bcrypt
import re

usuarios_bp = Blueprint('usuarios', __name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@usuarios_bp.route('/')
def vista_login():
    if 'usuario_id' in session:
        return redirect('/peluches/dashboard')
    return render_template('iniciar_sesion.html')

@usuarios_bp.route('/registrarse')
def vista_registro():
    if 'usuario_id' in session:
        return redirect('/peluches/dashboard')
    return render_template('registrarse.html')

@usuarios_bp.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    email = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '')
    confirmar = request.form.get('confirmar_contrasena', '')

    errores = False

    if len(nombre) < 2 or len(apellido) < 2:
        flash("El nombre y apellido deben tener al menos 2 caracteres.", "registro")
        errores = True

    if not EMAIL_REGEX.match(email):
        flash("El formato de correo electrónico es inválido.", "registro")
        errores = True

    if contrasena != confirmar:
        flash("Las contraseñas no coinciden.", "registro")
        errores = True

    if Usuario.obtener_por_email(email):
        flash("Este correo electrónico ya se encuentra registrado.", "registro")
        errores = True

    if errores:
        return redirect('/registrarse')

    password_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasena": password_hash
    }

    Usuario.registrar(data)
    flash("¡Registro exitoso! Por favor inicia sesión.", "login_success")
    return redirect('/')

@usuarios_bp.route('/procesar_login', methods=['POST'])
def procesar_login():
    email = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '')

    usuario_encontrado = Usuario.obtener_por_email(email)

    if not usuario_encontrado:
        flash("El correo electrónico no se encuentra registrado.", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario_encontrado.contrasena, contrasena):
        flash("La contraseña proporcionada es incorrecta.", "login")
        return redirect('/')

    session['usuario_id'] = usuario_encontrado.id_usuario
    session['usuario_nombre'] = f"{usuario_encontrado.nombre} {usuario_encontrado.apellido}"

    return redirect('/peluches/dashboard')

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
