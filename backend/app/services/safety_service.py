from ultralytics import YOLO
from pathlib import Path
import os
import cv2
# Load trained model
MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "ai_models"
    / "safety"
    / "best.pt"
)

print("Loading model from:", MODEL_PATH)

# Load model only once when the server starts
model = YOLO(str(MODEL_PATH))


def detect(image_path):
    # Run prediction
    results = model.predict(
        source=image_path,
        conf=0.4,
        save=True
    )

    # Get first prediction result
    result = results[0]

    # Count detected objects
    detections = {}

    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        detections[class_name] = detections.get(class_name, 0) + 1

    # Path of saved prediction image
    output_image = Path(result.save_dir) / Path(image_path).name
    

    print("Saved Image:", output_image)

    return {
    "detections": detections,
    "output_image": str(output_image).replace("\\", "/")
}

def detect_video(video_path):

    print("========== VIDEO DETECTION ==========")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Unable to open video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("FPS:", fps)
    print("Resolution:", width, "x", height)
    print("Total Frames:", total_frames)

    output_dir = Path("runs/videos")
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_video = output_dir / f"temp_{Path(video_path).stem}.mp4"

    final_video = output_dir / f"processed_{Path(video_path).stem}.mp4"

    writer = cv2.VideoWriter(
        str(temp_video),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    frame_count = 0

    # Store maximum detections observed in a frame
    max_detections = {}

    # Count frames containing violations
    violation_frames = 0
    analyzed_frames = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1
        analyzed_frames += 1

        results = model.predict(
            source=frame,
            conf=0.4,
            verbose=False
        )

        result = results[0]

        # Count detections in this frame
        frame_detections = {}

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            frame_detections[class_name] = (
                frame_detections.get(class_name, 0) + 1
            )

        # Keep maximum count seen for each class
        for class_name, count in frame_detections.items():

            if count > max_detections.get(class_name, 0):
                max_detections[class_name] = count

        # Check PPE violations
        has_violation = (
        "NO-Hardhat" in frame_detections
        or "NO-Safety Vest" in frame_detections
    )

        if has_violation:
            violation_frames += 1

        # Draw detections
        annotated_frame = result.plot()

        writer.write(annotated_frame)

        if frame_count % 30 == 0:

            progress = (frame_count / total_frames) * 100

            print(
                f"Processed {frame_count}/{total_frames} "
                f"frames ({progress:.1f}%)"
            )

    cap.release()
    writer.release()

    print("\nYOLO processing completed.")

    # Calculate compliance
    if analyzed_frames > 0:

        violation_percentage = (
            violation_frames / analyzed_frames
        ) * 100

        compliance_score = round(
            100 - violation_percentage
        )

    else:

        compliance_score = 0

    # Determine risk
    if compliance_score >= 90:

        risk_level = "LOW"

    elif compliance_score >= 70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    print("Compliance Score:", compliance_score)
    print("Risk Level:", risk_level)

    # Convert video to browser-compatible H.264
    print("Converting video to H.264...")

    os.system(
        f'ffmpeg -y -i "{temp_video}" '
        f'-c:v libx264 -preset fast -crf 23 '
        f'-pix_fmt yuv420p '
        f'"{final_video}"'
    )

    if temp_video.exists():
        temp_video.unlink()

    print("Final Video Saved:", final_video)

    return {
        "output_video": str(final_video).replace("\\", "/"),
        "detections": max_detections,
        "compliance_score": compliance_score,
        "risk_level": risk_level,
        "analyzed_frames": analyzed_frames,
        "violation_frames": violation_frames
    }

def detect_live_frame(frame):
    """
    Run YOLO detection on a single webcam frame.
    """

    results = model.predict(
        source=frame,
        conf=0.4,
        verbose=False
    )

    result = results[0]

    detections = {}

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        detections[class_name] = (
            detections.get(class_name, 0) + 1
        )

    annotated_frame = result.plot()

    return {
        "frame": annotated_frame,
        "detections": detections
    }