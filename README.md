# HA Shopping List

A comprehensive shopping list app for Home Assistant with recipe management and category organization.

## Features

- 📝 **Shopping List Management**: Add items with custom quantities and categories
- 🏷️ **Category Organization**: Items automatically organized by store aisle/section
- ✅ **Cart Functionality**: Check off items to move them to cart, cross them out, and move to bottom
- 🛒 **Checkout**: Confirm and remove all cart items at once
- 🍳 **Recipe Management**: Create recipes with predefined ingredients, categories, and quantities
- ➕ **Quick Add**: Add entire recipes to your shopping list with one click
- 🎨 **Theme Integration**: Automatically matches your Home Assistant theme

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/mtvProof/HA_ShoppingList` as a repository
6. Select "Integration" as the category
7. Click "Add"
8. Search for "HA Shopping List" in HACS
9. Click "Install"
10. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/mtvProof/HA_ShoppingList/releases)
2. Extract the contents
3. Copy the `custom_components/ha_shopping_list` folder to your Home Assistant's `custom_components` directory
4. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "HA Shopping List"
4. Click to add the integration
5. Restart Home Assistant

## Adding to Dashboard

1. Go to any dashboard
2. Click **Edit Dashboard**
3. Click **+ Add Card**
4. Click **Custom** at the bottom
5. Enter: `custom:ha-shopping-list-card`
6. Click **Save**

The shopping list will now appear as a card on your dashboard!

## Usage

### Adding Items

1. Navigate to the HA Shopping List panel
2. Enter the item name, quantity (e.g., "2", "5L", "300ml"), and category
3. Click "Add Item"

### Managing Items

- **Check/Uncheck**: Toggle items between active list and cart
- **Delete**: Click the × button to remove an item
- **Checkout**: Click "Checkout" button to remove all cart items (with confirmation)

### Recipes

1. Click the "Recipes" tab
2. Click "Add New Recipe"
3. Enter recipe name and add ingredients with quantities and categories
4. Click "Save Recipe"
5. To add a recipe to your shopping list, click "Add to List" next to any recipe

## Services

The integration provides the following services:

- `ha_shopping_list.add_item`: Add an item to the shopping list
- `ha_shopping_list.toggle_item`: Toggle an item's cart status
- `ha_shopping_list.remove_item`: Remove an item
- `ha_shopping_list.checkout`: Remove all cart items
- `ha_shopping_list.add_recipe`: Add all ingredients from a recipe

## Version History

- **1.0.0** - Initial release

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/mtvProof/HA_ShoppingList/issues) on GitHub.

## License

This project is licensed under the MIT License.
