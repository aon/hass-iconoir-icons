"""Iconoir Icons for Home Assistant.

Registers a frontend module that exposes the Iconoir icon pack under the
`iconoir:` prefix (e.g. `icon: iconoir:sofa`). Frontend-only integration:
no entities, no polling.
"""
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation
from homeassistant.loader import async_get_integration

DOMAIN = "iconoir_icons"
FRONTEND_SCRIPT_URL = f"/{DOMAIN}/main.js"

CONFIG_SCHEMA = config_validation.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Serve the iconset module and register it as a frontend resource."""
    if DOMAIN not in hass.data:
        # aiohttp routes cannot be unregistered, so this survives reloads.
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    FRONTEND_SCRIPT_URL,
                    str(Path(__file__).parent / "data" / "main.js"),
                    True,
                )
            ]
        )
    # Version the URL so the long-lived static cache busts on updates.
    integration = await async_get_integration(hass, DOMAIN)
    url = f"{FRONTEND_SCRIPT_URL}?v={integration.version}"
    hass.data[DOMAIN] = url
    add_extra_js_url(hass, url)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Stop injecting the module into new frontend loads."""
    if url := hass.data.get(DOMAIN):
        remove_extra_js_url(hass, url)
    return True
