from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <-- Esta línea habilita CORS para todos los endpoints

# Base de datos en memoria
productos = []
contador_id = 1

@app.route('/')
def home():
    return jsonify({'mensaje': 'API de Green Tiendita activa'})

# Crear producto
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    global contador_id
    datos = request.get_json()
    producto = {
        'id': contador_id,
        'nombre': datos.get('nombre'),
        'precio': datos.get('precio'),
        'categoria': datos.get('categoria')
    }
    productos.append(producto)
    contador_id += 1
    return jsonify(producto), 201

# Obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

# Obtener producto por ID
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = next((p for p in productos if p['id'] == id), None)
    return jsonify(producto) if producto else (jsonify({'mensaje': 'Producto no encontrado'}), 404)

# Actualizar producto
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    datos = request.get_json()
    for producto in productos:
        if producto['id'] == id:
            producto['nombre'] = datos.get('nombre', producto['nombre'])
            producto['precio'] = datos.get('precio', producto['precio'])
            producto['categoria'] = datos.get('categoria', producto['categoria'])
            return jsonify(producto)
    return jsonify({'mensaje': 'Producto no encontrado'}), 404

# Eliminar producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    global productos
    productos = [p for p in productos if p['id'] != id]
    return jsonify({'mensaje': f'Producto {id} eliminado'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
