import serial
import time

# Cau hinh
PORT = 'COM3'
BAUD = 9600
CHANNEL = 1
START = 833
END = 2173
STEP = 10        # 10 xung moi lan
MOVE_TIME = 500  # ms

ser = serial.Serial(PORT, BAUD, timeout=1)

def send_servo(channel, position, time_ms=500):
    cmd = f"#{channel}P{int(position)}T{time_ms}D0\r\n"
    ser.write(cmd.encode('ascii'))
    print(f"Sent: {cmd.strip()}")

try:
    while True:
        for pos in range(START, END + 1, STEP):
            send_servo(CHANNEL, pos, MOVE_TIME)
            time.sleep(0.7)

except KeyboardInterrupt:
    print("Dung lai.")

finally:
    ser.close()