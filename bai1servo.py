import time
import serial

ser = serial.Serial(
    port='/dev/ttyTHS1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

START = 833
END = 2173
STEP = 1  # moi xung 1 lan

while True:
    for pos in range(START, END + 1, STEP):
        ser.write(f'#1P{pos}T500D0\r\n'.encode('ascii'))
        time.sleep(0.02)