import time
import serial
import Jetson.GPIO as GPIO

# --- 1. CẤU HÌNH SERIAL (Đầy đủ thông số 8N1) ---
ser = serial.Serial(
    port='/dev/ttyTHS1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# --- 2. CẤU HÌNH MOTOR (Chân vật lý Jetson Nano) ---
IN1, IN2, IN3, IN4 = 11, 12, 15, 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)


def send_servo_cmd(pulse):
    """Gửi lệnh điều khiển Servo qua cổng Serial"""
    # Định dạng chuỗi lệnh theo đúng yêu cầu của Thuận
    cmd = f'#1P{pulse}T500D500\r\n'
    ser.write(cmd.encode())
    print(f"Gửi lệnh Servo: {cmd.strip()}")


def set_motor(i1, i2, i3, i4, pulse):
    """Hàm điều khiển tổng hợp: Bảo vệ mạch -> Lái Servo -> Chạy Motor"""
    # 1. Luôn đưa về 0 trước để bảo vệ mạch cầu H (tránh ngắn mạch)
    GPIO.output([IN1, IN2, IN3, IN4], 0)

    # 2. Xuất lệnh Servo trước để chuẩn bị hướng lái
    send_servo_cmd(pulse)

    # 3. Xuất lệnh motor bánh sau
    GPIO.output(IN1, i1)
    GPIO.output(IN2, i2)
    GPIO.output(IN3, i3)
    GPIO.output(IN4, i4)

    # Chờ 0.5s để xe thực hiện trạng thái trước khi sang lệnh mới
    time.sleep(0.5)


# --- 3. CHƯƠNG TRÌNH CHÍNH (9 TRẠNG THÁI) ---
if __name__ == "__main__":
    try:
        print("Đang bắt đầu chạy 9 trạng thái đồng bộ từ bản vẽ tay...")

        # Trạng thái 1: Dừng (Thái độ đầu tiên)
        set_motor(0, 0, 0, 0, 1500)

        # Trạng thái 2: Lùi thẳng
        set_motor(1, 0, 1, 0, 1500)

        # Trạng thái 3: Tiến thẳng
        set_motor(0, 1, 0, 1, 1500)

        # Trạng thái 4: Rẽ phải
        set_motor(0, 0, 0, 1, 1750)

        # Trạng thái 5: Rẽ phải gắt
        set_motor(0, 0, 1, 0, 1830)

        # Trạng thái 6: Rẽ trái
        set_motor(0, 1, 0, 0, 810)

        # Trạng thái 7: Rẽ trái gắt
        set_motor(1, 0, 0, 0, 750)

        # Trạng thái 8: Xoay phải
        set_motor(0, 1, 1, 0, 625)

        # Trạng thái 9: Xoay trái
        set_motor(1, 0, 0, 1, 1900)

        # Cuối cùng: Đưa về trạng thái dừng an toàn
        print("Hoàn thành lộ trình. Dừng xe.")
        set_motor(0, 0, 0, 0, 1500)

    except KeyboardInterrupt:
        print("\nNgười dùng dừng chương trình bằng phím bấm.")
    finally:
        # Dọn dẹp hệ thống trước khi thoát
        GPIO.output([IN1, IN2, IN3, IN4], 0)
        GPIO.cleanup()
        ser.close()
        print("Đã đóng cổng Serial và dọn dẹp GPIO.")