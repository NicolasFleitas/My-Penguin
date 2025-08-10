from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Mascota, Tarea

# ----------------
# Configuración de la aplicación Flask
# ----------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app) 

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('Cuenta no encontrada. Por favor inicia sesión de nuevo.', 'danger')
            return redirect(url_for('login'))
        return render_template('index.html', user=user)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            user = User.query.filter_by(username=username).first()
            if not user:
                flash('Usuario no encontrado. Por favor crea una cuenta.', 'info')
                return redirect(url_for('register'))
            if check_password_hash(user.password_hash, password):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Bienvenido, {user.username}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta. Inténtalo de nuevo.', 'danger')
                return render_template('login.html', username=username)
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            password2 = request.form.get('password2', '')
            if not username or not email or not password or not password2:
                flash('Todos los campos son obligatorios.', 'warning')
                return render_template('register.html', username=username, email=email)
            if password != password2:
                flash('Las contraseñas no coinciden.', 'warning')
                return render_template('register.html', username=username, email=email)
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                if existing_user.username == username:
                    flash('El nombre de usuario ya está en uso.', 'danger')
                else:
                    flash('El email ya está registrado.', 'danger')
                return render_template('register.html', username=username, email=email)
            password_hash = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Has cerrado sesión correctamente.', 'info')
        return redirect(url_for('login'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

# -----------------
# Inicio de la aplicación
# -----------------


# OPCION 2


# @app.route('/crear-db')
# def crear_db():
#     """
#     Ruta para crear la base de datos y las tablas.
#     Solo necesitas ejecutarla una vez.
#     """
#     with app.app_context():
#         db.create_all()
#     return "Base de datos creada exitosamente."

# @app.route('/crear-ejemplo')
# def crear_ejemplo():
#     """
#     Ruta para crear un usuario de ejemplo con su mascota y tareas.
#     """
#     with app.app_context():
#         # Creamos un nuevo usuario
#         nuevo_usuario = Usuario(nombre="Juan Pérez", email="juan@ejemplo.com", password="password123")
#         db.session.add(nuevo_usuario)
#         db.session.commit()

#         # Creamos una mascota y la asignamos al usuario
#         nueva_mascota = Mascota(nombre_mascota="Fido", puntos_totales=150, propietario=nuevo_usuario)
#         db.session.add(nueva_mascota)

#         # Creamos dos tareas y las asignamos al usuario
#         tarea1 = Tarea(descripcion_tarea="Comprar comida para perro", puntos_tarea=20, creador=nuevo_usuario)
#         tarea2 = Tarea(descripcion_tarea="Pasear a Fido por el parque", puntos_tarea=50, creador=nuevo_usuario)
#         db.session.add_all([tarea1, tarea2])
#         db.session.commit()
    
#     return "Usuario de ejemplo y datos relacionados creados."


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
