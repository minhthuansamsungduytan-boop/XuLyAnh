import serial
import time

# Cau hinh
PORT = 'COM3'
BAUD = 9600
CHANNEL = 1
START = 833
END = 2173
STEPS = 8
MOVE_TIME = 500  # ms

ser = serial.Serial(PORT, BAUD, timeout=1)

def send_servo(channel, position, time_ms=500):
    cmd = f"#{channel}P{int(position)}T{time_ms}D0\r\n"
    ser.write(cmd.encode('ascii'))
    print(f"Sent: {cmd.strip()}")

try:
    for i in range(STEPS + 1):
        pos = START + i * (END - START) / STEPS
        send_servo(CHANNEL, pos, MOVE_TIME)
        time.sleep(0.7)

except Exception as e:
    print(f"Loi: {e}")

finally:
    ser.close()