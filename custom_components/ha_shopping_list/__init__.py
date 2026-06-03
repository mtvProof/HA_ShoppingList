"""HA Shopping List integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .shopping_list import ShoppingListManager
from .recipe_manager import RecipeManager
from .api import async_setup_views

_LOGGER = logging.getLogger(__name__)

PLATFORMS = []


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HA Shopping List component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Shopping List from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize shopping list manager
    shopping_list = ShoppingListManager(hass)
    await shopping_list.async_load()
    hass.data[DOMAIN]["shopping_list"] = shopping_list
    
    # Initialize recipe manager
    recipe_manager = RecipeManager(hass)
    await recipe_manager.async_load()
    hass.data[DOMAIN]["recipe_manager"] = recipe_manager
    
    # Register services
    async def handle_add_item(call):
        """Handle add item service."""
        name = call.data.get("name")
        category = call.data.get("category", "Uncategorized")
        quantity = call.data.get("quantity", "1")
        await shopping_list.async_add_item(name, category, quantity)
    
    async def handle_toggle_item(call):
        """Handle toggle item service."""
        item_id = call.data.get("id")
        await shopping_list.async_toggle_item(item_id)
    
    async def handle_remove_item(call):
        """Handle remove item service."""
        item_id = call.data.get("id")
        await shopping_list.async_remove_item(item_id)
    
    async def handle_checkout(call):
        """Handle checkout service."""
        await shopping_list.async_checkout()
    
    async def handle_add_recipe(call):
        """Handle add recipe service."""
        recipe_id = call.data.get("recipe_id")
        await shopping_list.async_add_recipe(recipe_id, recipe_manager)
    
    hass.services.async_register(DOMAIN, "add_item", handle_add_item)
    hass.services.async_register(DOMAIN, "toggle_item", handle_toggle_item)
    hass.services.async_register(DOMAIN, "remove_item", handle_remove_item)
    hass.services.async_register(DOMAIN, "checkout", handle_checkout)
    hass.services.async_register(DOMAIN, "add_recipe", handle_add_recipe)
    
    # Register API views
    await async_setup_views(hass)
    
    _LOGGER.info("HA Shopping List integration loaded successfully")
    
    # Register the panel (deferred to avoid blocking setup)
    async def register_panel(_):
        """Register the panel when frontend is ready."""
        hass.components.frontend.async_register_built_in_panel(
            "iframe",
            "HA Shopping List",
            "mdi:cart",
            DOMAIN,
            {"url": f"/api/{DOMAIN}/panel"},
            require_admin=False,
        )
    
    hass.bus.async_listen_once("homeassistant_started", register_panel)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].clear()
    return True
