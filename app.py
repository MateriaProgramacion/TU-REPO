import stripe
from flask import Flask, render_template, redirect, request, url_for, jsonify

app = Flask(__name__)

# Configura tu clave secreta de Stripe
stripe.api_key = "sk_test_51RBRkw09LYEO8dot3czGI8R8zKn8TvLGuzdv7e2yxt4YjZ7ttIMQMZTRqE2y2CueATMFcskTYxbWh6KfeyIVIMns00eMI8mnGB"

# Lista de productos con las imágenes
productos = [
    {'id': 1, 'nombre': 'Producto 1', 'precio': 100, 'imagen': 'images/producto1.jpg'},
    {'id': 2, 'nombre': 'Producto 2', 'precio': 200, 'imagen': 'images/producto2.jpg'},
    {'id': 3, 'nombre': 'Producto 3', 'precio': 300, 'imagen': 'images/producto3.jpg'},
]

# Página de inicio con lista de productos
@app.route("/")
def home():
    return render_template("index.html", productos=productos)

# Página individual de cada producto
@app.route("/producto/<int:id>")
def producto(id):
    producto = next((p for p in productos if p['id'] == id), None)
    if producto is None:
        return "Producto no encontrado", 404
    return render_template("producto.html", producto=producto)

# Ruta para procesar la compra
@app.route("/comprar", methods=["POST"])
def comprar():
    producto_id = int(request.form['producto_id'])
    metodo_pago = request.form['metodo_pago']
    producto = next((p for p in productos if p['id'] == producto_id), None)
    
    if producto is None:
        return "Producto no encontrado", 404
    
    # Configura el método de pago dependiendo de la elección del usuario
    if metodo_pago == 'tarjeta':
        payment_method_types = ['card']
    elif metodo_pago == 'oxxo':
        payment_method_types = ['oxxo']

    # Crear una sesión de pago con Stripe
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=payment_method_types,
            line_items=[{
                "price_data": {
                    "currency": "mxn",
                    "product_data": {"name": producto['nombre']},
                    "unit_amount": producto['precio'] * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for('exito', _external=True),
            cancel_url=url_for('cancelado', _external=True),
        )
        # Redirigir al checkout de Stripe
        return redirect(session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 500

# Ruta para la página de éxito
@app.route('/exito')
def exito():
    return "<h2>¡Compra realizada con éxito!</h2><br><a href='/'>Volver al catálogo</a>"

# Ruta para la página de cancelación
@app.route('/cancelado')
def cancelado():
    return "<h2>La compra ha sido cancelada.</h2><br><a href='/'>Volver al catálogo</a>"

def obtener_producto_por_id(id):
    # Función de ejemplo para obtener un producto desde una base de datos o lista
    return next((producto for producto in productos if producto['id'] == id), None)




