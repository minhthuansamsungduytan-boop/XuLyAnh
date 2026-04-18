import RPi.GPIO as GPIO
import time

# --- CẤU HÌNH PIN (BCM) ---
# Motor trái (Bánh A)
IN1 = 17
IN2 = 18

# Motor phải (Bánh B)
IN3 = 22
IN4 = 23

# Thời gian chờ giữa các bước
delay = 2.0

# --- THIẾT LẬP GPIO ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)


def set_motors(i1, i2, i3, i4):
    """
    Hàm bổ trợ điều khiển logic an toàn.
    Luôn đưa các chân về 0 trước khi set giá trị mới để tránh ngắn mạch (1,1).
    """
    GPIO.output([IN1, IN2, IN3, IN4], 0)
    GPIO.output(IN1, i1)
    GPIO.output(IN2, i2)
    GPIO.output(IN3, i3)
    GPIO.output(IN4, i4)


# --- 9 TRƯỜNG HỢP ĐIỀU KHIỂN AN TOÀN ---

def stop():
    """1. Dừng xe (Trôi tự do)"""
    set_motors(0, 0, 0, 0)


def forward():
    """2. Tiến thẳng"""
    set_motors(0, 1, 0, 1)


def backward():
    """3. Lùi thẳng"""
    set_motors(1, 0, 1, 0)


def spin_right():
    """4. Xoay tại chỗ sang phải (Trái tiến - Phải lùi)"""
    set_motors(0, 1, 1, 0)


def spin_left():
    """5. Xoay tại chỗ sang trái (Trái lùi - Phải tiến)"""
    set_motors(1, 0, 0, 1)


def turn_left_forward():
    """6. Rẽ trái tiến (Chỉ bánh phải tiến)"""
    set_motors(0, 0, 0, 1)


def turn_right_forward():
    """7. Rẽ phải tiến (Chỉ bánh trái tiến)"""
    set_motors(0, 1, 0, 0)


def turn_left_backward():
    """8. Lùi quẹo trái (Chỉ bánh phải lùi)"""
    set_motors(0, 0, 1, 0)


def turn_right_backward():
    """9. Lùi quẹo phải (Chỉ bánh trái lùi)"""
    set_motors(1, 0, 0, 0)


# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    try:
        print("Bắt đầu thử nghiệm 9 chế độ an toàn...")

        while True:
            print("Đang tiến...")
            forward()
            time.sleep(delay)

            print("Xoay trái tại chỗ...")
            spin_left()
            time.sleep(delay)

            print("Rẽ phải tiến...")
            turn_right_forward()
            time.sleep(delay)

            print("Dừng xe...")
            stop()
            time.sleep(delay)

            # Bạn có thể gọi thêm các hàm khác ở đây để test đủ 9 cái

    except KeyboardInterrupt:
        print("\nĐã dừng bởi người dùng.")
    finally:
        stop()
        GPIO.cleanup()
        print("Đã dọn dẹp GPIO. Sẵn sàng thoát.")