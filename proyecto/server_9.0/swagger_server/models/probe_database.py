from swagger_server.database import db

class ProbeDataBase(db.Model):
    __tablename__ = 'probes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    last_recorded_ip = db.Column(db.String(255))
    in_use = db.Column(db.Boolean)
    group_id = db.Column(db.Integer, db.ForeignKey('probe_groups.id'))
    is_active = db.Column(db.Boolean, default=True)  # Campo adicional para manejar el estado activo/inactivo
    data = db.Column(db.JSON)  # Campo JSON para almacenar datos adicionales
