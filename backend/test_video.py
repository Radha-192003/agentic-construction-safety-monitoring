from app.services.safety_service import detect_video

result = detect_video(
    "uploads/videos/348898_medium.mp4"
)

print("\n========== FINAL VIDEO RESULT ==========")
print(result)