import cv2
import time
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
import torch
import argparse

# Add Basler camera support
try:
    from pypylon import pylon
    BASLER_AVAILABLE = True
except ImportError:
    BASLER_AVAILABLE = False

# === Config ===
YOLO_MODEL_PATH = r"C:\Users\kraie\OneDrive\Bureau\iat\runs\detect\yolo8_custom_opt3\weights\best.pt"  # Use the smallest, fastest YOLO model you trained
CONFIDENCE = 0.3
YOLO_ENABLED = True  # Set to True to enable YOLO detection by default
MEDIAPIPE_ENABLED = True   # Set to True to enable MediaPipe hand detection by default
CAPTURE_ENABLED = True  # Set to False to disable capturing/processing frames

# === Load YOLO and MediaPipe ===
print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")
yolo = YOLO(YOLO_MODEL_PATH)
try:
    yolo.to('cuda')
    print("YOLO model moved to GPU.")
except Exception as e:
    print(f"Could not move YOLO to GPU: {e}")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)
mp_draw = mp.solutions.drawing_utils


def main():
    parser = argparse.ArgumentParser(description="YOLO + MediaPipe Basler/USB Camera Script")
    parser.add_argument('--camera', type=int, default=0, help='Camera index to use (default: 0)')
    parser.add_argument('-q', '--capture', action='store_true', help='Enable capturing (processing frames). If not set, the script will not process frames.')
    args = parser.parse_args()

    if not CAPTURE_ENABLED:
        print("[INFO] Capture not enabled. Exiting (set CAPTURE_ENABLED = True to enable).")
        return

    if BASLER_AVAILABLE:
        print("Checking for Basler cameras...")
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        print(f"Detected {len(devices)} Basler camera(s).")
        if len(devices) == 0:
            print("No Basler cameras detected. Exiting.")
            return
        cam_idx = min(args.camera, len(devices)-1)
        camera1 = pylon.InstantCamera(tl_factory.CreateDevice(devices[cam_idx]))
        camera1.Open()
        # Do not set ROI, use full sensor area
        # ROI_W = 640
        # ROI_H = 480
        # offset_x = int((camera1.Width.Value - ROI_W) / 2)
        # offset_y = int((camera1.Height.Value - ROI_H) / 2)
        # offset_x = offset_x - (offset_x % 4)
        # offset_y = offset_y - (offset_y % 4)
        # camera1.Width.Value = ROI_W
        # camera1.Height.Value = ROI_H
        # camera1.OffsetX.Value = offset_x
        # camera1.OffsetY.Value = offset_y
        # Set camera to full sensor area (maximum width and height)
        camera1.Width.Value = camera1.Width.Max
        camera1.Height.Value = camera1.Height.Max
        width = camera1.Width.Value
        height = camera1.Height.Value
        camera1.StartGrabbing()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        fps = 30
    else:
        print("Basler camera not available, falling back to OpenCV webcam...")
        cam_idx = args.camera
        camera1 = cv2.VideoCapture(cam_idx)
        if not camera1.isOpened():
            print(f"Could not open camera {cam_idx}.")
            return
        width = int(camera1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = camera1.get(cv2.CAP_PROP_FPS) or 25
    print(f"Camera FPS: {fps}")
    frame_count = 0
    start_time = time.time()
    out_path = 'yolo_mediapipe_results.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    while True:
        # Get frame from camera1
        if BASLER_AVAILABLE:
            if not camera1.IsGrabbing():
                print("[DEBUG] Basler camera stopped grabbing. Exiting loop.")
                break
            grab1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab1.GrabSucceeded():
                img1 = converter.Convert(grab1)
                frame1 = img1.GetArray()
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
            else:
                print("[DEBUG] Basler camera failed to grab frame. Exiting loop.")
                break
            grab1.Release()
        else:
            ret1, frame1 = camera1.read()
            if not ret1:
                print("[DEBUG] OpenCV camera failed to read frame. Exiting loop.")
                break
        # Downscale for even more speed (use at least 320x240 for MediaPipe)
        MEDIAPIPE_FRAME_W = 320
        MEDIAPIPE_FRAME_H = 240
        scale_w = MEDIAPIPE_FRAME_W / frame1.shape[1] if frame1.shape[1] > MEDIAPIPE_FRAME_W else 1.0
        scale_h = MEDIAPIPE_FRAME_H / frame1.shape[0] if frame1.shape[0] > MEDIAPIPE_FRAME_H else 1.0
        scale = min(scale_w, scale_h)
        if scale < 1.0:
            small_frame = cv2.resize(frame1, (int(frame1.shape[1]*scale), int(frame1.shape[0]*scale)), interpolation=cv2.INTER_LINEAR)
        else:
            small_frame = frame1
        frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # Skip every third frame for even lower latency
        frame_count += 1
        if frame_count % 3 != 0:
            continue
        # YOLO detection (if enabled)
        if YOLO_ENABLED:
            try:
                results_yolo = yolo(small_frame, device='cuda' if torch.cuda.is_available() else 'cpu', verbose=False, conf=CONFIDENCE)[0]
            except Exception as e:
                print(f"[DEBUG] YOLO inference error: {e}. Exiting loop.")
                break
            for box in results_yolo.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Rescale boxes to original frame size if downscaled
                if scale < 1.0:
                    x1 = int(x1 / scale)
                    y1 = int(y1 / scale)
                    x2 = int(x2 / scale)
                    y2 = int(y2 / scale)
                cls_id = int(box.cls[0])
                label = yolo.model.names[cls_id]
                conf_score = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
                label_text = f"{label} {conf_score:.2f}"
                cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame1, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # MediaPipe hand detection (if enabled)
        if MEDIAPIPE_ENABLED:
            try:
                results = hands.process(frame_rgb)
            except Exception as e:
                print(f"[DEBUG] MediaPipe error: {e}. Exiting loop.")
                break
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    label_hand = handedness.classification[0].label
                    # Map landmarks from small_frame to original frame1 size
                    landmark_list = []
                    for lm in hand_landmarks.landmark:
                        x = int(lm.x * small_frame.shape[1] / scale)
                        y = int(lm.y * small_frame.shape[0] / scale)
                        landmark_list.append((x, y))
                    # Draw landmarks and connections on the original frame
                    for idx, (x, y) in enumerate(landmark_list):
                        cv2.circle(frame1, (x, y), 3, (0, 255, 255), -1)
                    # Draw connections
                    for connection in mp_hands.HAND_CONNECTIONS:
                        start_idx, end_idx = connection
                        x0, y0 = landmark_list[start_idx]
                        x1, y1 = landmark_list[end_idx]
                        cv2.line(frame1, (x0, y0), (x1, y1), (255, 255, 0), 2)
                    cv2.putText(frame1, f"{label_hand} Hand", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        # out.write(frame1)  # Disabled video saving for lower latency
        cv2.imshow("YOLO + MediaPipe", frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[DEBUG] 'q' pressed. Exiting loop.")
            break
    elapsed = time.time() - start_time
    print(f"Processed {frame_count} frames in {elapsed:.2f} seconds. Avg FPS: {frame_count/elapsed:.2f}")
    if BASLER_AVAILABLE:
        camera1.StopGrabbing()
        camera1.Close()
    else:
        camera1.release()
    # out.release()  # Disabled video saving for lower latency
    cv2.destroyAllWindows()
    # print(f"Saved result video to {out_path}")  # You can remove or comment out this line if you want

if __name__ == "__main__":
    main()
