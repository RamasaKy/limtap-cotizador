from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cotizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    objeto = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    descuento = db.Column(db.String(50))
    total = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
