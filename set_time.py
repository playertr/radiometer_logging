import ntplib
import datetime as dt

import serial
from pycampbellcr1000 import CR1000 # pip install git+https://github.com/playertr/PyCampbellCR1000.git
import pandas as pd # pip install pandas

"""Query the datetime from an NTP server"""
def get_time_ntp() -> dt.datetime:
    c = ntplib.NTPClient()
    # Provide the respective ntp server ip in below function
    response = c.request('us.pool.ntp.org', version=3)
    response.offset
    return dt.datetime.fromtimestamp(response.tx_time, dt.timezone.utc)

"""Get the current time from this computer"""
def get_time_local() -> dt.datetime:
    return dt.datetime.now()

def connect_to_device(port : str = "/dev/ttyUSB0") -> CR1000:
    # Open a connection to the CR1000 using PyCambellCR1000.
    # Use PySerial instead of PyLink to make the connection more reliable on Windows
    # as described here:
    # https://github.com/LionelDarras/PyCampbellCR1000/issues/21#issuecomment-1117096281

    # use port=None to create a serial port object without opening the underlying port
    ser = serial.Serial(port=None, 
        baudrate=115200,
        timeout=2,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=1)

    ser.port = port
    cr1000 = CR1000(ser)
    return cr1000

def as_utc_str(time: dt.datetime) -> str:
    return time.replace(tzinfo=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

print("Connecting to CR1000.")
device = connect_to_device()

print(f"Device time is currently {device.gettime()}.")
try:
    now = get_time_ntp()
    print("Got time from NTP server.")
except Exception as e:
    print("Could not get time from NTP server. Error:")
    print(e)
    print("Using local device time.")

    now = get_time_local()

now = now.replace(tzinfo=None).replace(microsecond=0)
device.settime(now)
print(f"Set device time to {now} UTC.")
