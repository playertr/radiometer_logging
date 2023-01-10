#!/usr/bin/python3
# get_data.py
# This script:

# finds all USB devices
# attempts to connect to each one as a CR1000 device
# reads the name of each CR1000 device
# verifies that the current time of the CR1000 is correct
# updates the data from each CR1000 device to a CSV file

from pycampbellcr1000 import CR1000
import cr1000utils as cru
from pathlib import Path, PosixPath
import datetime as dt
import pandas as pd

import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

MAX_ALLOWABLE_TIME_DIFF = dt.timedelta(seconds=3) # seconds

# a mapping from serial number to device name
names = {
    b'4295' : "shackleton",
    b'4297' : "klenova"
}

def get_device_name(device: CR1000) -> str:
    """Get the name of this device by reading its serial number."""
    progstat = device.getprogstat()
    serial_number = progstat['SerialNbr']
    try:
        name = names[serial_number]
    except KeyError as e:
        print(f"Device with serial number {serial_number} not in mapping {names}.")
        raise e
    return name

def get_usb_devices():
    """Open up the "/dev/" directory and look for USB devices"""
    devpath = Path("/dev/")
    paths = list(devpath.glob('*USB*'))
    if len(paths) == 0:
        raise IOError("No USB devices found in /dev/.")
    return paths

def get_last_date(csv_path: PosixPath) -> dt.datetime:
    """Get the last date from a CSV path if it has dates."""
    try:
        data = pd.read_csv(csv_path)
        last_date = data['Datetime'].max()
    except Exception as e:
        logger.info(f"Potential CSV path {csv_path} does not contain a valid date.")
        raise e
    return dt.datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")

def process_path(path: PosixPath) -> None:
    """Process this path, such as '/dev/ttyUSB0'."""

    # Connect to CR1000
    dev = cru.connect_to_device(str(path))

    # Find the CR1000's name
    name = get_device_name(dev)
    
    # Verify that the CR1000's time is correct
    time = dev.gettime()
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    if abs(time - now) > MAX_ALLOWABLE_TIME_DIFF:
        raise Exception(f"CR1000 time of {time} is too different from system time of {now}.")

    # Read new data from the CR1000.
    output_path = Path("output") / (name + ".csv")
    try: # attempt to get the latest date from the CSV path
        start_date = get_last_date(output_path)
    except:
        start_date = None
    data = dev.get_data('Radiation', start_date, None)
    df = pd.DataFrame(data)

    # Write data from CR1000 to disk.
    if start_date == None:
        print(f"Creating a new CSV file named {output_path} with {len(data)} entries.")
        df.to_csv(output_path, mode='w', header=True)
    else:
        print(f"Appending to CSV file named {output_path} .")
        print(f"Got {len(data)} new entries since {start_date} .")
        df.to_csv(output_path, mode='a', header=False)

def main():
    
    usb_paths = get_usb_devices()

    for usbpath in usb_paths:

        # attempt to process this path, and harmlessly print
        # any exceptions that occur
        print(f"Processing device at path {str(usbpath)} .")
        try:
            process_path(usbpath)
        except Exception as e:
            print(f"Processing device {usbpath} failed.")
            logger.exception(e)
            continue

        print()

if __name__ == "__main__":
    main()