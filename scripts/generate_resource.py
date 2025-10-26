import argparse
import os
import re

def get_route_template(name):
    plural_name = name + 's'
    return f'''from flask import Blueprint, jsonify, request, abort

{name}_bp = Blueprint('{name}', __name__)

{plural_name} = []
next_{name}_id = 1

def _get_next_{name}_id():
    global next_{name}_id
    result = next_{name}_id
    next_{name}_id += 1
    return result

def _reset_{plural_name}():
    global {plural_name}, next_{name}_id
    {plural_name} = []
    next_{name}_id = 1

@{name}_bp.route('/{plural_name}', methods=['GET'])
def get_{plural_name}():
    return jsonify({'{'}'{plural_name}': {plural_name}{'}'})

@{name}_bp.route('/{plural_name}/<int:{name}_id>', methods=['GET'])
def get_{name}({name}_id):
    item = [p for p in {plural_name} if p['id'] == {name}_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'{'}'{name}': item[0]{'}'})

@{name}_bp.route('/{plural_name}', methods=['POST'])
def create_{name}():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {{
        'id': _get_next_{name}_id(),
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }}
    {plural_name}.append(item)
    return jsonify({'{'}'{name}': item{'}'}), 201

@{name}_bp.route('/{plural_name}/<int:{name}_id>', methods=['PUT'])
def update_{name}({name}_id):
    item = [p for p in {plural_name} if p['id'] == {name}_id]
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
    return jsonify({'{'}'{name}': item[0]{'}'})

@{name}_bp.route('/{plural_name}/<int:{name}_id>', methods=['DELETE'])
def delete_{name}({name}_id):
    item = [p for p in {plural_name} if p['id'] == {name}_id]
    if len(item) == 0:
        abort(404)
    {plural_name}.remove(item[0])
    return jsonify({'{'}'result': True{'}'})
'''

def get_test_template(name):
    capitalized_name = name.capitalize()
    plural_name = name + 's'
    return f'''import unittest
import json
from src.app import app
from src.routes.{plural_name} import _reset_{plural_name}

class Test{capitalized_name}s(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        _reset_{plural_name}()

    def test_get_{plural_name}_empty(self):
        response = self.app.get('/{plural_name}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['{plural_name}'], [])

    def test_create_and_get_{name}(self):
        new_item = {{'title': 'Test {capitalized_name}', 'description': 'Test Desc'}}
        response = self.app.post('/{plural_name}', data=json.dumps(new_item), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['{name}']['title'], 'Test {capitalized_name}')
        item_id = data['{name}']['id']

        response = self.app.get(f'/{plural_name}/{{item_id}}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['{name}']['title'], 'Test {capitalized_name}')

    def test_update_{name}(self):
        new_item = {{'title': 'To Update'}}
        response = self.app.post('/{plural_name}', data=json.dumps(new_item), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        item_id = data['{name}']['id']

        updated_data = {{'title': 'Updated Title', 'description': 'Updated Desc'}}
        response = self.app.put(f'/{plural_name}/{{item_id}}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get(f'/{plural_name}/{{item_id}}')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['{name}']['title'], 'Updated Title')

    def test_delete_{name}(self):
        new_item = {{'title': 'To Delete'}}
        response = self.app.post('/{plural_name}', data=json.dumps(new_item), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        item_id = data['{name}']['id']

        response = self.app.delete(f'/{plural_name}/{{item_id}}')
        self.assertEqual(response.status_code, 200)

        response = self.app.get(f'/{plural_name}/{{item_id}}')
        self.assertEqual(response.status_code, 404)
'''

def register_blueprint(resource_name):
    app_py_path = 'src/app.py'
    plural_name = resource_name + 's'
    blueprint_var = f'{resource_name}_bp'
    import_line = f'from src.routes.{plural_name} import {blueprint_var}'
    register_line = f'app.register_blueprint({blueprint_var})'

    with open(app_py_path, 'r+') as f:
        content = f.read()
        if import_line in content:
            print(f"Blueprint '{resource_name}' already imported.")
            return

        # Add the import statement
        content = re.sub(r'(from src\.routes\..*)\n', f'\\1\n{import_line}\n', content, 1)

        # Add the register line
        register_section_match = re.search(r'(# Register Blueprints\n)', content)
        if register_section_match:
            insert_point = register_section_match.end(0)
            content = content[:insert_point] + register_line + '\n' + content[insert_point:]
        else: # Fallback if comment not found
            content = content.replace('app = Flask(__name__)', f'app = Flask(__name__)\n\n{register_line}')

        f.seek(0)
        f.write(content)
        f.truncate()
    print(f"Registered blueprint for '{resource_name}' in 'src/app.py'.")

def main():
    parser = argparse.ArgumentParser(description='Generate a new Flask RESTful resource.')
    parser.add_argument('name', type=str, help='The name of the resource (e.g., product, user).')
    args = parser.parse_args()
    resource_name = args.name.lower()

    print(f"Generating resource: {resource_name}")

    plural_name = resource_name + 's'

    # Create route file
    route_file_path = f'src/routes/{plural_name}.py'
    if os.path.exists(route_file_path):
        print(f"Error: Route file already exists at {route_file_path}")
        return
    with open(route_file_path, 'w') as f:
        f.write(get_route_template(resource_name))
    print(f"Created route file: {route_file_path}")

    # Create test file
    test_file_path = f'tests/test_{plural_name}.py'
    if os.path.exists(test_file_path):
        print(f"Error: Test file already exists at {test_file_path}")
        return
    with open(test_file_path, 'w') as f:
        f.write(get_test_template(resource_name))
    print(f"Created test file: {test_file_path}")

    # Register the blueprint
    register_blueprint(resource_name)

    print("\\nGeneration complete!")

if __name__ == '__main__':
    main()
