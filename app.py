from flask import Flask, render_template

app = Flask(__name__)

# Lista de productos
productos = [
    {"id": 1, "nombre": "Audífonos Bluetooth", "precio": 500},
    {"id": 2, "nombre": "Teclado mecánico", "precio": 1200},
    {"id": 3, "nombre": "Mouse gamer", "precio": 800}
]












@app.route("/")
def home():
    return render_template("index.html", productos=productos)

@app.route("/producto/<int:id>")
def producto(id):
    producto = next((p for p in productos if p["id"] == id), None)
    return render_template("producto.html", producto=producto) if producto else "Producto no encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)



