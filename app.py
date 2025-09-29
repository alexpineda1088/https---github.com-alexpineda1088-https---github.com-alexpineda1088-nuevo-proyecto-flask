from flask import Flask, render_template, request, redirect, url_for, flash, session
from Conexion.conexion import get_connection
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

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
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    cantidad INT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    producto VARCHAR(50) NOT NULL,
                    cantidad INT NOT NULL,
                    total DECIMAL(10,2) NOT NULL,
                    fecha DATE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    mail VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """)
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
        conn.close()

# ------------------------------
# Ruta de prueba de conexión
# ------------------------------
@app.route('/test_db')
def test_db():
    conn = get_connection()
    if conn:
        conn.close()
        return "✅ Conexión exitosa a la base de datos"
    else:
        return "❌ Error de conexión"

# ------------------------------
# Página principal
# ------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# ------------------------------
# Contacto
# ------------------------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        # Aquí podrías guardar el mensaje en la DB o enviarlo por correo
        flash("¡Mensaje enviado correctamente!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ------------------------------
# Autenticación
# ------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('password')

        conn = get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (mail,))
            usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session['usuario'] = usuario['nombre']
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('index'))
        else:
            flash("Credenciales incorrectas", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('index'))

# ------------------------------
# Usuarios
# ------------------------------
@app.route('/usuarios')
def listar_usuarios():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id_usuario, nombre, mail FROM usuarios")
        usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        mail = request.form.get('mail')
        password = generate_password_hash("temporal123")

        if not nombre or not mail:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('agregar_usuario'))

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
                    (nombre, mail, password)
                )
            conn.commit()
            flash("Usuario agregado correctamente", "success")
            return redirect(url_for('listar_usuarios'))
        except Exception as e:
            flash(f"Error al agregar usuario: {e}", "danger")
            return redirect(url_for('agregar_usuario'))
        finally:
            conn.close()

    return render_template('usuario_form.html', usuario=None)

@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
        usuario = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        mail = request.form.get('mail')

        if not nombre or not mail:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('editar_usuario', id=id))

        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, mail=%s WHERE id_usuario=%s",
                (nombre, mail, id)
            )
        conn.commit()
        conn.close()
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for('listar_usuarios'))

    conn.close()
    return render_template('usuario_form.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conn.commit()
    conn.close()
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('listar_usuarios'))

# ------------------------------
# Productos
# ------------------------------
@app.route('/productos')
def productos():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM productos")
        productos_db = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos_db=productos_db)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')

        if not all([nombre, cantidad, precio]):
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('agregar'))

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            flash("Cantidad y precio deben ser numéricos", "danger")
            return redirect(url_for('agregar'))

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                (nombre, cantidad, precio)
            )
        conn.commit()
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
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT nombre, cantidad FROM productos")
        inventario_db = cursor.fetchall()
    conn.close()
    return render_template('inventario.html', inventario_db=inventario_db)

# ------------------------------
# Ventas
# ------------------------------
@app.route('/ventas')
def ver_ventas():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM ventas")
        ventas = cursor.fetchall()
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
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cantidad, precio FROM productos WHERE nombre=%s", (producto,))
            result = cursor.fetchone()
            if not result:
                flash("Producto no encontrado", "danger")
                return redirect(url_for('productos'))

            stock, precio_unitario = result

            if cantidad > stock:
                flash("Cantidad insuficiente en inventario", "danger")
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
        flash("Venta registrada correctamente", "success")
        return redirect(url_for('ver_ventas'))

    except Exception as e:
        flash(f"Error al registrar la venta: {e}", "danger")
        return redirect(url_for('productos'))

    finally:
        conn.close()

# ------------------------------
# Reporte de Ventas
# ------------------------------
@app.route('/reporte')
def reporte():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT producto, SUM(cantidad) as total_cantidad, SUM(total) as total_ventas
            FROM ventas
            GROUP BY producto
        """)
        reporte_db = cursor.fetchall()
    conn.close()
    return render_template('reporte.html', reporte_db=reporte_db)

# ------------------------------
# Ejecutar la app
# ------------------------------
if __name__ == "__main__":
    inicializar_db()
    app.run(debug=True)
