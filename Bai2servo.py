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

channel = 2
A = 833
B = 2177
step = 168

try:
    while True:
        # Di chuyen tu 1000 len 8 vi tri:
        # 1125, 1250, 1375, 1500, 1625, 1750, 1875, 2000
        p = A + step
        vi_tri = 1
        while p <= B:
            cmd = f'#{channel}P{p}T300D300\r\n'
            print(f'Len vi tri {vi_tri}:', cmd.strip())
            ser.write(cmd.encode())
            time.sleep(1)
            p += step
            vi_tri += 1

        # Di chuyen nguoc lai:
        # 1875, 1750, 1625, 1500, 1375, 1250, 1125
        p = B - step
        vi_tri = 7
        while p >= A + step:
            cmd = f'#{channel}P{p}T300D300\r\n'
            print(f'Xuong vi tri {vi_tri}:', cmd.strip())
            ser.write(cmd.encode())
            time.sleep(1)
            p -= step
            vi_tri -= 1

except KeyboardInterrupt:
    print("Dung chuong trinh")

finally:
    ser.close()
