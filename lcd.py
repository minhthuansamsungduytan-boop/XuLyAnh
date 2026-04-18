from RPi_GPIO_i2c_LCD import lcd
from time import sleep

# Khoi tao LCD
lcdDisplay = lcd.HD44780(0x3f)
WIDTH = 20


def slide_to_target(text, stop_row, stop_pos):
    # Duyet qua tung dong tu dong 1 den dong can dung
    for r in range(1, stop_row + 1):
        is_last = (r == stop_row)
        # Neu la dong cuoi thi dung tai stop_pos, neu chua thi chay qua het man hinh (WIDTH)
        limit = stop_pos if is_last else WIDTH

        for p in range(-len(text), limit + 1):
            # To hop chuoi hien thi: khoang trang + chu
            display = (" " * max(0, p) + text[max(0, -p):])[:WIDTH]
            lcdDisplay.set(display, r)
            sleep(0.02)  # Toc do chay chu

        # Xoa dong cu neu chua phai la diem dung cuoi cung
        if not is_last:
            lcdDisplay.set(" " * WIDTH, r)


# Danh sach cau hinh: (Ten, Dong dung, Vi tri dung)
tasks = [
    ("Nhom 4", 1, (WIDTH - 6) // 2),  # Dong 1 - Chinh giua
    ("Bui Nguyen Kim Ngan", 2, 0),  # Dong 2 - Trai cung
    ("Mai Tuyet Ly", 3, WIDTH - 12),  # Dong 3 - Phai cung
    ("Le Minh Thuan", 4, 0),  # Dong 4 - Trai cung
]

# Thuc thi
lcdDisplay.clear()
for name, row, pos in tasks:
    slide_to_target(name, row, pos)