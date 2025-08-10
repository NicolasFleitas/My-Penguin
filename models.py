from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    """
    Representa la tabla 'users' en la base de datos.
    Cada instancia de esta clase es una fila en la tabla.
    """
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    # Relaciones de SQLAlchemy
    # Usamos back_populates para definir relaciones explícitas en ambos lados,
    # lo cual ayuda a evitar errores de recursión.
    mascota = db.relationship('Mascota', back_populates='propietario', uselist=False, cascade="all, delete-orphan")
    tareas = db.relationship('Tarea', back_populates='propietario', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class Mascota(db.Model):
    """
    Representa la tabla 'Mascotas'.
    Relacionada con Usuario a través de 'id_usuario'.
    """
    __tablename__ = 'mascotas'
    id_mascota = db.Column(db.Integer, primary_key=True)
    nombre_mascota = db.Column(db.String(20), nullable=False)
    puntos_totales = db.Column(db.Integer, default=0)
    
    # Clave foránea que la relaciona con el usuario.
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id_user'), unique=True, nullable=False)
    
    # Relación de vuelta al propietario
    propietario = db.relationship('User', back_populates='mascota')

    def __repr__(self):
        return f'<Mascota {self.nombre_mascota}>'


class Tarea(db.Model):
    """
    Representa la tabla 'Tareas'.
    Relacionada con Usuario a través de 'id_usuario'.
    """
    __tablename__ = 'tareas'
    id_tarea = db.Column(db.Integer, primary_key=True)
    descripcion_tarea = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.Date, default=date.today())
    puntos_tarea = db.Column(db.Integer, default=1)
    fecha_limite = db.Column(db.Date, nullable=True)

    # Clave foránea que la relaciona con el usuario.
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    
    # Relación de vuelta al propietario
    propietario = db.relationship('User', back_populates='tareas')

    def __repr__(self):
        return f'<Tarea {self.descripcion_tarea}>'
