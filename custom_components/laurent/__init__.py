"""Support for the KernelChip Laurent device."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    CONF_HOST,
    CONF_PASSWORD,
)

from .const import (
    DOMAIN
)
from .coordinator import LaurentDataCoordinator
from .laurent import Laurent


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a device from a config entry."""

    # Setup the Laurent instance
    host = entry.data.get(CONF_HOST)
    password = entry.data.get(CONF_PASSWORD)
    laurent = Laurent(host, password)

    hass.data.setdefault(DOMAIN, {})[
        entry.entry_id
    ] = LaurentDataCoordinator(hass, entry, laurent)

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SWITCH])
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SWITCH])
    if unload_ok:
        hass.data.pop(DOMAIN)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
