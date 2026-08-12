from typing import TypedDict


class SafetyAgentState(TypedDict):
    image_path:str
    output_image:str
    detections: dict
    risk_level: str
    recommendation: str
    report: str
