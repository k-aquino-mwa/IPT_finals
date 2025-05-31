import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
import app.routes

@pytest.fixture(autouse=True)
def reset_items():
    app.routes.items.clear()
    app.routes.next_id = 1

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Welcome to Flask Web Template" in rv.data

def test_list_items_empty(client):
    rv = client.get('/items')
    assert rv.status_code == 200
    assert b"No items found." in rv.data or b"Items List" in rv.data

def test_add_item_get(client):
    rv = client.get('/items/add')
    assert rv.status_code == 200
    assert b"Add New Item" in rv.data

def test_add_item_post(client):
    rv = client.post('/items/add', data={'name': 'Test Item'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Test Item" in rv.data

def test_edit_item_get(client):
    # Add item first
    client.post('/items/add', data={'name': 'Edit Item'}, follow_redirects=True)
    rv = client.get('/items/edit/1')
    assert rv.status_code == 200
    assert b"Edit Item" in rv.data

def test_edit_item_post(client):
    # Add item first
    client.post('/items/add', data={'name': 'Old Name'}, follow_redirects=True)
    rv = client.post('/items/edit/1', data={'name': 'New Name'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"New Name" in rv.data

def test_edit_item_invalid_id(client):
    rv = client.get('/items/edit/999')
    # Should redirect to list_items
    assert rv.status_code == 302 or rv.status_code == 302

def test_delete_item_post(client):
    # Add item first
    client.post('/items/add', data={'name': 'Delete Item'}, follow_redirects=True)
    rv = client.post('/items/delete/1', follow_redirects=True)
    assert rv.status_code == 200
    assert b"Delete Item" not in rv.data

def test_delete_item_invalid_id(client):
    rv = client.post('/items/delete/999', follow_redirects=True)
    # Should redirect to list_items without error
    assert rv.status_code == 200

def test_add_item_post_empty_name(client):
    rv = client.post('/items/add', data={'name': ''}, follow_redirects=True)
    # Should redirect to list_items without adding
    assert rv.status_code == 200
    assert b"No items found." in rv.data or b"Items List" in rv.data
