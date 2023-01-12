# get_progstats.py
# Tim Player, January 10 2023
# Script that connects to a CR1000 and gets progstats

from cr1000utils import connect_to_device
import argparse

# Add parser object for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Port to connect to like /dev/ttyUSB0")

if __name__ == "__main__":

    args = parser.parse_args() # get command line args

    print("Connecting to CR1000.")
    device = connect_to_device(args.port)

    progstats = device.getprogstat()

    print("progstats:")
    for k, v in progstats.items():
        print(f"{k} \t:\t{v}")