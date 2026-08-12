from fastapi import APIRouter, UploadFile, File
import shutil
import os
import cv2
import numpy as np
import base64

from app.graphs.safety_graph import graph
from app.graphs.video_safety_graph import video_graph

from app.services.incident_service import ViolationTracker

from app.services.safety_service import (
    detect_video,
    detect_live_frame
)


router = APIRouter(
    prefix="/safety",
    tags=["Safety Monitoring"]
)


# ==========================================
# LIVE VIOLATION TRACKER
# ==========================================

live_tracker = ViolationTracker()


# ==========================================
# IMAGE DETECTION
# ==========================================

@router.post("/detect")
async def detect_safety(
    file: UploadFile = File(...)
):

    upload_dir = "uploads/images"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    image_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(
        image_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    print("Calling detect()...")

    result = graph.invoke(
        {
            "image_path": image_path,
            "output_image": "",
            "detections": {},
            "risk_level": "",
            "recommendation": "",
            "report": ""
        }
    )

    image_url = (
        result["output_image"]
        .replace("\\", "/")
        .split("/runs/")[-1]
    )

    image_url = (
        f"http://127.0.0.1:8000/results/"
        f"{image_url}"
    )

    return {

        "message":
            "AI Safety Analysis Completed",

        "filename":
            file.filename,

        "output_image":
            image_url,

        "detections":
            result["detections"],

        "risk_level":
            result["risk_level"],

        "recommendation":
            result["recommendation"],

        "report":
            result["report"]
    }


# ==========================================
# VIDEO DETECTION
# ==========================================

@router.post("/video-detect")
async def detect_video_safety(
    file: UploadFile = File(...)
):

    upload_dir = "uploads/videos"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    video_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(
        video_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    print(
        "Processing video:",
        video_path
    )

    # ======================================
    # STEP 1: YOLO VIDEO DETECTION
    # ======================================

    video_result = detect_video(
        video_path
    )


    # ======================================
    # STEP 2: VIDEO SAFETY AI GRAPH
    # ======================================

    graph_result = video_graph.invoke(
        {
            "image_path": "",

            "output_image": "",

            "detections":
                video_result["detections"],

            "risk_level":
                video_result["risk_level"],

            "recommendation": "",

            "report": "",

            "compliance_score":
                video_result[
                    "compliance_score"
                ],

            "analyzed_frames":
                video_result[
                    "analyzed_frames"
                ],

            "violation_frames":
                video_result[
                    "violation_frames"
                ]
        }
    )


    # ======================================
    # STEP 3: RESPONSE
    # ======================================

    return {

        "message":
            "AI Video Safety Analysis Completed",

        "filename":
            file.filename,

        "output_video":
            video_result[
                "output_video"
            ],

        "detections":
            video_result[
                "detections"
            ],

        "compliance_score":
            video_result[
                "compliance_score"
            ],

        "risk_level":
            graph_result[
                "risk_level"
            ],

        "analyzed_frames":
            video_result[
                "analyzed_frames"
            ],

        "violation_frames":
            video_result[
                "violation_frames"
            ],

        "recommendation":
            graph_result[
                "recommendation"
            ],

        "report":
            graph_result[
                "report"
            ]
    }


# ==========================================
# LIVE WEBCAM DETECTION
# ==========================================

@router.post("/live-detect")
async def live_detect(
    file: UploadFile = File(...)
):

    try:

        # ==================================
        # STEP 1: READ FRAME
        # ==================================

        contents = await file.read()


        # ==================================
        # STEP 2: CONVERT TO NUMPY
        # ==================================

        np_array = np.frombuffer(
            contents,
            np.uint8
        )


        # ==================================
        # STEP 3: DECODE IMAGE
        # ==================================

        frame = cv2.imdecode(
            np_array,
            cv2.IMREAD_COLOR
        )


        if frame is None:

            return {
                "error":
                    "Unable to decode frame"
            }


        # ==================================
        # STEP 4: YOLO DETECTION
        # ==================================

        result = detect_live_frame(
            frame
        )


        detections = result[
            "detections"
        ]


        # ==================================
        # STEP 5: PERSISTENT VIOLATION
        # ==================================

        incident_result = (
            live_tracker.update(
                detections
            )
        )


        # ==================================
        # STEP 6: ANNOTATED FRAME
        # ==================================

        annotated_frame = result[
            "frame"
        ]


        # ==================================
        # STEP 7: ENCODE JPEG
        # ==================================

        success, encoded_image = (
            cv2.imencode(
                ".jpg",
                annotated_frame
            )
        )


        if not success:

            return {
                "error":
                    "Unable to encode detection frame"
            }


        # ==================================
        # STEP 8: BASE64 IMAGE
        # ==================================

        image_base64 = (
            base64.b64encode(
                encoded_image.tobytes()
            ).decode("utf-8")
        )


        # ==================================
        # STEP 9: RISK LEVEL
        # ==================================

        risk_level = "LOW"


        if (
            detections.get(
                "NO-Hardhat",
                0
            ) > 0
            or
            detections.get(
                "NO-Safety Vest",
                0
            ) > 0
        ):

            risk_level = "HIGH"


        elif detections.get(
            "Person",
            0
        ) > 0:

            persons = detections.get(
                "Person",
                0
            )

            hardhats = detections.get(
                "Hardhat",
                0
            )

            vests = detections.get(
                "Safety Vest",
                0
            )

            if (
                hardhats < persons
                or
                vests < persons
            ):

                risk_level = "MEDIUM"


        # ==================================
        # STEP 10: RESPONSE
        # ==================================

        return {

            "detections":
                detections,

            "image":
                image_base64,

            "violation":
                incident_result[
                    "violation"
                ],

            "confirmed_violation":
                incident_result[
                    "confirmed"
                ],

            "incident":
                incident_result[
                    "incident"
                ],

            "risk_level":
                risk_level
        }


    except Exception as e:

        print(
            "LIVE DETECTION ERROR:",
            e
        )

        return {
            "error": str(e)
        }