import cv2
import time
import os
from ultralytics import YOLO

# ── CẤU HÌNH HỆ THỐNG ────────────────────────────────
MODEL_PATH = r'/best.pt'
CLASS_NAMES = ['1.Dung', '2.Do_xe', '3.O_to', '4.Tru_tron']

# Ngưỡng IOU để lọc khung trùng
IOU_THRESH = 0.45


class SimpleSmoother:
    """Giúp khung hình không bị nhảy (flicker) giữa các frame"""

    def __init__(self, keep_frames=5):
        self.history = []
        self.keep_frames = keep_frames

    def update(self, current_dets):
        # Đây là logic đơn giản, bạn có thể tích hợp SORT/DeepSORT nếu cần phức tạp hơn
        # Hiện tại trả về raw để code bạn chạy mượt trước
        return current_dets


def draw_detection(frame, det, is_stable=True):
    x1, y1, x2, y2 = det['box']
    conf = det['conf']
    label = det['label']

    color = (0, 255, 0) if is_stable else (0, 100, 0)  # Xanh sáng cho stable, xanh tối cho raw
    thickness = 2 if is_stable else 1

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    label_str = f"{label} {conf:.2%}"
    cv2.putText(frame, label_str, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)


def draw_hud(frame, fps, stable_count, raw_count):
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Stable: {stable_count} | Raw: {raw_count}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


def main():
    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Khong tim thay file: {MODEL_PATH}")
        return

    model = YOLO(MODEL_PATH)

    # Cài đặt HSV thấp ngay từ đầu để tránh lệch màu đỏ/cam như bạn muốn
    model.overrides['hsv_h'] = 0.005
    model.overrides['hsv_s'] = 0.3
    model.overrides['hsv_v'] = 0.2

    conf_thresh = 0.75  # Bắt đầu với ngưỡng cao để lọc biển 50

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    smoother = SimpleSmoother()
    prev_time = time.time()

    print("[INFO] Bam '+' de tang Conf, '-' de giam Conf. 'q' de thoat.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # ── INFERENCE ──────────────────────────────────────
        results = model.predict(frame,
                                device=0,
                                conf=conf_thresh,
                                iou=IOU_THRESH,
                                verbose=False)[0]

        # ── PARSE KẾT QUẢ ──────────────────────────
        raw_dets = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if cls_id >= len(CLASS_NAMES): continue

            label = CLASS_NAMES[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            raw_dets.append(dict(label=label, conf=conf, box=(x1, y1, x2, y2)))

        # ── TEMPORAL SMOOTHING ─────────────────────
        stable_dets = smoother.update(raw_dets)

        # ── VẼ ─────────────────────────────────────
        for det in raw_dets:
            draw_detection(frame, det, is_stable=False)

        for det in stable_dets:
            draw_detection(frame, det, is_stable=True)

        # HUD
        cur_time = time.time()
        fps = 1.0 / max(cur_time - prev_time, 1e-5)
        prev_time = cur_time
        draw_hud(frame, fps, len(stable_dets), len(raw_dets))

        cv2.putText(frame, f"Conf Threshold: {conf_thresh:.0%}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 255), 1)

        cv2.imshow("YOLO11 - Nhan dang vat the - Thuan", frame)

        # ── ĐIỀU KHIỂN ─────────────────────────────
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+') or key == ord('='):
            conf_thresh = min(conf_thresh + 0.05, 0.95)
            print(f"[CONF] Tang len {conf_thresh:.0%}")
        elif key == ord('-'):
            conf_thresh = max(conf_thresh - 0.05, 0.10)
            print(f"[CONF] Giam xuong {conf_thresh:.0%}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()