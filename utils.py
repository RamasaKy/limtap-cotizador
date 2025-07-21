from datetime import datetime
import csv, os

TARIFAS = {
    "colchón": 150000,
    "sofá": 120000,
    "sofacama": 180000,
    "silla sala": 30000,
    "vehículo": 150000,
    "silla comedor sencilla": 25000,
    "silla comedor forrada": 30000
}
DESCUENTOS = {"referido": 0.10, "promo_instagram": 0.15}

def calcular_total(unidades, tipo_objeto, descuento=None):
    precio_base = TARIFAS.get(tipo_objeto.lower(), 0)
    if not precio_base:
        return None
    total = unidades * precio_base
    if descuento and descuento != "ninguno":
        total *= (1 - DESCUENTOS.get(descuento, 0))
    return round(total)

def guardar_cotizacion(unidades, tipo_objeto, total, descuento_aplicado, cliente):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    archivo = "cotizaciones.csv"
    escribir_encabezados = not os.path.exists(archivo)

    try:
        with open(archivo, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if escribir_encabezados:
                writer.writerow(["Fecha", "Cliente", "Unidades", "Tipo", "Descuento", "Total"])
            writer.writerow([fecha, cliente, unidades, tipo_objeto, descuento_aplicado, total])
    except PermissionError:
        print("⚠️ El archivo 'cotizaciones.csv' está abierto. Cierra Excel y vuelve a intentarlo.")
