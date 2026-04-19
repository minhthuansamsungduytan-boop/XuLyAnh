import time
import serial
import Jetson.GPIO as GPIO
from RPi_GPIO_i2c_LCD import lcd  # Thu vien LCD ban cung cap

# ─────────────────────────────────────────────
# ⚙️ 1. CẤU HÌNH LCD & SERIAL
# ─────────────────────────────────────────────
# Khoi tao LCD (Dia chi 0x3f, 20 cot)
lcdDisplay = lcd.HD44780(0x3f)
WIDTH = 20

# Cấu hình Serial cho Servo
ser = serial.Serial(
    port='/dev/ttyTHS1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# ─────────────────────────────────────────────
# 📍 2. CẤU HÌNH GPIO (LED & MOTOR)
# ─────────────────────────────────────────────
LED_PINS = [7, 29, 31, 26]  # D4, D5, D6, D7
MOTOR_PINS = [11, 12, 13, 15]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PINS, GPIO.OUT, initial=GPIO.HIGH)  # Tich cuc thap (HIGH = TAT)
GPIO.setup(MOTOR_PINS, GPIO.OUT, initial=GPIO.LOW)

channel = 2  # Servo channel


# ─────────────────────────────────────────────
# 🔧 3. HÀM HIỆU ỨNG LCD (Của bạn)
# ─────────────────────────────────────────────
def slide_msg(text, stop_row, stop_pos):
    """Hieu ung chu chay den vi tri chi dinh"""
    for r in range(1, stop_row + 1):
        is_last = (r == stop_row)
        limit = stop_pos if is_last else WIDTH
        for p in range(-len(text), limit + 1):
            display = (" " * max(0, p) + text[max(0, -p):])[:WIDTH]
            lcdDisplay.set(display, r)
            time.sleep(0.01)  # Tang toc do mot chut de robot phan hoi nhanh
        if not is_last:
            lcdDisplay.set(" " * WIDTH, r)


# ─────────────────────────────────────────────
# 🔧 4. HÀM ĐIỀU KHIỂN TỔNG HỢP 4 MODULE
# ─────────────────────────────────────────────
def control_robot(servo_p, motor_bits, active_led, lcd_text, row):
    # --- LED (Active Low) ---
    GPIO.output(LED_PINS, GPIO.HIGH)  # Tat het
    if active_led in LED_PINS:
        GPIO.output(active_led, GPIO.LOW)  # Bat LED chi dinh

    # --- Motor ---
    GPIO.output(MOTOR_PINS, motor_bits)

    # --- Servo Serial ---
    cmd = f'#{channel}P{servo_p}T300D300\r\n'
    ser.write(cmd.encode())

    # --- LCD Slide ---
    # Xoa dong hien tai truoc khi slide de tranh de chu
    lcdDisplay.set(" " * WIDTH, row)
    slide_msg(lcd_text, row, 0)  # Slide den dau dong


# ─────────────────────────────────────────────
# 🚀 5. CHẠY THỬ NGHIỆM
# ─────────────────────────────────────────────
try:
    lcdDisplay.clear()
    print("He thong 4 module san sang...")

    # Vi du 1: Nhom 4 - Thang Tien
    # (Pulse, Motor, LED_Pin, Text, Row)
    control_robot(1500, (1, 0, 1, 1), 7, "Thang Tien", 1)
    time.sleep(1)

    # Vi du 2: Ngan - Thang Lui
    control_robot(1300, (0, 1, 0, 1), 29, "Thang Lui", 2)
    time.sleep(1)

    # Vi du 3: Ly - Re Phai
    control_robot(1750, (0, 0, 0, 1), 31, "Re Phai", 3)
    time.sleep(1)

    # Vi du 4: Thuan - Re Trai
    control_robot(750, (1, 0, 0, 0), 26, "Re Trai", 4)
    time.sleep(1)

except KeyboardInterrupt:
    print("\nStop.")
finally:
    lcdDisplay.clear()
    GPIO.output(LED_PINS, GPIO.HIGH)
    GPIO.output(MOTOR_PINS, GPIO.LOW)
    GPIO.cleanup()
    ser.close()