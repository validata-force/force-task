import json
import pytest
from bank_app.app import create_app
from bank_app.db.models import db, Bank

@pytest.fixture
def app():
    """testings"""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        test_banks = [
            Bank(name='Test Bank 1', location='Test Location 1'),
            Bank(name='Test Bank 2', location='Test Location 2')
        ]
        db.session.add_all(test_banks)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Bank 1' in response.data
    assert b'Test Bank 2' in response.data

def test_bank_detail_page(client, app):
    with app.app_context():
        bank = Bank.query.filter_by(name='Test Bank 1').first()
    response = client.get(f'/bank/{bank.id}')
    assert response.status_code == 200
    assert b'Test Bank 1' in response.data
    assert b'Test Location 1' in response.data

def test_create_bank(client):
    response = client.post('/bank/new', data={
        'name': 'New Test Bank',
        'location': 'New Test Location'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Test Bank' in response.data
    assert b'Bank added successfully' in response.data

def test_update_bank(client, app):
    with app.app_context():
        bank = Bank.query.filter_by(name='Test Bank 1').first()
    response = client.post(f'/bank/{bank.id}/edit', data={
        'name': 'Updated Test Bank',
        'location': 'Updated Test Location'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Test Bank' in response.data
    assert b'Bank updated successfully' in response.data

def test_delete_bank(client, app):
    with app.app_context():
        bank = Bank.query.filter_by(name='Test Bank 1').first()
    response = client.post(f'/bank/{bank.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Bank deleted successfully' in response.data
    assert b'Test Bank 1' not in response.data

def test_get_banks_api(client):
    response = client.get('/api/banks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == 'Test Bank 1'
    assert data[1]['name'] == 'Test Bank 2'

def test_get_bank_api(client, app):
    with app.app_context():
        bank = Bank.query.filter_by(name='Test Bank 1').first()
    response = client.get(f'/api/banks/{bank.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Bank 1'
    assert data['location'] == 'Test Location 1'

def test_create_bank_api(client):
    response = client.post('/api/banks',
                          data=json.dumps({
                              'name': 'API Test Bank',
                              'location': 'API Test Location'
                          }),
                          content_type='application/json')
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['name'] == 'API Test Bank'
    assert data['location'] == 'API Test Location'
    
    response = client.get('/api/banks')
    data = json.loads(response.data)
    assert len(data) == 3
    assert any(bank['name'] == 'API Test Bank' for bank in data)

def test_update_bank_api(client, app):
    with app.app_context():
        bank = Bank.query.filter_by(name='Test Bank 1').first()
        
    response = client.put(f'/api/banks/{bank.id}',
                         data=json.dumps({
                             'name': 'Updated API Bank',
                             'location': 'Updated API Location'
                         }),
                         content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['name'] == 'Updated API Bank'
    assert data['location'] == 'Updated API Location'

def test_delete_bank_api(client, app):
    with app.app_context():
        bank = Bank.query.filter_by(name='Test Bank 1').first()
        
    response = client.delete(f'/api/banks/{bank.id}')
    assert response.status_code == 200
    
    response = client.get('/api/banks')
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Bank 2'
