# test.py
# Tim Player, January 1 2023
# Test script that connects to a CR1000 on COM3 on a Windows computer and 
# downloads the last hour of data from the 'Radiation' table.
# The script prints the data and writes it to a file.
import serial
from pycampbellcr1000 import CR1000 # pip install pycambellcr1000
import pandas as pd # pip install pandas
import datetime

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

ser.port = "COM3"
cr1000 = CR1000(ser)


# Print out the tables stored by the CR1000
print(cr1000.list_tables())

# Retrieve and print the last hour of data
end = cr1000.gettime()
start = end - datetime.timedelta(hours=1)

lwdata = cr1000.get_data('Radiation', start, end) # Read dictionary from CR1000
lwdf = pd.DataFrame(lwdata) # convert to Pandas DataFrame for prettier formatting

print(lwdf) # print the table
lwdf.to_csv('last_hour.csv') # write to CSV file
