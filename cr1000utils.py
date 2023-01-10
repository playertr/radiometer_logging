
from pycampbellcr1000 import CR1000 # pip install git+https://github.com/playertr/PyCampbellCR1000.git
import serial

def connect_to_device(port : str = "/dev/ttyUSB0") -> CR1000:
    # Open a connection to the CR1000 using PyCambellCR1000.
    # Use PySerial instead of PyLink to make the connection more reliable on Windows
    # as described here:
    # https://github.com/LionelDarras/PyCampbellCR1000/issues/21#issuecomment-1117096281

    # use port=None to create a serial port object without opening the underlying port
    ser = serial.Serial(port=None, 
        baudrate=38400,
        timeout=2,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=1)

    ser.port = port
    cr1000 = CR1000(ser)
    return cr1000
