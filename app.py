from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv, os
from utils import calcular_total, guardar_cotizacion

app = Flask(__name__)
app.secret_key = "limtap-secreto"

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
            total = calcular_total(cantidad, objeto, descuento if descuento != "ninguno" else None)
            guardar_cotizacion(cantidad, objeto, total, descuento, cliente)
            return render_template("index.html", objetos=objetos, descuentos=descuentos, total=total)
        except ValueError:
            flash("La cantidad debe ser un número entero.", "error")
            return redirect(url_for("index"))

    return render_template("index.html", objetos=objetos, descuentos=descuentos, total=total)

if __name__ == "__main__":
    app.run(debug=True)

