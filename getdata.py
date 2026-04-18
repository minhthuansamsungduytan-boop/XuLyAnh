import cv2
import os


def FrameCapture(path):
    # Kiểm tra và tạo thư mục dataset nếu chưa có
    output_dir = "dataset"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Khởi tạo đối tượng video
    vidObj = cv2.VideoCapture(path)
    count = 0
    success = True

    print("Đang bắt đầu trích xuất khung hình...")

    while success:
        # Đọc frame tiếp theo
        success, image = vidObj.read()

        # Nếu đọc thành công và đúng frame thứ 10, 20, 30...
        if success and count % 10 == 0:
            # Lưu ảnh vào thư mục dataset
            file_path = os.path.join(output_dir, f"frame{int(count / 10)}.jpg")
            cv2.imwrite(file_path, image)

        count += 1

    # Giải phóng đối tượng video sau khi xong
    vidObj.release()
    print(f"Hoàn thành! Đã lưu các ảnh vào thư mục '{output_dir}'.")


# Driver Code
if __name__ == '__main__':
    # Thay "test.mp4" bằng đường dẫn video của bạn
    FrameCapture("test.mp4")