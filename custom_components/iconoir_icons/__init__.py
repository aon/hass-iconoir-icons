"""Iconoir Icons for Home Assistant.

Registers a frontend module that exposes the Iconoir icon pack under the
`iconoir:` prefix (e.g. `icon: iconoir:sofa`). Frontend-only integration:
no entities, no polling. The icon stroke width is chosen in the options flow
and passed to the module via a `?w=` query parameter.
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

# Stroke width (px, on a 24-unit viewBox). Each value maps to a pre-generated
# path set bundled in data/main.js; the module serves the set matching ?w=.
CONF_STROKE_WIDTH = "stroke_width"
STROKE_WIDTHS = ["1.0", "1.25", "1.5", "1.75", "2.0"]
DEFAULT_STROKE_WIDTH = "1.5"

CONFIG_SCHEMA = config_validation.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Serve the iconset module and register it as a frontend resource."""
    data = hass.data.setdefault(DOMAIN, {})
    if not data.get("static_registered"):
        # aiohttp routes cannot be unregistered, so register the path once and
        # let it survive reloads.
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    FRONTEND_SCRIPT_URL,
                    str(Path(__file__).parent / "data" / "main.js"),
                    True,
                )
            ]
        )
        data["static_registered"] = True

    integration = await async_get_integration(hass, DOMAIN)
    width = entry.options.get(CONF_STROKE_WIDTH, DEFAULT_STROKE_WIDTH)
    # Version + width in the URL so the long-lived static cache busts on an
    # update or a stroke-width change.
    url = f"{FRONTEND_SCRIPT_URL}?v={integration.version}&w={width}"
    data["url"] = url
    add_extra_js_url(hass, url)

    # Re-inject the module (with the new ?w=) whenever the options change.
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload so the stroke-width change takes effect on new frontend loads."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Stop injecting the module into new frontend loads."""
    if url := hass.data.get(DOMAIN, {}).get("url"):
        remove_extra_js_url(hass, url)
    return True
