import cv2


def read_video(video_path):

    print("========== VIDEO TOOL ==========")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        print("Cannot open video.")

        return

    frame_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        print(f"Frame {frame_count}")

    cap.release()

    print("Total Frames :", frame_count)