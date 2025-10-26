import unittest
import json
from src.app import app
from src.routes.tasks import _reset_tasks

class TestTasks(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        _reset_tasks() # Reset tasks before each test

    def test_get_tasks_empty(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['tasks'], [])

    def test_create_and_get_task(self):
        # Create a task
        new_task = {'title': 'A new task', 'description': 'New description'}
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['task']['title'], 'A new task')
        new_task_id = data['task']['id']

        # Get the task
        response = self.app.get(f'/tasks/{new_task_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['task']['title'], 'A new task')

    def test_create_task_no_title(self):
        new_task = {'description': 'Description without title'}
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_task(self):
        # Create a task
        new_task = {'title': 'Task to update'}
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        task_id = data['task']['id']

        # Update the task
        updated_task_data = {'title': 'Updated Title', 'done': True}
        response = self.app.put(f'/tasks/{task_id}', data=json.dumps(updated_task_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = self.app.get(f'/tasks/{task_id}')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['task']['title'], 'Updated Title')
        self.assertTrue(data['task']['done'])

    def test_delete_task(self):
        # Create a task
        new_task = {'title': 'Task to delete'}
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        task_id = data['task']['id']

        # Delete the task
        response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)

        # Verify the deletion
        response = self.app.get(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 404)
