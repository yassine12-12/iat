import cv2
import time
import argparse
import os
from datetime import datetime

# Add Basler camera support
try:
    from pypylon import pylon
    BASLER_AVAILABLE = True
except ImportError:
    BASLER_AVAILABLE = False

def main():
    parser = argparse.ArgumentParser(description="Raw video capture from Basler or USB camera.")
    parser.add_argument('--camera', type=int, default=0, help='Camera index to use (default: 0)')
    parser.add_argument('--folder', type=str, default='videos', help='Folder to save videos in (default: videos)')
    args = parser.parse_args()

    # Ensure output folder exists
    os.makedirs(args.folder, exist_ok=True)
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(args.folder, f"raw_capture_{timestamp}.mp4")

    if BASLER_AVAILABLE:
        print("Using Basler camera...")
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        if len(devices) == 0:
            print("No Basler cameras detected. Exiting.")
            return
        cam_idx = min(args.camera, len(devices)-1)
        camera = pylon.InstantCamera(tl_factory.CreateDevice(devices[cam_idx]))
        camera.Open()
        # Set to full frame, but use a lower resolution for more reliable capture
        try:
            camera.Width.Value = 1280  # or another supported lower value
            camera.Height.Value = 720
        except Exception as e:
            print(f"[DEBUG] Could not set lower resolution: {e}. Using max resolution.")
            camera.Width.Value = camera.Width.Max
            camera.Height.Value = camera.Height.Max
        width = camera.Width.Value
        height = camera.Height.Value
        camera.StartGrabbing()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        fps = 60  # Set FPS to 60 for higher frame rate capture
    else:
        print("Using OpenCV camera...")
        camera = cv2.VideoCapture(args.camera)
        if not camera.isOpened():
            print(f"Could not open camera {args.camera}.")
            return
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = camera.get(cv2.CAP_PROP_FPS) or 25

    print(f"Capturing video at {fps} FPS, resolution: {width}x{height}. Press 'q' to stop.")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    frame_count = 0
    while True:
        if BASLER_AVAILABLE:
            if not camera.IsGrabbing():
                print("[DEBUG] Basler camera stopped grabbing.")
                break
            grab = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab.GrabSucceeded():
                img = converter.Convert(grab)
                frame = img.GetArray()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                print("[DEBUG] Basler camera failed to grab frame.")
                break
            grab.Release()
        else:
            ret, frame = camera.read()
            if not ret:
                print("[DEBUG] OpenCV camera failed to read frame.")
                break
        out.write(frame)
        frame_count += 1
        cv2.imshow("Raw Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[DEBUG] 'q' pressed. Stopping capture.")
            break
    print(f"Saved {frame_count} frames to {output_path}")
    if BASLER_AVAILABLE:
        camera.StopGrabbing()
        camera.Close()
    else:
        camera.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
