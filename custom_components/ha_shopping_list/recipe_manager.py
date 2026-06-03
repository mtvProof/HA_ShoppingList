"""Recipe manager for HA Shopping List."""
import uuid
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY_RECIPES, STORAGE_VERSION


class RecipeManager:
    """Manage recipes."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the recipe manager."""
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY_RECIPES)
        self._recipes: dict[str, dict[str, Any]] = {}

    async def async_load(self) -> None:
        """Load recipes from storage."""
        data = await self._store.async_load()
        if data:
            self._recipes = data.get("recipes", {})
        else:
            self._recipes = {}

    async def async_save(self) -> None:
        """Save recipes to storage."""
        await self._store.async_save({"recipes": self._recipes})

    async def async_add_recipe(
        self, name: str, ingredients: list[dict[str, str]]
    ) -> dict[str, Any]:
        """Add a recipe."""
        recipe_id = str(uuid.uuid4())
        recipe = {
            "id": recipe_id,
            "name": name,
            "ingredients": ingredients,
            "created_at": datetime.now().isoformat(),
        }
        self._recipes[recipe_id] = recipe
        await self.async_save()
        self.hass.bus.async_fire(
            "ha_shopping_list_recipe_updated", {"action": "add", "recipe": recipe}
        )
        return recipe

    async def async_update_recipe(
        self, recipe_id: str, name: str = None, ingredients: list[dict[str, str]] = None
    ) -> dict[str, Any] | None:
        """Update a recipe."""
        if recipe_id not in self._recipes:
            return None
        
        recipe = self._recipes[recipe_id]
        if name is not None:
            recipe["name"] = name
        if ingredients is not None:
            recipe["ingredients"] = ingredients
        
        await self.async_save()
        self.hass.bus.async_fire(
            "ha_shopping_list_recipe_updated", {"action": "update", "recipe": recipe}
        )
        return recipe

    async def async_remove_recipe(self, recipe_id: str) -> bool:
        """Remove a recipe."""
        if recipe_id in self._recipes:
            recipe = self._recipes.pop(recipe_id)
            await self.async_save()
            self.hass.bus.async_fire(
                "ha_shopping_list_recipe_updated", {"action": "remove", "recipe": recipe}
            )
            return True
        return False

    def get_recipe(self, recipe_id: str) -> dict[str, Any] | None:
        """Get a specific recipe."""
        return self._recipes.get(recipe_id)

    def get_all_recipes(self) -> list[dict[str, Any]]:
        """Get all recipes."""
        return list(self._recipes.values())
