"""Config flow for Iconoir Icons (single instance, no options)."""
from homeassistant import config_entries


@config_entries.HANDLERS.register("iconoir_icons")
class IconoirIconsConfigFlow(config_entries.ConfigFlow):
    """Single-instance config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="Iconoir Icons", data={})
