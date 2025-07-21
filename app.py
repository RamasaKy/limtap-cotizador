from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
from models import db, Cotizacion  # Importamos SQLAlchemy y el modelo

app = Flask(__name__)
app.secret_key = "limtap-secreto"

# Configuración de base de datos (Render la envía como variable de entorno)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crea las tablas si no existen
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    objetos = ["colchón", "sofá", "sofacama", "silla sala", "vehículo", "silla comedor sencilla", "silla comedor forrada"]
    descuentos = ["ninguno", "referido", "promo_instagram"]
    total = None

    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        objeto = request.form.get("objeto")
        cantidad = request.form.get("cantidad")
        descuento = request.form.get("descuento")

        if not cliente or not cantidad:
            flash("Debe ingresar el nombre del cliente y la cantidad.", "error")
            return redirect(url_for("index"))

        try:
            cantidad = int(cantidad)
            # Calcula el total
            from utils import calcular_total
            total = calcular_total(cantidad, objeto, descuento if descuento != "ninguno" else None)

            # Guarda en la base de datos
            nueva_cotizacion = Cotizacion(
                cliente=cliente,
                objeto=objeto,
                cantidad=cantidad,
                descuento=descuento,
                total=total,
                fecha=datetime.now()
            )
            db.session.add(nueva_cotizacion)
            db.session.commit()

            return render_template("index.html", objetos=objetos, descuentos=descuentos, total=total)
        except ValueError:
            flash("La cantidad debe ser un número entero.", "error")
            return redirect(url_for("index"))

    return render_template("index.html", objetos=objetos, descuentos=descuentos, total=total)
@app.route("/historial")
def historial():
    cotizaciones = Cotizacion.query.order_by(Cotizacion.fecha.desc()).all()
    return render_template("historial.html", cotizaciones=cotizaciones)

if __name__ == "__main__":
    app.run(debug=True)


