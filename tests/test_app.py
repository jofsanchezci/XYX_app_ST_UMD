import sys
import os
import pytest
import redis
from app import app, r, get_inventory, update_inventory, record_sale

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Configuración de la base de datos de pruebas
            r.flushdb()  # Limpia la base de datos de Redis antes de cada prueba
        yield client

def test_inventory_update(client):
    update_inventory('Laptop', 10, 1000.0)
    inventory = get_inventory()
    assert inventory['Laptop']['quantity'] == 10
    assert inventory['Laptop']['price'] == 1000.0

def test_inventory_update_transaction(client):
    update_inventory('Laptop', 10, 1000.0)
    try:
        with r.pipeline() as pipe:
            pipe.watch('inventory')
            update_inventory('Laptop', -5, 1000.0)
            assert get_inventory()['Laptop']['quantity'] == 5
            # Simulación de fallo para probar la transacción
            raise Exception("Simulated failure")
            pipe.execute()
    except Exception as e:
        pass

    # Verificación de que la cantidad de inventario no ha cambiado debido al fallo
    assert get_inventory()['Laptop']['quantity'] == 10

def test_record_sale(client):
    update_inventory('Laptop', 10, 1000.0)
    record_sale('Laptop', 2, 1200.0, '2024-01-01')
    inventory = get_inventory()
    assert inventory['Laptop']['quantity'] == 8

def test_record_sale_insufficient_inventory(client):
    update_inventory('Laptop', 1, 1000.0)
    try:
        with r.pipeline() as pipe:
            pipe.watch('inventory')
            record_sale('Laptop', 2, 1200.0, '2024-01-01')
            pipe.execute()
    except redis.exceptions.WatchError:
        pass

    # Verificación de que la venta no se realizó debido a inventario insuficiente
    inventory = get_inventory()
    assert inventory['Laptop']['quantity'] == 1

def test_inventory_update_new_product(client):
    update_inventory('Smartphone', 20, 500.0)
    inventory = get_inventory()
    assert 'Smartphone' in inventory
    assert inventory['Smartphone']['quantity'] == 20
    assert inventory['Smartphone']['price'] == 500.0

def test_inventory_update_existing_product(client):
    update_inventory('Laptop', 10, 1000.0)
    update_inventory('Laptop', 5, 1200.0)
    inventory = get_inventory()
    assert inventory['Laptop']['quantity'] == 15
    assert inventory['Laptop']['price'] == 1200.0

def test_record_sale_updates_inventory_correctly(client):
    update_inventory('Tablet', 10, 300.0)
    record_sale('Tablet', 3, 350.0, '2024-01-01')
    inventory = get_inventory()
    assert inventory['Tablet']['quantity'] == 7

def test_price_update_in_inventory(client):
    update_inventory('Laptop', 10, 1000.0)
    update_inventory('Laptop', 0, 1200.0)  # No cambia la cantidad, solo el precio
    inventory = get_inventory()
    assert inventory['Laptop']['price'] == 1200.0
