import cv2
import os
from glob import glob

# Settings
VIDEOS_DIR = 'videos'
FRAMES_DIR = os.path.join(VIDEOS_DIR, 'frames')
FRAME_SKIP = 10  # Extract every 10th frame by default

os.makedirs(FRAMES_DIR, exist_ok=True)

video_files = glob(os.path.join(VIDEOS_DIR, '*.mp4'))

for video_path in video_files:
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    out_dir = os.path.join(FRAMES_DIR, video_name)
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    saved_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % FRAME_SKIP == 0:
            out_path = os.path.join(out_dir, f'frame_{frame_idx:06d}.jpg')
            cv2.imwrite(out_path, frame)
            saved_idx += 1
        frame_idx += 1
    cap.release()
    print(f"Extracted {saved_idx} frames from {video_name} to {out_dir}")

print("Done extracting frames from all videos.")
