import time
import serial
import Jetson.GPIO as GPIO

# 1. Cấu hình Serial cho Servo (Gửi lệnh qua TX/RX) [cite: 1, 21]
ser = serial.Serial(
    port='/dev/ttyTHS1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# 2. Cấu hình GPIO cho Motor & LED
LED_PINS = [7, 29, 31, 26]  # D4, D5, D6, D7 [cite: 21]
MOTOR_PINS = [11, 12, 13, 15]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PINS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_PINS, GPIO.OUT, initial=GPIO.LOW)

channel = 1 # Servo channel theo ý bạn


def control_4_modules(p_val, motor_bits, led_pin, lcd_msg):
    # Điều khiển Servo qua Serial
    cmd = f'#{channel}P{p_val}T300D300\r\n'
    ser.write(cmd.encode())

    # Điều khiển LED
    GPIO.output(LED_PINS, GPIO.LOW)  # Tắt hết LED trước [cite: 21]
    GPIO.output(led_pin, GPIO.HIGH)  # Bật LED tương ứng [cite: 21]

    # Điều khiển Motor
    GPIO.output(MOTOR_PINS, motor_bits)  # Xuất 4 bit ra motor

    # Hiển thị LCD (Print terminal)
    print(f"LCD: {lcd_msg} | Servo P: {p_val}")


try:
    while True:
        # Ví dụ: Trạng thái Thẳng Tiến (Sơ đồ: 1011, P1500, LED D4/chân 7)
        control_4_modules(1500, (1, 0, 1, 1), 7, "Thang Tien")
        time.sleep(2)

        # Ví dụ: Trạng thái Rẽ Phải (Sơ đồ: 0001, P1750, LED D6/chân 31)
        control_4_modules(1750, (0, 0, 0, 1), 31, "Re Phai")
        time.sleep(2)

except KeyboardInterrupt:
    print("Dung chuong trinh")
finally:
    GPIO.cleanup()
    ser.close()