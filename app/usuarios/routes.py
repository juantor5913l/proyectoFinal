from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user


import app
#from app.models import Material
from . import usuario_blueprint
from flask import flash, url_for, render_template
from flask_bcrypt import generate_password_hash


@usuario_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('usuario_blueprint.dashboard'))

    if request.method == 'POST':
        correo_electronico = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = app.models.Usuario.query.filter_by(correo_electronico=correo_electronico).first()

        if usuario and usuario.contrasena == contrasena:
            login_user(usuario)
            return redirect(url_for('usuario_blueprint.dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')  # Mensaje de error

    return render_template('login.html')


@usuario_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('usuario_blueprint.login'))

@usuario_blueprint.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']
        contrasena = request.form['contrasena']

        # Verificar si el correo ya está en uso
        usuario_existente = app.models.Usuario.query.filter_by(correo_electronico=correo).first()

        if usuario_existente:
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'danger')
            

        nuevo_usuario = app.models.Usuario(nombre=nombre, apellido=apellido, telefono=telefono,
                                 correo_electronico=correo, direccion=direccion, contrasena=contrasena, rol_id=2)
        app.db.session.add(nuevo_usuario)
        app.db.session.commit()
        flash('Registrado correctamente', 'success')
        return redirect(url_for('usuario_blueprint.login'))

    return render_template('registro.html')
@usuario_blueprint.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol.nombre_rol == 'admin':
        return render_template('admin_dashboar.html')
    elif current_user.rol.nombre_rol == 'cliente':
        return render_template('user_dashboard.html')
    else:
        return "Rol no válido para el dashboard"
    
    
    
@usuario_blueprint.route('/perfil/<int:id>', methods=['GET', 'POST'])
@login_required
def perfil(id):
    actualizar_usuario = app.models.Usuario.query.get(id)
    if request.method == 'POST':
        actualizar_usuario.nombre = request.form['nombre']
        actualizar_usuario.apellido = request.form['apellido']
        actualizar_usuario.telefono = request.form['telefono']
        actualizar_usuario.correo_electronico = request.form['correo']
        actualizar_usuario.direccion = request.form['direccion']
        actualizar_usuario.contrasena = request.form['contrasena']
          
        app.db.session.commit()
        
        return render_template('perfil.html',usuario=actualizar_usuario )
    
