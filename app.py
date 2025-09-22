from flask import Flask, render_template, request, redirect, url_for, flash
from Conexion.conexion import get_connection
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------------------
# Inicializar Base de Datos
# ------------------------------
def inicializar_db():
    conn = get_connection()
    if not conn:
        print("No se pudo conectar a MySQL")
        return
    cursor = conn.cursor()
    try:
        # Tabla productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                cantidad INT NOT NULL,
                precio DECIMAL(10,2) NOT NULL
            )
        """)

        # Tabla ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                producto VARCHAR(50) NOT NULL,
                cantidad INT NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                fecha DATE NOT NULL
            )
        """)

        # Tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                mail VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Inserción inicial de productos (solo si no hay registros)
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            productos = [
                ('Leche', 50, 1.20), ('Pan', 100, 0.80), ('Huevos', 200, 0.10),
                ('Arroz', 150, 0.50), ('Frijoles', 80, 0.60), ('Azúcar', 120, 0.70),
                ('Aceite', 60, 2.00)
            ]
            cursor.executemany(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)", productos
            )

        conn.commit()
    except Exception as e:
        print("Error al inicializar la base de datos:", e)
    finally:
        cursor.close()
        conn.close()

# ------------------------------
# Rutas principales
# ------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------------
# Productos
# ------------------------------
@app.route('/productos')
def productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos_db=productos_db)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')

        if not nombre or not cantidad or not precio:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('agregar'))

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            flash("Cantidad y precio deben ser numéricos", "danger")
            return redirect(url_for('agregar'))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
            (nombre, cantidad, precio)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Producto agregado correctamente", "success")
        return redirect(url_for('productos'))

    return render_template('agregar.html')

# ------------------------------
# Inventario
# ------------------------------
@app.route('/inventario')
def inventario():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre, cantidad FROM productos")
    inventario_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inventario.html', inventario_db=inventario_db)

# ------------------------------
# Ventas
# ------------------------------
@app.route('/ventas')
def ver_ventas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('ventas.html', ventas=ventas)

@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    producto = request.form.get('producto')
    cantidad = request.form.get('cantidad')

    try:
        cantidad = int(cantidad)
    except ValueError:
        flash("Cantidad inválida", "danger")
        return redirect(url_for('productos'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad, precio FROM productos WHERE nombre=%s", (producto,))
    result = cursor.fetchone()
    if not result:
        flash("Producto no encontrado", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))

    stock, precio_unitario = result
    if cantidad > stock:
        flash("Cantidad insuficiente en inventario", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))

    total = precio_unitario * cantidad
    hoy = date.today()

    cursor.execute(
        "INSERT INTO ventas (producto, cantidad, total, fecha) VALUES (%s, %s, %s, %s)",
        (producto, cantidad, total, hoy)
    )
    cursor.execute(
        "UPDATE productos SET cantidad = cantidad - %s WHERE nombre = %s",
        (cantidad, producto)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Venta registrada correctamente", "success")
    return redirect(url_for('ver_ventas'))

# ------------------------------
# Reporte de Ventas
# ------------------------------
@app.route('/reporte')
def reporte():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reporte.html', ventas=ventas)

# ------------------------------
# Inicialización
# ------------------------------
if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)
