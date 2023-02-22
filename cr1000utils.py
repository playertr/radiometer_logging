
from pycampbellcr1000 import CR1000 # pip install git+https://github.com/playertr/PyCampbellCR1000.git
import serial
import multiprocessing.pool
import functools

# Decorator to time out a function
# https://stackoverflow.com/questions/492519/timeout-on-a-function-call
def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


@timeout(5.0)
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
