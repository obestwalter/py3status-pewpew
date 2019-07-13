import serial.tools.list_ports

SERIAL_DEVICE = '/dev/ttyACM0'


def send_number(number: int, serial_device: str = SERIAL_DEVICE):  # TODO: this should be context manager
    with serial.Serial(serial_device, 9600, timeout=1) as ser:
        if number < 0 or number > 99:
            raise Exception("Invalid argument")
        ser.write(b"%d\r\n" % number)
