#!/usr/bin/env python3

import connexion
from flask_sqlalchemy import SQLAlchemy
from swagger_server import encoder
from swagger_server.database import db
from flask_cors import CORS


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Control de sondas'}, pythonic_params=True)
    
    # Configuración de SQLAlchemy
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/probes_control'
    # Reemplaza 'usuario', 'contraseña' y 'nombre_de_base_de_datos' con tus propios valores
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app.app)

    CORS(app.app)
    
    # Esto te permite acceder a la instancia de SQLAlchemy en tu aplicación utilizando `app.app.db`
    
    app.run(port=8080)


if __name__ == '__main__':
    main()
