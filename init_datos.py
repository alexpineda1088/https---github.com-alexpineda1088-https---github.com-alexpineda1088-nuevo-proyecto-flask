import os
import json
import csv

# 📂 Carpeta de datos
os.makedirs("datos", exist_ok=True)

# 📄 Rutas de archivos
TXT_FILE = "datos/datos.txt"
JSON_FILE = "datos/datos.json"
CSV_FILE = "datos/datos.csv"

# 📦 Datos de ejemplo (20 productos como en la DB)
productos = [
    {"nombre": "Leche", "precio": 1.20, "cantidad": 50},
    {"nombre": "Pan", "precio": 0.80, "cantidad": 100},
    {"nombre": "Huevos", "precio": 0.10, "cantidad": 200},
    {"nombre": "Arroz", "precio": 0.50, "cantidad": 150},
    {"nombre": "Frijoles", "precio": 0.60, "cantidad": 80},
    {"nombre": "Azúcar", "precio": 0.70, "cantidad": 120},
    {"nombre": "Sal", "precio": 0.30, "cantidad": 100},
    {"nombre": "Aceite", "precio": 2.00, "cantidad": 60},
    {"nombre": "Queso", "precio": 3.50, "cantidad": 40},
    {"nombre": "Jabón", "precio": 1.00, "cantidad": 70},
    {"nombre": "Shampoo", "precio": 4.00, "cantidad": 50},
    {"nombre": "Cereal", "precio": 2.50, "cantidad": 60},
    {"nombre": "Yogur", "precio": 0.90, "cantidad": 80},
    {"nombre": "Mantequilla", "precio": 1.50, "cantidad": 40},
    {"nombre": "Tomate", "precio": 0.40, "cantidad": 100},
    {"nombre": "Lechuga", "precio": 0.60, "cantidad": 90},
    {"nombre": "Pollo", "precio": 5.00, "cantidad": 30},
    {"nombre": "Carne", "precio": 6.00, "cantidad": 25},
    {"nombre": "Pescado", "precio": 7.00, "cantidad": 20},
    {"nombre": "Café", "precio": 3.00, "cantidad": 50},
]

# ✅ Crear TXT
if not os.path.exists(TXT_FILE):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        for p in productos:
            f.write(f"{p['nombre']},{p['precio']},{p['cantidad']}\n")
    print("✅ datos.txt creado")

# ✅ Crear JSON
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)
    print("✅ datos.json creado")

# ✅ Crear CSV
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nombre", "precio", "cantidad"])  # encabezado
        for p in productos:
            writer.writerow([p["nombre"], p["precio"], p["cantidad"]])
    print("✅ datos.csv creado")

print("📂 Archivos TXT, JSON y CSV inicializados correctamente.")
