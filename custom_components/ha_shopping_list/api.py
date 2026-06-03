"""API views for HA Shopping List."""
import logging
from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ShoppingListPanelView(HomeAssistantView):
    """View to serve the shopping list panel."""

    url = f"/api/{DOMAIN}/panel"
    name = f"api:{DOMAIN}:panel"
    requires_auth = False

    async def get(self, request):
        """Serve the panel HTML."""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>HA Shopping List</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--primary-font-family, 'Roboto', sans-serif);
            background-color: var(--card-background-color, #fff);
            color: var(--primary-text-color, #212121);
            padding: 16px;
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--divider-color, #e0e0e0);
        }

        h1 {
            font-size: 24px;
            font-weight: 500;
            color: var(--primary-text-color, #212121);
        }

        .button {
            background-color: var(--primary-color, #03a9f4);
            color: var(--text-primary-color, #fff);
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: background-color 0.3s;
        }

        .button:hover {
            opacity: 0.9;
        }

        .button-secondary {
            background-color: var(--secondary-background-color, #f5f5f5);
            color: var(--primary-text-color, #212121);
        }

        .button-danger {
            background-color: var(--error-color, #f44336);
            color: var(--text-primary-color, #fff);
        }

        .add-item-form {
            background-color: var(--primary-background-color, #fafafa);
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .form-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        input, select {
            flex: 1;
            padding: 10px;
            border: 1px solid var(--divider-color, #e0e0e0);
            border-radius: 4px;
            background-color: var(--card-background-color, #fff);
            color: var(--primary-text-color, #212121);
            font-size: 14px;
        }

        input[type="text"] {
            flex: 2;
        }

        .category-section {
            margin-bottom: 24px;
        }

        .category-header {
            font-size: 18px;
            font-weight: 500;
            color: var(--primary-color, #03a9f4);
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }

        .item {
            display: flex;
            align-items: center;
            padding: 12px;
            background-color: var(--card-background-color, #fff);
            border: 1px solid var(--divider-color, #e0e0e0);
            border-radius: 4px;
            margin-bottom: 8px;
            transition: all 0.3s;
        }

        .item.in-cart {
            opacity: 0.6;
            text-decoration: line-through;
        }

        .item input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 12px;
            cursor: pointer;
        }

        .item-content {
            flex: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .item-name {
            font-size: 16px;
            font-weight: 400;
        }

        .item-details {
            display: flex;
            gap: 16px;
            font-size: 14px;
            color: var(--secondary-text-color, #757575);
        }

        .item-quantity {
            font-weight: 500;
        }

        .delete-btn {
            background: none;
            border: none;
            color: var(--error-color, #f44336);
            cursor: pointer;
            padding: 4px 8px;
            font-size: 18px;
        }

        .cart-section {
            margin-top: 32px;
            padding-top: 24px;
            border-top: 2px solid var(--divider-color, #e0e0e0);
        }

        .checkout-section {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 16px;
            padding: 16px;
            background-color: var(--primary-background-color, #fafafa);
            border-radius: 8px;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background-color: var(--card-background-color, #fff);
            padding: 24px;
            border-radius: 8px;
            max-width: 400px;
            width: 90%;
        }

        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 20px;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--secondary-text-color, #757575);
        }

        .nav-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border: none;
            border-bottom: 3px solid transparent;
            background: none;
            color: var(--primary-text-color, #212121);
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }

        .tab.active {
            border-bottom-color: var(--primary-color, #03a9f4);
            font-weight: 500;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>HA Shopping List</h1>
    </div>

    <div class="nav-tabs">
        <button class="tab active" onclick="switchTab('shopping')">Shopping List</button>
        <button class="tab" onclick="switchTab('recipes')">Recipes</button>
    </div>

    <div id="shopping-tab" class="tab-content active">
        <div class="add-item-form">
            <div class="form-row">
                <input type="text" id="item-name" placeholder="Item name" />
                <input type="text" id="item-quantity" placeholder="Qty (e.g., 2, 5L)" value="1" />
                <input type="text" id="item-category" placeholder="Category" value="Uncategorized" />
            </div>
            <button class="button" onclick="addItem()">Add Item</button>
        </div>

        <div id="shopping-list"></div>

        <div class="cart-section">
            <div class="category-header">In Cart</div>
            <div id="cart-items"></div>
            <div class="checkout-section" id="checkout-section" style="display: none;">
                <span id="cart-count">0 items in cart</span>
                <button class="button button-danger" onclick="showCheckoutModal()">Checkout</button>
            </div>
        </div>
    </div>

    <div id="recipes-tab" class="tab-content">
        <button class="button" onclick="showAddRecipeModal()" style="margin-bottom: 20px;">Add New Recipe</button>
        <div id="recipes-list"></div>
    </div>

    <!-- Checkout Confirmation Modal -->
    <div id="checkout-modal" class="modal">
        <div class="modal-content">
            <h2>Confirm Checkout</h2>
            <p>Are you sure you want to remove all items in cart?</p>
            <div class="modal-buttons">
                <button class="button button-secondary" onclick="hideCheckoutModal()">Cancel</button>
                <button class="button button-danger" onclick="checkout()">Checkout</button>
            </div>
        </div>
    </div>

    <!-- Add Recipe Modal -->
    <div id="add-recipe-modal" class="modal">
        <div class="modal-content">
            <h2>Add New Recipe</h2>
            <input type="text" id="recipe-name" placeholder="Recipe name" style="width: 100%; margin-bottom: 16px;" />
            <div id="recipe-ingredients">
                <div class="form-row">
                    <input type="text" class="ingredient-name" placeholder="Ingredient" />
                    <input type="text" class="ingredient-quantity" placeholder="Qty" value="1" />
                    <input type="text" class="ingredient-category" placeholder="Category" value="Uncategorized" />
                </div>
            </div>
            <button class="button button-secondary" onclick="addIngredientField()" style="margin-top: 10px;">+ Add Ingredient</button>
            <div class="modal-buttons">
                <button class="button button-secondary" onclick="hideAddRecipeModal()">Cancel</button>
                <button class="button" onclick="saveRecipe()">Save Recipe</button>
            </div>
        </div>
    </div>

    <script>
        let items = {};
        let recipes = [];
        let hassConnection = null;

        // Connect to Home Assistant WebSocket
        async function connectToHass() {
            try {
                const auth = await window.parent.hassConnection.conn;
                hassConnection = auth;
                
                // Subscribe to events
                hassConnection.subscribeEvents((event) => {
                    if (event.event_type === 'ha_shopping_list_updated') {
                        loadItems();
                    } else if (event.event_type === 'ha_shopping_list_recipe_updated') {
                        loadRecipes();
                    }
                }, 'ha_shopping_list_updated');
                
                hassConnection.subscribeEvents((event) => {
                    if (event.event_type === 'ha_shopping_list_recipe_updated') {
                        loadRecipes();
                    }
                }, 'ha_shopping_list_recipe_updated');
                
            } catch (error) {
                console.error('Failed to connect to Home Assistant:', error);
            }
            
            loadItems();
            loadRecipes();
        }

        async function callService(service, data = {}) {
            try {
                const response = await fetch('/api/services/ha_shopping_list/' + service, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error('Service call failed');
                }
                
                return await response.json();
            } catch (error) {
                console.error('Service call error:', error);
                throw error;
            }
        }

        async function loadItems() {
            try {
                const response = await fetch('/api/ha_shopping_list/items');
                const data = await response.json();
                items = data;
                renderItems();
            } catch (error) {
                console.error('Failed to load items:', error);
            }
        }

        async function loadRecipes() {
            try {
                const response = await fetch('/api/ha_shopping_list/recipes');
                const data = await response.json();
                recipes = data;
                renderRecipes();
            } catch (error) {
                console.error('Failed to load recipes:', error);
            }
        }

        async function addItem() {
            const name = document.getElementById('item-name').value.trim();
            const quantity = document.getElementById('item-quantity').value.trim();
            const category = document.getElementById('item-category').value.trim();

            if (!name) {
                alert('Please enter an item name');
                return;
            }

            await callService('add_item', { name, quantity, category });
            
            document.getElementById('item-name').value = '';
            document.getElementById('item-quantity').value = '1';
            document.getElementById('item-category').value = 'Uncategorized';
            
            loadItems();
        }

        async function toggleItem(itemId) {
            await callService('toggle_item', { id: itemId });
            loadItems();
        }

        async function removeItem(itemId) {
            await callService('remove_item', { id: itemId });
            loadItems();
        }

        function renderItems() {
            const listContainer = document.getElementById('shopping-list');
            const cartContainer = document.getElementById('cart-items');
            const checkoutSection = document.getElementById('checkout-section');
            
            listContainer.innerHTML = '';
            cartContainer.innerHTML = '';

            // Render active items by category
            const active = items.active || {};
            if (Object.keys(active).length === 0) {
                listContainer.innerHTML = '<div class="empty-state">No items in your shopping list</div>';
            } else {
                for (const [category, categoryItems] of Object.entries(active)) {
                    const section = document.createElement('div');
                    section.className = 'category-section';
                    section.innerHTML = `<div class="category-header">${category}</div>`;
                    
                    categoryItems.forEach(item => {
                        section.innerHTML += renderItem(item);
                    });
                    
                    listContainer.appendChild(section);
                }
            }

            // Render cart items
            const cart = items.cart || [];
            if (cart.length === 0) {
                cartContainer.innerHTML = '<div class="empty-state">No items in cart</div>';
                checkoutSection.style.display = 'none';
            } else {
                cart.forEach(item => {
                    cartContainer.innerHTML += renderItem(item);
                });
                document.getElementById('cart-count').textContent = `${cart.length} item${cart.length !== 1 ? 's' : ''} in cart`;
                checkoutSection.style.display = 'flex';
            }
        }

        function renderItem(item) {
            return `
                <div class="item ${item.in_cart ? 'in-cart' : ''}">
                    <input type="checkbox" ${item.in_cart ? 'checked' : ''} onchange="toggleItem('${item.id}')">
                    <div class="item-content">
                        <span class="item-name">${item.name}</span>
                        <div class="item-details">
                            <span class="item-quantity">${item.quantity}</span>
                            <span>${item.category}</span>
                        </div>
                    </div>
                    <button class="delete-btn" onclick="removeItem('${item.id}')">×</button>
                </div>
            `;
        }

        function showCheckoutModal() {
            document.getElementById('checkout-modal').classList.add('active');
        }

        function hideCheckoutModal() {
            document.getElementById('checkout-modal').classList.remove('active');
        }

        async function checkout() {
            await callService('checkout');
            hideCheckoutModal();
            loadItems();
        }

        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            if (tab === 'shopping') {
                document.querySelector('.tab:first-child').classList.add('active');
                document.getElementById('shopping-tab').classList.add('active');
            } else {
                document.querySelector('.tab:last-child').classList.add('active');
                document.getElementById('recipes-tab').classList.add('active');
            }
        }

        function renderRecipes() {
            const container = document.getElementById('recipes-list');
            
            if (recipes.length === 0) {
                container.innerHTML = '<div class="empty-state">No recipes yet. Create your first recipe!</div>';
                return;
            }

            container.innerHTML = recipes.map(recipe => `
                <div class="item">
                    <div class="item-content">
                        <span class="item-name">${recipe.name}</span>
                        <span style="color: var(--secondary-text-color);">${recipe.ingredients.length} ingredients</span>
                    </div>
                    <button class="button button-secondary" onclick="addRecipeToList('${recipe.id}')" style="margin-right: 10px;">Add to List</button>
                    <button class="delete-btn" onclick="deleteRecipe('${recipe.id}')">×</button>
                </div>
            `).join('');
        }

        function showAddRecipeModal() {
            document.getElementById('recipe-name').value = '';
            document.getElementById('recipe-ingredients').innerHTML = `
                <div class="form-row">
                    <input type="text" class="ingredient-name" placeholder="Ingredient" />
                    <input type="text" class="ingredient-quantity" placeholder="Qty" value="1" />
                    <input type="text" class="ingredient-category" placeholder="Category" value="Uncategorized" />
                </div>
            `;
            document.getElementById('add-recipe-modal').classList.add('active');
        }

        function hideAddRecipeModal() {
            document.getElementById('add-recipe-modal').classList.remove('active');
        }

        function addIngredientField() {
            const container = document.getElementById('recipe-ingredients');
            const newField = document.createElement('div');
            newField.className = 'form-row';
            newField.innerHTML = `
                <input type="text" class="ingredient-name" placeholder="Ingredient" />
                <input type="text" class="ingredient-quantity" placeholder="Qty" value="1" />
                <input type="text" class="ingredient-category" placeholder="Category" value="Uncategorized" />
            `;
            container.appendChild(newField);
        }

        async function saveRecipe() {
            const name = document.getElementById('recipe-name').value.trim();
            if (!name) {
                alert('Please enter a recipe name');
                return;
            }

            const ingredientRows = document.querySelectorAll('#recipe-ingredients .form-row');
            const ingredients = [];
            
            ingredientRows.forEach(row => {
                const ingredientName = row.querySelector('.ingredient-name').value.trim();
                if (ingredientName) {
                    ingredients.push({
                        name: ingredientName,
                        quantity: row.querySelector('.ingredient-quantity').value.trim(),
                        category: row.querySelector('.ingredient-category').value.trim()
                    });
                }
            });

            if (ingredients.length === 0) {
                alert('Please add at least one ingredient');
                return;
            }

            try {
                const response = await fetch('/api/ha_shopping_list/recipes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, ingredients })
                });

                if (response.ok) {
                    hideAddRecipeModal();
                    loadRecipes();
                }
            } catch (error) {
                console.error('Failed to save recipe:', error);
            }
        }

        async function deleteRecipe(recipeId) {
            if (!confirm('Are you sure you want to delete this recipe?')) {
                return;
            }

            try {
                const response = await fetch(`/api/ha_shopping_list/recipes/${recipeId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    loadRecipes();
                }
            } catch (error) {
                console.error('Failed to delete recipe:', error);
            }
        }

        async function addRecipeToList(recipeId) {
            await callService('add_recipe', { recipe_id: recipeId });
            switchTab('shopping');
            loadItems();
        }

        // Initialize on load
        connectToHass();
    </script>
</body>
</html>
        """
        return web.Response(text=html_content, content_type="text/html")


class ShoppingListAPIView(HomeAssistantView):
    """API view for shopping list operations."""

    url = "/api/ha_shopping_list/items"
    name = "api:ha_shopping_list:items"
    requires_auth = True

    def __init__(self, hass: HomeAssistant):
        """Initialize the view."""
        self.hass = hass

    async def get(self, request):
        """Get all shopping list items."""
        shopping_list = self.hass.data[DOMAIN]["shopping_list"]
        items = shopping_list.get_items()
        return web.json_response(items)


class RecipesAPIView(HomeAssistantView):
    """API view for recipe operations."""

    url = "/api/ha_shopping_list/recipes"
    name = "api:ha_shopping_list:recipes"
    requires_auth = True

    def __init__(self, hass: HomeAssistant):
        """Initialize the view."""
        self.hass = hass

    async def get(self, request):
        """Get all recipes."""
        recipe_manager = self.hass.data[DOMAIN]["recipe_manager"]
        recipes = recipe_manager.get_all_recipes()
        return web.json_response(recipes)

    async def post(self, request):
        """Create a new recipe."""
        data = await request.json()
        recipe_manager = self.hass.data[DOMAIN]["recipe_manager"]
        recipe = await recipe_manager.async_add_recipe(
            data.get("name"),
            data.get("ingredients", [])
        )
        return web.json_response(recipe)


class RecipeDetailAPIView(HomeAssistantView):
    """API view for individual recipe operations."""

    url = "/api/ha_shopping_list/recipes/{recipe_id}"
    name = "api:ha_shopping_list:recipe_detail"
    requires_auth = True

    def __init__(self, hass: HomeAssistant):
        """Initialize the view."""
        self.hass = hass

    async def delete(self, request, recipe_id):
        """Delete a recipe."""
        recipe_manager = self.hass.data[DOMAIN]["recipe_manager"]
        await recipe_manager.async_remove_recipe(recipe_id)
        return web.Response(status=204)


async def async_setup_views(hass: HomeAssistant):
    """Set up the API views."""
    hass.http.register_view(ShoppingListPanelView())
    hass.http.register_view(ShoppingListAPIView(hass))
    hass.http.register_view(RecipesAPIView(hass))
    hass.http.register_view(RecipeDetailAPIView(hass))
