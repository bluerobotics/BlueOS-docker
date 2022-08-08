import logging
import shlex
import time
from shutil import which
from subprocess import DEVNULL, Popen

from serial.tools.list_ports_linux import SysFS

from bridges.serialhelper import Baudrate


# pylint: disable=too-many-arguments
class Bridge:
    """Basic abstraction of Bridges. Used to bridge serial devices to UDP ports"""

    def __init__(
        self,
        serial_port: SysFS,
        baud: Baudrate,
        ip: str,
        udp_port: int,
        automatic_disconnect: bool = True,
    ) -> None:
        bridges = which("bridges")
        automatic_disconnect_clients = "" if automatic_disconnect else "--no-udp-disconnection"
        command_line = f"{bridges} -u {ip}:{udp_port} -p {serial_port.device}:{baud} {automatic_disconnect_clients}"
        logging.info(f"Launching bridge link with command '{command_line}'.")
        # pylint: disable=consider-using-with
        self.process = Popen(shlex.split(command_line), stdout=DEVNULL, stderr=DEVNULL)
        time.sleep(1.0)
        if self.process.poll() is not None:
            _stdout, strerr = self.process.communicate()
            error = strerr.decode("utf-8") if strerr else "Empty error"
            raise RuntimeError(f'Failed to initialize bridge, code: {self.process.returncode}, message: "{error}".')

    def stop(self) -> None:
        if not self.process:
            raise RuntimeError("Bridges process doesn't exist.")
        self.process.kill()
        time.sleep(1.0)
        if self.process.poll() is None:
            raise RuntimeError("Failed to kill bridges process.")

    def __del__(self) -> None:
        self.stop()
