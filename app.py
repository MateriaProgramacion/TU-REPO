import stripe
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Clave secreta de Stripe (usa la clave de pruebas)
stripe.api_key = "sk_test_51RBRkw09LYEO8dot3czGI8R8zKn8TvLGuzdv7e2yxt4YjZ7ttIMQMZTRqE2y2CueATMFcskTYxbWh6KfeyIVIMns00eMI8mnGB"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Producto de prueba"},
                        "unit_amount": 1000,  # Precio en centavos (10.00 USD)
                    },
                    "quantity": 1,
                }
            ],
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

if __name__ == "__main__":
    app.run(debug=True)




