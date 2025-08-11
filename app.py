from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Mascota, Tarea
from datetime import date

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
    def home():
        """
        Ruta para la página de inicio pública.
        No requiere que el usuario esté logueado.
        """
        return render_template('home.html')

    @app.route('/dashboard')
    def dashboard():
        """
        Ruta para el panel de control del usuario.
        Requiere que el usuario esté logueado.
        """
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder al panel de control.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('Cuenta no encontrada. Por favor inicia sesión de nuevo.', 'danger')
            return redirect(url_for('login'))
        
        return render_template('dashboard.html', user=user)

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
                session['user_id'] = user.id_user
                session['username'] = user.username
                flash(f'Bienvenido, {user.username}!', 'success')
                return redirect(url_for('dashboard'))
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
            
            # Crear el nuevo usuario
            password_hash = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            
            # Crear la mascota para el nuevo usuario de forma más limpia
            new_pet = Mascota(nombre_mascota='Pengu', puntos_totales=0, propietario=new_user)
            db.session.add(new_pet)
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

    # ----------------
    # Rutas para el asistente y CRUD de Tareas
    # ----------------
    @app.route('/asistente')
    def asistente():
        """Muestra la página del asistente con las tareas del usuario y su mascota."""
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder al asistente.', 'warning')
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            session.clear()
            flash('Usuario no encontrado. Por favor inicia sesión de nuevo.', 'danger')
            return redirect(url_for('login'))
            
        # Cargar las tareas del usuario ordenadas por estado (no completadas primero)
        tareas = Tarea.query.filter_by(id_usuario=user_id).order_by(Tarea.estado).all()
        mascota = Mascota.query.filter_by(id_usuario=user_id).first()
        
        # Si el usuario no tiene mascota, crear una
        if not mascota:
            mascota = Mascota(nombre_mascota='Pengu', puntos_totales=0, propietario=user)
            db.session.add(mascota)
            db.session.commit()

        return render_template('asistente.html', user=user, mascota=mascota, tareas=tareas)

    @app.route('/tareas/agregar', methods=['POST'])
    def agregar_tarea():
        """Ruta API para agregar una nueva tarea."""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'No autorizado.'}), 401
        
        data = request.json
        descripcion = data.get('descripcion')
        puntos = data.get('puntos', 1)  # Valor por defecto
        fecha_limite_str = data.get('fecha_limite')

        if not descripcion:
            return jsonify({'success': False, 'message': 'La descripción de la tarea es obligatoria.'}), 400

        fecha_limite = None
        if fecha_limite_str:
            try:
                fecha_limite = date.fromisoformat(fecha_limite_str)
            except ValueError:
                return jsonify({'success': False, 'message': 'Formato de fecha inválido. Use YYYY-MM-DD.'}), 400

        nueva_tarea = Tarea(
            descripcion_tarea=descripcion,
            puntos_tarea=puntos,
            fecha_limite=fecha_limite,
            id_usuario=session['user_id']
        )
        db.session.add(nueva_tarea)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea agregada correctamente.',
            'tarea': {
                'id': nueva_tarea.id_tarea,
                'descripcion': nueva_tarea.descripcion_tarea,
                'estado': nueva_tarea.estado,
                'puntos': nueva_tarea.puntos_tarea,
                'fecha_creacion': nueva_tarea.fecha_creacion.isoformat(),
                'fecha_limite': nueva_tarea.fecha_limite.isoformat() if nueva_tarea.fecha_limite else None
            }
        }), 201

    @app.route('/tareas/completar/<int:id_tarea>', methods=['POST'])
    def completar_tarea(id_tarea):
        """Ruta API para marcar una tarea como completada y sumar puntos."""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'No autorizado.'}), 401
        
        tarea = Tarea.query.get(id_tarea)
        if not tarea or tarea.id_usuario != session['user_id']:
            return jsonify({'success': False, 'message': 'Tarea no encontrada o no tienes permisos.'}), 404
            
        if not tarea.estado:
            tarea.estado = True
            
            mascota = Mascota.query.filter_by(id_usuario=session['user_id']).first()
            if mascota:
                mascota.puntos_totales += tarea.puntos_tarea
                db.session.commit()
            else:
                db.session.commit()
                return jsonify({'success': False, 'message': 'Mascota no encontrada para el usuario.'}), 500

            return jsonify({
                'success': True,
                'message': 'Tarea completada y puntos sumados.',
                'tarea': {
                    'id': tarea.id_tarea,
                    'estado': tarea.estado
                },
                'puntos_mascota': mascota.puntos_totales
            })
        
        return jsonify({'success': False, 'message': 'La tarea ya estaba completada.'}), 200

    @app.route('/tareas/eliminar/<int:id_tarea>', methods=['DELETE'])
    def eliminar_tarea(id_tarea):
        """Ruta API para eliminar una tarea."""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'No autorizado.'}), 401
            
        tarea = Tarea.query.get(id_tarea)
        if not tarea or tarea.id_usuario != session['user_id']:
            return jsonify({'success': False, 'message': 'Tarea no encontrada o no tienes permisos.'}), 404
            
        db.session.delete(tarea)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tarea eliminada correctamente.'}), 200

    return app

# -----------------
# Inicio de la aplicación
# -----------------
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
