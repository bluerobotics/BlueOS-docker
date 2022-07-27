import logging
from typing import Dict, List

from serial import Serial

from ping1d_driver import Ping1DDriver
from ping360_driver import Ping360Driver
from pingdriver import PingDriver
from pingutils import PingDeviceDescriptor, PingType


class PingManager:
    def __init__(self) -> None:
        self.drivers: Dict[PingDeviceDescriptor, PingDriver] = {}
        self.ping1d_current_port: int = 9090
        self.ping360_current_port: int = 9092

    def stop_driver_at_port(self, port: Serial) -> None:
        """Stops the driver instance running for port "port" """
        ping_at_port = list(filter(lambda ping: ping.port == port, self.drivers.keys()))
        print(f"stopping: {port}")
        if ping_at_port:
            self.drivers[ping_at_port[0]].stop()
            del self.drivers[ping_at_port[0]]

    async def launch_driver_instance(self, ping: PingDeviceDescriptor) -> None:
        """Launches a new driver instance for the PingDeviceDescriptor "ping" """
        driver: PingDriver
        if ping.ping_type == PingType.PING1D:
            logging.info("Launching ping1d driver")
            driver = Ping1DDriver(ping, self.ping1d_current_port)
            self.ping1d_current_port -= 1
        elif ping.ping_type == PingType.PING360:
            logging.info("Launching ping360 driver")
            driver = Ping360Driver(ping, self.ping360_current_port)
            self.ping360_current_port += 1

        self.drivers[ping] = driver
        await driver.start()

    def devices(self) -> List[PingDeviceDescriptor]:
        return list(self.drivers.keys())


    def update_device_settings(self, sensor_settings):
        found = [driver for (sensor, driver) in self.drivers.items() if sensor.port.device == sensor_settings["port"]]
        print([sensor for sensor in self.drivers if sensor.port.device == sensor_settings["port"]])

        for sensor in self.drivers:
            import pprint
            pprint.pprint(vars(sensor))
        print([sensor.port.device_path for sensor in self.drivers])
        if not found:
            raise ValueError(f"unknown device: {port}")
        found[0].update_settings(sensor_settings)