"""Iconoir Icons for Home Assistant.

Registers a frontend module that exposes the Iconoir icon pack under the
`iconoir:` prefix (e.g. `icon: iconoir:sofa`). Frontend-only integration:
no entities, no polling.
"""
import logging

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "iconoir_icons"
SCRIPT_NAME = "main.js"
FRONTEND_SCRIPT_URL = f"/{DOMAIN}/{SCRIPT_NAME}"

CONFIG_SCHEMA = config_validation.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Serve the iconset module and register it as a frontend resource."""
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                FRONTEND_SCRIPT_URL,
                hass.config.path(f"custom_components/{DOMAIN}/data/{SCRIPT_NAME}"),
                True,
            )
        ]
    )
    add_extra_js_url(hass, FRONTEND_SCRIPT_URL)
    return True


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """No-op: setup happens in async_setup; the entry just marks it enabled."""
    return True


async def async_remove_entry(hass: HomeAssistant, entry) -> None:
    """Nothing persistent to clean up."""
    return None
