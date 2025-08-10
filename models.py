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
    # 'mascota' es la relación 'uno a uno' con la tabla Mascotas.
    # 'backref' crea un atributo 'propietario' en la clase Mascota.
    # 'uselist=False' es para que la relación sea de uno a uno.
    # Usamos "cascade='all, delete-orphan'" para asegurar que al eliminar un usuario,
    # también se elimine su mascota y todas sus tareas asociadas.
    # Esto es intencional y debe coincidir con la lógica de negocio.
    mascota = db.relationship('Mascota', backref='propietario', uselist=False, cascade="all, delete-orphan")

    # 'tareas' es la relación 'uno a muchos' con la tabla Tareas.
    # 'lazy=True' carga la lista de tareas solo cuando la necesitas.
    # También usamos "cascade='all, delete-orphan'" para eliminar todas las tareas del usuario al eliminarlo.
    tareas = db.relationship('Tarea', backref='creador', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

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
    # 'unique=True' es crucial para la relación de uno a uno.
    # Esto asegura que cada mascota esté asociada a un único usuario, 
    # implementando la relación uno a uno en la base de datos.
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id_user'), unique=True, nullable=False)
    
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
    puntos_tarea = db.Column(db.Integer, nullable=False)
    fecha_limite = db.Column(db.Date, nullable=True)

    # Clave foránea que la relaciona con el usuario.
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)

    def __repr__(self):
        return f'<Tarea {self.descripcion_tarea}>'

