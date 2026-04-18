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

channel = 1
A = 850
B = 2150
step = 10

try:
    while True:
        p = A
        while p <= B:
            cmd = f'#{channel}P{p}T100D100\r\n'
            print("Gui:", cmd.strip())
            ser.write(cmd.encode())
            time.sleep(0.2)
            p += step

        p = B
        while p >= A:
            cmd = f'#{channel}P{p}T100D100\r\n'
            print("Gui:", cmd.strip())
            ser.write(cmd.encode())
            time.sleep(0.2)
            p -= step

except KeyboardInterrupt:
    print("Dung chuong trinh")
finally:
    ser.close()