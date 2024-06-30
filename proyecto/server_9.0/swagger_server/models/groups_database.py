from swagger_server.database import db

class GroupDataBase(db.Model):
    __tablename__ = 'probe_groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)  # Añadir para controlar la activación/desactivación