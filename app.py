import stripe
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Clave secreta de Stripe (usa la clave de pruebas)
stripe.api_key = "sk_test_51RBRkw09LYEO8dot3czGI8R8zKn8TvLGuzdv7e2yxt4YjZ7ttIMQMZTRqE2y2CueATMFcskTYxbWh6KfeyIVIMns00eMI8mnGBi"

# Lista de productos
productos = [
    {'id': 1, 'nombre': 'Producto 1', 'precio': 100},
    {'id': 2, 'nombre': 'Producto 2', 'precio': 200},
    {'id': 3, 'nombre': 'Producto 3', 'precio': 300},
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

# Ruta de compra directa con mensaje (simulada sin Stripe)
@app.route("/comprar", methods=["POST"])
def comprar():
    producto_id = int(request.form['producto_id'])
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        return f"<h2>¡Gracias por comprar {producto['nombre']} por ${producto['precio']}!</h2><br><a href='/'>Volver al catálogo</a>"
    return "Producto no encontrado", 404

# Ruta que crea sesión de pago real con Stripe
@app.route("/checkout/<int:id>", methods=["POST"])
def checkout(id):
    producto = next((p for p in productos if p['id'] == id), None)
    if producto is None:
        return jsonify(error="Producto no encontrado"), 404

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": producto['nombre']},
                    "unit_amount": producto['precio'] * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://tu-repo.onrender.com/success",
            cancel_url="https://tu-repo.onrender.com/cancel",
        )
        print(f"Session URL: {session.url}")
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify(error=str(e)), 500

# Rutas de éxito o cancelación de Stripe
@app.route("/success")
def success():
    return "¡Pago exitoso!"

@app.route("/cancel")
def cancel():
    return "Pago cancelado"

if __name__ == "__main__":
    app.run(debug=True)



