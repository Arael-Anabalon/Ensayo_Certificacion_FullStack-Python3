from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_app.models.peluche import Peluche

peluches_bp = Blueprint('peluches', __name__, url_prefix='/peluches')

def usuario_autenticado():
    return 'usuario_id' in session

@peluches_bp.route('/dashboard')
def dashboard():
    if not usuario_autenticado():
        flash("Debes iniciar sesión primero.", "login")
        return redirect('/')
    todos = Peluche.obtener_todos_con_usuarios()
    return render_template('dashboard.html', peluches=todos)

@peluches_bp.route('/nuevo')
def vista_nueva_donacion():
    if not usuario_autenticado():
        return redirect('/')
    return render_template('nueva_donacion.html')

@peluches_bp.route('/crear', methods=['POST'])
def crear_peluche():
    if not usuario_autenticado():
        return redirect('/')

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    datos_formulario = {"nombre": nombre, "descripcion": descripcion}

    if not nombre or not descripcion:
        flash("Los campos nombre y descripción no pueden estar vacíos.", "peluche_error")
        flash(datos_formulario, "datos_previos")
        return redirect('/peluches/nuevo')

    if not Peluche.validar_nombre_unico(nombre):
        flash("El nombre del peluche ya existe. Debe ser único.", "peluche_error")
        flash(datos_formulario, "datos_previos")
        return redirect('/peluches/nuevo')

    data = {
        "nombre": nombre,
        "descripcion": descripcion,
        "creador_id": session['usuario_id'],
        "created_by": session['usuario_nombre']
    }
    Peluche.guardar(data)
    return redirect('/peluches/dashboard')

@peluches_bp.route('/ver/<int:id>')
def ver_peluche(id):
    if not usuario_autenticado():
        return redirect('/')

    Peluche.incrementar_vista(id)
    peluche_seleccionado = Peluche.obtener_por_id_con_usuarios(id)
    if not peluche_seleccionado:
        return redirect('/peluches/dashboard')

    return render_template('ver_peluche.html', peluche=peluche_seleccionado)

@peluches_bp.route('/editar/<int:id>')
def vista_editar_donacion(id):
    if not usuario_autenticado():
        return redirect('/')
    
    peluche_editar = Peluche.obtener_por_id_con_usuarios(id)
    if not peluche_editar or peluche_editar.creador_id != session['usuario_id']:
        return redirect('/peluches/dashboard')
        
    return render_template('editar_donacion.html', peluche=peluche_editar)

@peluches_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_peluche(id):
    if not usuario_autenticado():
        return redirect('/')

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    datos_formulario = {"nombre": nombre, "descripcion": descripcion}

    if not nombre or not descripcion:
        flash("Todos los campos son obligatorios.", "editar_error")
        flash(datos_formulario, "datos_previos")
        return redirect(f'/peluches/editar/{id}')

    if not Peluche.validar_nombre_unico(nombre, id_peluche=id):
        flash("Ese nombre ya pertenece a otro peluche.", "editar_error")
        flash(datos_formulario, "datos_previos")
        return redirect(f'/peluches/editar/{id}')

    data = {
        "id_peluche": id,
        "nombre": nombre,
        "descripcion": descripcion,
        "updated_by": session['usuario_nombre']
    }
    Peluche.actualizar(data)
    return redirect('/peluches/dashboard')

@peluches_bp.route('/adoptar/<int:id>', methods=['POST'])
def adoptar_peluche(id):
    if not usuario_autenticado():
        return redirect('/')

    Peluche.adoptar({"id_peluche": id, "adoptador_id": session['usuario_id']})
    return redirect('/peluches/dashboard')

@peluches_bp.route('/eliminar/<int:id>')
def eliminar_peluche(id):
    if not usuario_autenticado():
        return redirect('/')
    Peluche.eliminar(id)
    return redirect('/peluches/dashboard')
