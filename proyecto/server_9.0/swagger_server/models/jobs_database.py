from swagger_server.database import db

class JobDataBase(db.Model):
    __tablename__ = 'jobs'
    JobID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BSSID = db.Column(db.String(255))
    ESSID = db.Column(db.String(255))
    Channel = db.Column(db.Integer)
    WaveLength = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('probe_groups.id'))  # Clave foránea
    Status = db.Column(db.String(255), default='stop')  # Cambiado a String
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Fecha y hora de creación automática
    is_active = db.Column(db.Boolean, default=True)  # Boolean para actividad
    band = db.Column(db.String(255))
    cswitch = db.Column(db.Integer)
    security = db.Column(db.String(255))  # Cambiado a String
    wildcard = db.Column(db.String(255))
    associated_clients = db.Column(db.Boolean, default=False)
    ChannelMode = db.Column(db.String(255))  # Cambiado a String
    URL = db.Column(db.String(255))