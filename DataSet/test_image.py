from ultralytics import YOLO
import cv2
import os

if __name__ == '__main__':
    # 1. Load model best.pt (Đảm bảo đường dẫn này đúng với thư mục Train_Final mới nhất)
    model_path = r'C:\Users\LeMinhThuan\OneDrive\Desktop\XuLiAnh\Yolo\runs\detect\Yolo_RoadSign\Train_Final\weights\best.pt'
    model = YOLO(model_path)

    # 2. Danh sách ảnh test (Thuận có thể thêm bao nhiêu tùy thích)
    img_list = [
        r'C:\Users\LeMinhThuan\OneDrive\Desktop\XuLiAnh\Yolo\DataSet\val\images\frame555.jpg',
        r'C:\Users\LeMinhThuan\OneDrive\Desktop\XuLiAnh\Yolo\DataSet\val\images\frame_1000.jpg'
    ]

    print("--- Đang bắt đầu kiểm tra ảnh tĩnh ---")

    for img_path in img_list:
        # Kiểm tra xem file có tồn tại không trước khi chạy
        if not os.path.exists(img_path):
            print(f"⚠️ Cảnh báo: Không tìm thấy file {img_path}")
            continue

        # 3. Dự đoán với các tham số tối ưu
        # device=0: Chạy bằng GPU cho cực nhanh
        # conf=0.75: Chỉ hiện những gì chắc chắn (giúp loại bỏ biển 50 bị nhầm)
        results = model.predict(img_path, imgsz=640, conf=0.75, device=0)

        for r in results:
            # 4. Vẽ khung lên ảnh (line_width=3 cho dễ nhìn trên ảnh tĩnh)
            im_array = r.plot(line_width=3, font_size=1.2)

            # 5. Hiển thị cửa sổ ảnh
            # Dùng cv2.namedWindow để cửa sổ có thể tự co giãn theo màn hình
            cv2.namedWindow("Ket qua test anh", cv2.WINDOW_NORMAL)
            cv2.imshow("Ket qua test anh", im_array)

            print(f"✅ Đã xong: {os.path.basename(img_path)}. Nhấn phím bất kỳ để xem ảnh tiếp theo...")
            cv2.waitKey(0) # Đợi nhấn phím mới sang ảnh sau

    cv2.destroyAllWindows()
    print("--- Hoàn thành test danh sách ảnh ---")