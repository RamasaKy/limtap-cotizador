from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv
import os
from utils import calcular_total

app = Flask(__name__)
app.secret_key = "limtap-secreto"

CSV_FILE = "cotizaciones.csv"

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

            # Guardar en CSV
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M'), cliente, objeto, cantidad, descuento, total])

            return render_template("index.html", objetos=objetos, descuentos=descuentos, total=total)
        except ValueError:
            flash("La cantidad debe ser un número entero.", "error")
            return redirect(url_for("index"))

    return render_template("index.html", objetos=objetos, descuentos=descuentos, total=total)

@app.route("/historial")
def historial():
    cotizaciones = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                cotizaciones.append({
                    "fecha": row[0],
                    "cliente": row[1],
                    "objeto": row[2],
                    "cantidad": row[3],
                    "descuento": row[4],
                    "total": row[5]
                })
    return render_template("historial.html", cotizaciones=cotizaciones)

if __name__ == "__main__":
    app.run(debug=True)
