import stripe
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Clave secreta de Stripe (usa la clave de pruebas)
stripe.api_key = "sk_test_51RBRkw09LYEO8dot3czGI8R8zKn8TvLGuzdv7e2yxt4YjZ7ttIMQMZTRqE2y2CueATMFcskTYxbWh6KfeyIVIMns00eMI8mnGBi"

# Ejemplo de productos
productos = [
    {'id': 1, 'nombre': 'Producto 1', 'precio': 100},
    {'id': 2, 'nombre': 'Producto 2', 'precio': 200},
    {'id': 3, 'nombre': 'Producto 3', 'precio': 300},
]

@app.route("/")
def home():
    return render_template("index.html", productos=productos)

@app.route("/checkout/<int:id>", methods=["POST"])
def checkout(id):
    # Buscar el producto con el id recibido
    producto = next((p for p in productos if p['id'] == id), None)
    if producto is None:
        return jsonify(error="Producto no encontrado"), 404

    try:
        # Crear una sesión de Stripe para el producto seleccionado
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": producto['nombre']},
                    "unit_amount": producto['precio'] * 100,  # Precio en centavos
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://tu-repo.onrender.com/success",
            cancel_url="https://tu-repo.onrender.com/cancel",
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/success")
def success():
    return "¡Pago exitoso!"

@app.route("/cancel")
def cancel():
    return "Pago cancelado"

@app.route("/producto/<int:id>")
def producto(id):
    # Busca el producto por su id
    producto = next((p for p in productos if p['id'] == id), None)
    if producto is None:
        return "Producto no encontrado", 404
    return render_template('producto.html', producto=producto)

if __name__ == "__main__":
    app.run(debug=True)




