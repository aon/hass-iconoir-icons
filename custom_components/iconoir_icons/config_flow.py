"""Config flow for Iconoir Icons (single instance, stroke-width option)."""
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers import selector

from . import CONF_STROKE_WIDTH, DEFAULT_STROKE_WIDTH, DOMAIN, STROKE_WIDTHS


class IconoirIconsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Trivial flow: single instance is enforced by the manifest."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        return self.async_create_entry(title="Iconoir Icons", data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return IconoirIconsOptionsFlow(config_entry)


class IconoirIconsOptionsFlow(OptionsFlow):
    """Let the user pick the icon stroke width."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        # Stored privately so this works across HA versions without tripping
        # the `self.config_entry` assignment deprecation.
        self._entry = config_entry

    async def async_step_init(self, user_input=None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self._entry.options.get(CONF_STROKE_WIDTH, DEFAULT_STROKE_WIDTH)
        schema = vol.Schema(
            {
                vol.Required(CONF_STROKE_WIDTH, default=current): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=w, label=f"{w} px")
                            for w in STROKE_WIDTHS
                        ],
                        mode=selector.SelectSelectorMode.LIST,
                        translation_key=CONF_STROKE_WIDTH,
                    )
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
