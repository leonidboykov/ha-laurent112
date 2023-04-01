"""Coordinatior for Laurent."""

from typing import Any
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.const import (
    CONF_NAME,
    CONF_SCAN_INTERVAL
)

from .laurent import (
    Laurent,
    LaurentData
)

_LOGGER = logging.getLogger(__name__)


class LaurentDataCoordinator(DataUpdateCoordinator[LaurentData]):
    """Get latest data from Laurent."""

    config: ConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, client: Laurent) -> None:
        self.config = config_entry
        self.laurent = client
        super().__init__(
            hass,
            _LOGGER,
            name=config_entry.data.get(CONF_NAME),
            update_interval=timedelta(
                seconds=config_entry.data.get(CONF_SCAN_INTERVAL)),
            update_method=self.fetch_data
        )

    async def fetch_data(self) -> LaurentData:
        return await self.laurent.fetch_info()
