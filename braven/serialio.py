"""
Low-level serial I/O helpers for the Featherweight Blue Raven.

Notes:
- USB CDC ignores baudrate but pyserial requires one. 115200 8N1 is fine.
- Disable flow control explicitly. Use small read timeout for responsiveness.
"""

import serial
from serial.tools import list_ports


def list_serial_ports():
    return list_ports.comports()


def open_port(port: str, *, timeout: float = 0.1) -> serial.Serial:
    """Open a configured Serial instance.

    timeout: per-read timeout in seconds (small for streaming).
    """
    return serial.Serial(
        port=port,
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=timeout,
        write_timeout=10.0,
        rtscts=False,
        dsrdtr=False,
        xonxoff=False,
    )
