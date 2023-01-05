# read_data_python.py
# Tim Player, January 1 2023
# Test script that connects to a CR1000 on COM3 on a Windows computer and 
# downloads the last hour of data from the 'Radiation' table.
# The script prints the data and writes it to a file.

import pandas as pd # pip install pandas
import datetime
import argparse
from cr1000utils import connect_to_device

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Port to connect to like /dev/ttyUSB0")
parser.add_argument("--hours", type=int, default="0", help="Integer number of hours into the past of data to retrieve. 0 for all data.")
parser.add_argument("--output", type=str, default="data.csv", help="Path of output CSV file.")

if __name__ == "__main__":

    args = parser.parse_args()

    cr1000 = connect_to_device(args.port)

    # Print out the tables stored by the CR1000
    print(f"Tables stored in device: \n{cr1000.list_tables()}")

    start, end = None, None
    
    if args.hours != 0:
        # Retrieve and print the last n hours of data if requested
        end = cr1000.gettime()
        start = end - datetime.timedelta(hours=args.hours)

    print(f"Getting data from {start} to {end}.")
    lwdata = cr1000.get_data('Radiation', start_date=start, stop_date=end) # Read dictionary from CR1000
    lwdf = pd.DataFrame(lwdata) # convert to Pandas DataFrame for prettier formatting
    print(lwdf) # print the table
    lwdf.to_csv(args.output) # write to CSV file
