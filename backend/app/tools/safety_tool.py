from app.services.safety_service import detect


def safety_detection_tool(image_path: str):

    print("\n========== SAFETY TOOL ==========")

    result = detect(image_path)

    print(result)

    return result