import aiohttp
import datetime
import ipaddress
import logging
from decimal import Decimal

DEFAULT_RESOLUTION = "DAY"
METER_SERIAL = "DEFAULT"

_LOGGER = logging.getLogger(__name__)

class Chargebox:
    """
    Instantiate a Garo Chargebox
    Data will be fetched from the Chargebox API given the IP Address and the Serial identifier

    :param ip_addr: The ipv4 address of the Chargebox
    :type ip_addr: ipaddress.ip_address

    :param serial: The serial identifier of the Chargebox
    :type serial: str
    """
    def __init__(self, ip_addr: ipaddress.ip_address, serial: str) -> None:
        self.ip_addr = ip_addr
        self.serial = serial

    async def GetCurrentEnergyUsage(self) -> Decimal:

        from_date = datetime.datetime.utcnow() - datetime.timedelta(days = 1)
        to_date = datetime.datetime.utcnow() + datetime.timedelta(days = 1)

        resp_dict = await self.__getFromChargeBox(from_date, to_date, DEFAULT_RESOLUTION)
        if resp_dict is not None: 
            _LOGGER.debug("device reports {0:.1f} kWh".format(Decimal(resp_dict["stopValue"])))
            return Decimal(resp_dict["stopValue"])
        return 0

    async def __getFromChargeBox(self, from_date, to_date, resolution) -> dict:
        timeout = aiohttp.ClientTimeout(total=30)
        try: 
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f"http://{self.ip_addr}:8080/servlet/rest/chargebox/energy",
                    json={
                        "chargeboxSerial": self.serial,
                        "fromDate": from_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "toDate": to_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "meterSerial": METER_SERIAL,
                        "resolution": resolution
                    }) as response:
                    resp_dict = await response.json()
                    return resp_dict
        except (aiohttp.ClientConnectorError, OSError) as err:
            _LOGGER.warning(
                "device %s get from chargebox error - %s", self.ip_addr, repr(err)
            )
