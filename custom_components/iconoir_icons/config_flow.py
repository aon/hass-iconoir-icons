"""Config flow for Iconoir Icons (single instance, no options)."""
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from . import DOMAIN


class IconoirIconsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Trivial flow: single instance is enforced by the manifest."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        return self.async_create_entry(title="Iconoir Icons", data={})
