import unittest
import json
from src.app import app
from src.routes.products import _reset_products

class TestProducts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        _reset_products()

    def test_get_products_empty(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['products'], [])

    def test_create_and_get_product(self):
        new_item = {'title': 'Test Product', 'description': 'Test Desc'}
        response = self.app.post('/products', data=json.dumps(new_item), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['product']['title'], 'Test Product')
        item_id = data['product']['id']

        response = self.app.get(f'/products/{item_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['product']['title'], 'Test Product')

    def test_update_product(self):
        new_item = {'title': 'To Update'}
        response = self.app.post('/products', data=json.dumps(new_item), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        item_id = data['product']['id']

        updated_data = {'title': 'Updated Title', 'description': 'Updated Desc'}
        response = self.app.put(f'/products/{item_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get(f'/products/{item_id}')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['product']['title'], 'Updated Title')

    def test_delete_product(self):
        new_item = {'title': 'To Delete'}
        response = self.app.post('/products', data=json.dumps(new_item), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        item_id = data['product']['id']

        response = self.app.delete(f'/products/{item_id}')
        self.assertEqual(response.status_code, 200)

        response = self.app.get(f'/products/{item_id}')
        self.assertEqual(response.status_code, 404)
