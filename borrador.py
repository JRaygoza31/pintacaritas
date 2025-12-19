# borrador.py
from app import create_app  # o donde crees tu app Flask
from extensiones import db
from models import Servicio

app = create_app()  # Inicializa tu app Flask

with app.app_context():
    # ⚠️ Esto borrará todos los datos de la tabla servicios
    Servicio.__table__.drop(db.engine, checkfirst=True)
    Servicio.__table__.create(db.engine, checkfirst=True)

    print("Tabla 'servicios' recreada con éxito.")
