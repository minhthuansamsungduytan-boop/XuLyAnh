from ultralytics import YOLO

if __name__ == '__main__':
    # 1. Khởi tạo model YOLO11 bản Nano (nhẹ và nhanh)
    # Vì bạn đã sửa nhãn rất kỹ, nên bắt đầu mới từ yolo11n.pt
    model = YOLO('yolo11n.pt')

    print("--- BẮT ĐẦU HUẤN LUYỆN LẠI VỚI 606 ẢNH ĐÃ CẬP NHẬT NHÃN MỚI ---")

    # 2. Huấn luyện
    model.train(
        # Đường dẫn đến file yaml của bạn
        data=r'C:\Users\LeMinhThuan\OneDrive\Desktop\XuLiAnh\Yolo\DataSet\dataset.yaml',

        epochs=150,  # 150 vòng là con số "vàng" để model ngấm dữ liệu
        imgsz=640,  # Kích thước ảnh chuẩn
        batch=16,  # Card RTX 4050 dư sức chạy batch 16, giúp train nhanh hơn

        # --- CÁC THAM SỐ TỐI ƯU ---
        optimizer='AdamW',  # Bộ tối ưu thông minh giúp hội tụ nhanh
        lr0=0.01,  # Tốc độ học ban đầu chuẩn cho AdamW
        device=0,  # ÉP CHẠY GPU (Card rời)
        workers=0,  # Tránh lỗi đa luồng trên Windows

        # --- TĂNG CƯỜNG ĐỘ CHÍNH XÁC ---
        augment=True,  # Tự động xoay, lật ảnh để máy học đa dạng hơn
        close_mosaic=10,  # 10 vòng cuối tắt ghép ảnh để tinh chỉnh khung hình (box)
        label_smoothing=0.1,  # Giúp model bớt "tự tin thái quá", giảm nhận diện nhầm
    )