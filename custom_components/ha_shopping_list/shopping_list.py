"""Shopping list manager for HA Shopping List."""
import uuid
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY_SHOPPING, STORAGE_VERSION


class ShoppingListManager:
    """Manage shopping list data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the shopping list manager."""
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY_SHOPPING)
        self._items: dict[str, dict[str, Any]] = {}

    async def async_load(self) -> None:
        """Load shopping list from storage."""
        data = await self._store.async_load()
        if data:
            self._items = data.get("items", {})
        else:
            self._items = {}

    async def async_save(self) -> None:
        """Save shopping list to storage."""
        await self._store.async_save({"items": self._items})

    async def async_add_item(
        self, name: str, category: str = "Uncategorized", quantity: str = "1"
    ) -> dict[str, Any]:
        """Add an item to the shopping list."""
        item_id = str(uuid.uuid4())
        item = {
            "id": item_id,
            "name": name,
            "category": category,
            "quantity": quantity,
            "in_cart": False,
            "created_at": datetime.now().isoformat(),
        }
        self._items[item_id] = item
        await self.async_save()
        self.hass.bus.async_fire(
            "ha_shopping_list_updated", {"action": "add", "item": item}
        )
        return item

    async def async_toggle_item(self, item_id: str) -> dict[str, Any] | None:
        """Toggle an item's cart status."""
        if item_id not in self._items:
            return None
        
        item = self._items[item_id]
        item["in_cart"] = not item["in_cart"]
        await self.async_save()
        self.hass.bus.async_fire(
            "ha_shopping_list_updated", {"action": "toggle", "item": item}
        )
        return item

    async def async_remove_item(self, item_id: str) -> bool:
        """Remove an item from the shopping list."""
        if item_id in self._items:
            item = self._items.pop(item_id)
            await self.async_save()
            self.hass.bus.async_fire(
                "ha_shopping_list_updated", {"action": "remove", "item": item}
            )
            return True
        return False

    async def async_update_item(
        self, item_id: str, name: str = None, category: str = None, quantity: str = None
    ) -> dict[str, Any] | None:
        """Update an item in the shopping list."""
        if item_id not in self._items:
            return None
        
        item = self._items[item_id]
        if name is not None:
            item["name"] = name
        if category is not None:
            item["category"] = category
        if quantity is not None:
            item["quantity"] = quantity
        
        await self.async_save()
        self.hass.bus.async_fire(
            "ha_shopping_list_updated", {"action": "update", "item": item}
        )
        return item

    async def async_checkout(self) -> list[str]:
        """Remove all items in cart."""
        removed_ids = []
        for item_id, item in list(self._items.items()):
            if item["in_cart"]:
                self._items.pop(item_id)
                removed_ids.append(item_id)
        
        await self.async_save()
        self.hass.bus.async_fire(
            "ha_shopping_list_updated", {"action": "checkout", "removed_ids": removed_ids}
        )
        return removed_ids

    def get_items(self) -> dict[str, dict[str, Any]]:
        """Get all items organized by category."""
        active_items = {}
        cart_items = {}
        
        for item_id, item in self._items.items():
            if item["in_cart"]:
                cart_items[item_id] = item
            else:
                active_items[item_id] = item
        
        # Organize active items by category
        organized = {}
        for item_id, item in active_items.items():
            category = item["category"]
            if category not in organized:
                organized[category] = []
            organized[category].append(item)
        
        # Sort categories alphabetically
        sorted_categories = dict(sorted(organized.items()))
        
        return {
            "active": sorted_categories,
            "cart": list(cart_items.values())
        }

    async def async_add_recipe(self, recipe_id: str, recipe_manager) -> list[dict[str, Any]]:
        """Add all items from a recipe to the shopping list."""
        recipe = recipe_manager.get_recipe(recipe_id)
        if not recipe:
            return []
        
        added_items = []
        for ingredient in recipe.get("ingredients", []):
            item = await self.async_add_item(
                ingredient["name"],
                ingredient.get("category", "Uncategorized"),
                ingredient.get("quantity", "1")
            )
            added_items.append(item)
        
        return added_items
