"""Client for Laurent."""

import aiohttp
from json import JSONDecoder


class LaurentData:
    firmware: str | None
    serial_number: str | None
    mac: str | None
    model: str | None
    states: list[bool] | None

    def __init__(self, input) -> None:
        self.firmware = input.get("fw")
        self.serial_number = input.get("sn")
        self.mac = input.get("mac")
        self.model = self._model_by_fw(input.get("fw"))
        self.states = list(bool(int(x)) for x in input.get("rele"))

    def _model_by_fw(self, fw: str) -> str:
        if fw.startswith("LR"):
            return "Laurent-112"
        elif fw.startswith("LX"):
            return "Laurent-128"
        elif fw.startswith("L"):
            return "Laurent-2"
        else:
            return "Unknown Model"


class Laurent:
    def __init__(self, host: str, password: str) -> None:
        self.host = host
        self.password = password

    async def fetch_info(self) -> LaurentData:
        params = {"psw": self.password}
        async with aiohttp.ClientSession(self.host) as session:
            async with session.get("/json_sensor.cgi", params=params) as resp:
                # TODO: Add error handling.
                return await resp.json(
                    content_type="text/html",
                    loads=JSONDecoder(object_hook=LaurentData).decode,
                )

    async def turn_on(self, idx: int) -> bool:
        return await self.exec_command(f"REL,{idx},1")

    async def turn_off(self, idx: int) -> bool:
        return await self.exec_command(f"REL,{idx},0")

    async def exec_command(self, cmd: str) -> bool:
        params = {"psw": self.password, "cmd": cmd}
        async with aiohttp.ClientSession(self.host) as session:
            async with session.get("/cmd.cgi", params=params) as resp:
                ret = await resp.text()
                print("---", ret, "---")
                return True


# Laurent-112 версии
# программного обеспечения (версия “прошивки”) LR11 (и старше), модулю
# Laurent-128 версии “прошивки” LX11 (и страше), модулю Laurent-2 версии
# “прошивки” L212 (и страше).

    # async def fetch_info(self):
    #     async with aiohttp.request(
    #         "get",
    #         f"http://{self.host}/json_sensor.cgi?psw={self.password}",
    #     ) as resp:
    #         return await resp.json(content_type="text/html")  # fix for Laurent

    # async def switch_state(self, socket_id: int, state: int):
    #     command = f"REL,{socket_id},{state}"

    #     # async with aiohttp.request(
    #     #     "get",
    #     #     f"http://{self.host}/cmd.cgi?psw={self.password}&cmd={command}"
    #     # )

    # async def exec_command(self, cmd: str) -> str:
    #     async with aiohttp.request(
    #         "get",
    #         f"http://{self.host}/cmd.cgi?psw={self.password}&cmd={cmd}",
    #     ) as resp:
    #         return await resp.text()

    #     # import logging

    #     # from homeassistant.components.switch import (
    #     #     SwitchDeviceClass,
    #     #     SwitchEntity,
    #     #     SwitchEntityDescription  # ?
    #     # )
    #     # from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
    #     # from homeassistant.core import HomeAssistant
    #     # from homeassistant.helpers.entity_platform import AddEntitiesCallback
    #     # from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

    #     # _LOGGER = logging.getLogger(__name__)

    #     # class Laurent:
    #     #     pass

    #     # async def async_setup_platform(
    #     #     hass: HomeAssistant,
    #     #     config: ConfigType,
    #     #     add_entities: AddEntitiesCallback,
    #     #     discovery_info: DiscoveryInfoType | None = None
    #     # ) -> None:
    #     #     _LOGGER.warning("setup_platform", config)
    #     #     add_entities(LaurentSwitch())

    #     # class LaurentSwitch(SwitchEntity):
    #     #     """ Representation of Laurent switch entity."""
    #     #     _attr_name = "Example Switch"
    #     #     _attr_device_class = SwitchDeviceClass.SWITCH
    #     #     #     _attr_name = "Example Temperature"
    #     #     # _attr_native_unit_of_measurement = TEMP_CELSIUS
    #     #     # _attr_device_class = SensorDeviceClass.TEMPERATURE
    #     #     # _attr_state_class = SensorStateClass.MEASUREMENT

    #     # # ### Laurent client. ###

    #     # # import aiohttp

    #     # # class Laurent():
    #     # #     host: str
    #     # #     password: str
    #     # #     firmware: str

    #     # #     def __init__(self, host: str, password: str) -> None:
    #     # #         self.host = host
    #     # #         self.password = password
