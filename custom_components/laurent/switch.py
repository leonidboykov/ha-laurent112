
from typing import Any
import logging

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    CONF_NAME
)

from .const import (
    DOMAIN,
    MANUFACTURER,
)
from .coordinator import LaurentDataCoordinator
from .laurent import LaurentData


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: LaurentDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = await coordinator.laurent.fetch_info()
    async_add_entities(
        [LaurentSwitchEntity(coordinator, idx+1, data)
         for idx in range(len(data.states))],
        True
    )


class LaurentSwitchEntity(
    CoordinatorEntity[LaurentDataCoordinator], SwitchEntity
):
    """Implementation of Laurent switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(self, coordinator: LaurentDataCoordinator, idx: int, data: LaurentData) -> None:
        super().__init__(coordinator=coordinator, context=idx)
        self.idx = idx
        self._attr_unique_id = f"{coordinator.config.data.get(CONF_NAME)} Socket {idx}"
        self._attr_name = f"{coordinator.config.data.get(CONF_NAME)} Socket {idx}"
        self._attr_is_on = data.states[idx-1]

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config.entry_id)},
            name=self.coordinator.config.data.get(CONF_NAME),
            model=data.model,
            manufacturer=MANUFACTURER,
            sw_version=data.firmware,
            hw_version=data.serial_number,
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.laurent.turn_off(self.idx)
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.laurent.turn_on(self.idx)
        await self.coordinator.async_request_refresh()

    def _handle_coordinator_update(self) -> None:
        self._attr_is_on = self.coordinator.data.states[self.idx-1]
        self.async_write_ha_state()
