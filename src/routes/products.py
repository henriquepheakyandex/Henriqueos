from flask import Blueprint, jsonify, request, abort

product_bp = Blueprint('product', __name__)

products = []
next_product_id = 1

def _get_next_product_id():
    global next_product_id
    result = next_product_id
    next_product_id += 1
    return result

def _reset_products():
    global products, next_product_id
    products = []
    next_product_id = 1

@product_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products})

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    item = [p for p in products if p['id'] == product_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'product': item[0]})

@product_bp.route('/products', methods=['POST'])
def create_product():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {
        'id': _get_next_product_id(),
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }
    products.append(item)
    return jsonify({'product': item}), 201

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    item = [p for p in products if p['id'] == product_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    item[0]['title'] = request.json.get('title', item[0]['title'])
    item[0]['description'] = request.json.get('description', item[0]['description'])
    return jsonify({'product': item[0]})

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    item = [p for p in products if p['id'] == product_id]
    if len(item) == 0:
        abort(404)
    products.remove(item[0])
    return jsonify({'result': True})
