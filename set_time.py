# set_time.py
# Tim Player, January 5 2023
# Script that connects to a CR1000 and sets the time from an
# NTP server or from the device's present time.

import ntplib
import datetime as dt
from cr1000utils import connect_to_device
import argparse

# Add parser object for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Port to connect to like /dev/ttyUSB0")

"""Query the datetime from an NTP server"""
def get_time_ntp() -> dt.datetime:
    c = ntplib.NTPClient()
    # Provide the respective ntp server ip in below function
    response = c.request('us.pool.ntp.org', version=3)
    response.offset
    return dt.datetime.fromtimestamp(response.tx_time, dt.timezone.utc)

"""Get the current time from this computer"""
def get_time_local() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)

def as_utc_str(time: dt.datetime) -> str:
    return time.replace(tzinfo=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":

    args = parser.parse_args() # get command line args

    print("Connecting to CR1000.")
    device = connect_to_device(args.port)

    # attempt to get time from NTP server or locally
    try:
        now = get_time_ntp()
        print("Got time from NTP server in UTC.")
    except Exception as e:
        print("Could not get time from NTP server. Error:")
        print(e)
        print("Using local device time in UTC.")

        now = get_time_local()

    now = now.replace(tzinfo=None).replace(microsecond=0)
    device.settime(now)
    print(f"Set device time to {now} UTC.")
