from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint('main', __name__)

# In-memory list to store items
items = []
next_id = 1

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/items')
def list_items():
    return render_template('items.html', items=items)

@main_bp.route('/items/add', methods=['GET', 'POST'])
def add_item():
    global next_id
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name:
            try:
                price_value = float(price) if price else 0.0
            except ValueError:
                price_value = 0.0
            items.append({'id': next_id, 'name': name, 'price': price_value})
            next_id += 1
        return redirect(url_for('main.list_items'))
    return render_template('add_item.html')

@main_bp.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return redirect(url_for('main.list_items'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name:
            item['name'] = name
            try:
                price_value = float(price) if price else 0.0
            except ValueError:
                price_value = 0.0
            item['price'] = price_value
        return redirect(url_for('main.list_items'))
    return render_template('edit_item.html', item=item)

@main_bp.route('/items/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return redirect(url_for('main.list_items'))
