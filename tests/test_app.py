import unittest
import json
from src.app import app, tasks

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Reset tasks before each test
        tasks.clear()
        tasks.extend([
            {'id': 1, 'title': 'Task 1', 'description': 'Description 1', 'done': False},
            {'id': 2, 'title': 'Task 2', 'description': 'Description 2', 'done': False}
        ])

    def test_get_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['tasks']), 2)

    def test_get_task(self):
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['task']['title'], 'Task 1')

    def test_get_task_not_found(self):
        response = self.app.get('/tasks/99')
        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        new_task = {'title': 'Task 3', 'description': 'Description 3'}
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['task']['title'], 'Task 3')
        self.assertEqual(len(tasks), 3)

    def test_create_task_no_title(self):
        new_task = {'description': 'Description 3'}
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_task(self):
        updated_task = {'title': 'Updated Task 1', 'done': True}
        response = self.app.put('/tasks/1', data=json.dumps(updated_task), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['task']['title'], 'Updated Task 1')
        self.assertTrue(data['task']['done'])

    def test_update_task_not_found(self):
        updated_task = {'title': 'Updated Task'}
        response = self.app.put('/tasks/99', data=json.dumps(updated_task), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['result'])
        self.assertEqual(len(tasks), 1)

    def test_delete_task_not_found(self):
        response = self.app.delete('/tasks/99')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
