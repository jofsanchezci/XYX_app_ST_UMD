from flask import Flask, request, render_template, redirect, url_for, flash
import redis
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Funciones de gestión de inventario
def get_inventory():
    inventory = r.hgetall('inventory')
    return {k: json.loads(v) for k, v in inventory.items()}

def update_inventory(product, quantity, price):
    inventory = get_inventory()
    if product in inventory:
        inventory[product]['quantity'] += quantity
        inventory[product]['price'] = price
    else:
        inventory[product] = {'quantity': quantity, 'price': price}
    r.hset('inventory', product, json.dumps(inventory[product]))

# Funciones de gestión de ventas
def record_sale(product, quantity, price, date):
    sale_id = r.incr('sale_id')
    sale = {'product': product, 'quantity': quantity, 'price': price, 'date': date}
    r.hset('sales', sale_id, json.dumps(sale))
    inventory = get_inventory()
    inventory[product]['quantity'] -= quantity
    r.hset('inventory', product, json.dumps(inventory[product]))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        product = request.form['product']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        date = request.form['date']
        
        try:
            with r.pipeline() as pipe:
                pipe.watch('inventory')
                inventory = get_inventory()
                if product not in inventory or inventory[product]['quantity'] < quantity:
                    flash('Error: No hay suficiente inventario o el producto no existe.', 'error')
                    return redirect(url_for('sales'))
                
                record_sale(product, quantity, price, date)
                pipe.execute()
                flash('Venta registrada exitosamente.', 'success')
        except redis.exceptions.WatchError:
            flash('Error: La transacción falló, por favor intente nuevamente.', 'error')
        
        return redirect(url_for('sales'))
    
    inventory = get_inventory()
    return render_template('sales.html', inventory=inventory)

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        product = request.form['product']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        
        try:
            with r.pipeline() as pipe:
                pipe.watch('inventory')
                update_inventory(product, quantity, price)
                pipe.execute()
                flash('Inventario actualizado exitosamente.', 'success')
        except redis.exceptions.WatchError:
            flash('Error: La transacción falló, por favor intente nuevamente.', 'error')
        
        return redirect(url_for('inventory'))
    
    inventory = get_inventory()
    return render_template('inventory.html', inventory=inventory)

if __name__ == '__main__':
    app.run(debug=True)
