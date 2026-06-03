"""HA Shopping List - Standalone Flask Application"""
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)

@app.after_request
def add_header(response):
    """Add headers to allow iframe embedding."""
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

DATA_FILE = '/data/shopping_list.json'

DEFAULT_CATEGORIES = [
    {'name': 'Produce', 'emoji': '🥬'},
    {'name': 'Dairy', 'emoji': '🥛'},
    {'name': 'Meat', 'emoji': '🥩'},
    {'name': 'Bakery', 'emoji': '🍞'},
    {'name': 'Frozen', 'emoji': '🧊'},
    {'name': 'Pantry', 'emoji': '🥫'},
    {'name': 'Snacks', 'emoji': '🍿'},
    {'name': 'Beverages', 'emoji': '🥤'},
    {'name': 'Household', 'emoji': '🧹'},
    {'name': 'Personal Care', 'emoji': '🧴'},
    {'name': 'Other', 'emoji': '📦'}
]

def load_data():
    """Load data from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure categories and theme exist
            if 'categories' not in data:
                data['categories'] = DEFAULT_CATEGORIES
            if 'theme' not in data:
                data['theme'] = {'mode': 'dark', 'primary': '#2196F3', 'background': '#1e1e1e', 'surface': '#2d2d2d'}
            return data
    return {
        'items': [], 
        'recipes': [], 
        'categories': DEFAULT_CATEGORIES,
        'theme': {'mode': 'dark', 'primary': '#2196F3', 'background': '#1e1e1e', 'surface': '#2d2d2d'}
    }

def save_data(data):
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all shopping list items organized by category."""
    data = load_data()
    items = data.get('items', [])
    
    # Organize items
    active_items = {}
    cart_items = []
    
    for item in items:
        if item['in_cart']:
            cart_items.append(item)
        else:
            category = item['category']
            if category not in active_items:
                active_items[category] = []
            active_items[category].append(item)
    
    # Sort categories alphabetically
    active_items = {k: active_items[k] for k in sorted(active_items.keys())}
    
    return jsonify({
        'active': active_items,
        'cart': cart_items
    })

@app.route('/api/items', methods=['POST'])
def add_item():
    """Add a new item to the shopping list."""
    data = load_data()
    
    item = {
        'id': str(uuid.uuid4()),
        'name': request.json['name'],
        'category': request.json.get('category', 'Uncategorized'),
        'quantity': request.json.get('quantity', '1'),
        'in_cart': False,
        'created_at': datetime.now().isoformat()
    }
    
    data['items'].append(item)
    save_data(data)
    
    return jsonify(item), 201

@app.route('/api/items/<item_id>/toggle', methods=['POST'])
def toggle_item(item_id):
    """Toggle item between active and cart."""
    data = load_data()
    
    for item in data['items']:
        if item['id'] == item_id:
            item['in_cart'] = not item['in_cart']
            save_data(data)
            return jsonify(item)
    
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item from the shopping list."""
    data = load_data()
    data['items'] = [item for item in data['items'] if item['id'] != item_id]
    save_data(data)
    return '', 204

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Remove all items in cart."""
    data = load_data()
    data['items'] = [item for item in data['items'] if not item['in_cart']]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes."""
    data = load_data()
    return jsonify(data.get('recipes', []))

@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    """Add a new recipe."""
    data = load_data()
    
    recipe = {
        'id': str(uuid.uuid4()),
        'name': request.json['name'],
        'ingredients': request.json['ingredients'],
        'created_at': datetime.now().isoformat()
    }
    
    data['recipes'].append(recipe)
    save_data(data)
    
    return jsonify(recipe), 201

@app.route('/api/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get a specific recipe."""
    data = load_data()
    
    for recipe in data.get('recipes', []):
        if recipe['id'] == recipe_id:
            return jsonify(recipe)
    
    return jsonify({'error': 'Recipe not found'}), 404

@app.route('/api/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete a recipe."""
    data = load_data()
    data['recipes'] = [r for r in data.get('recipes', []) if r['id'] != recipe_id]
    save_data(data)
    return '', 204

@app.route('/api/recipes/<recipe_id>/add', methods=['POST'])
def add_recipe_to_list(recipe_id):
    """Add all ingredients from a recipe to the shopping list."""
    data = load_data()
    
    recipe = None
    for r in data.get('recipes', []):
        if r['id'] == recipe_id:
            recipe = r
            break
    
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    
    # Add each ingredient to the shopping list
    for ingredient in recipe['ingredients']:
        item = {
            'id': str(uuid.uuid4()),
            'name': ingredient['name'],
            'category': ingredient.get('category', 'Other'),
            'quantity': ingredient.get('quantity', '1'),
            'in_cart': False,
            'created_at': datetime.now().isoformat()
        }
        data['items'].append(item)
    
    save_data(data)
    return jsonify({'success': True, 'added': len(recipe['ingredients'])})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    data = load_data()
    return jsonify(data.get('categories', DEFAULT_CATEGORIES))

@app.route('/api/categories', methods=['POST'])
def save_categories():
    """Save categories."""
    data = load_data()
    data['categories'] = request.json['categories']
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/theme', methods=['GET'])
def get_theme():
    """Get current theme."""
    data = load_data()
    return jsonify(data.get('theme', {'mode': 'dark', 'primary': '#2196F3', 'background': '#1e1e1e', 'surface': '#2d2d2d'}))

@app.route('/api/theme', methods=['POST'])
def save_theme():
    """Save theme settings."""
    data = load_data()
    data['theme'] = request.json
    save_data(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
