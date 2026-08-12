from datetime import datetime


# Current webcam sends approximately
# 1 frame every 500 ms.
# 6 consecutive frames ≈ 3 seconds.
VIOLATION_THRESHOLD_FRAMES = 6


class ViolationTracker:

    def __init__(self):
        self.current_violation = None
        self.consecutive_frames = 0
        self.incidents = []

    def update(self, detections):

        no_hardhat = detections.get(
            "NO-Hardhat", 0
        )

        no_vest = detections.get(
            "NO-Safety Vest", 0
        )

        # Determine current violation

        if no_hardhat > 0 and no_vest > 0:

            violation = "Missing Hardhat and Safety Vest"

        elif no_hardhat > 0:

            violation = "Missing Hardhat"

        elif no_vest > 0:

            violation = "Missing Safety Vest"

        else:

            violation = None


        # No violation

        if violation is None:

            self.current_violation = None
            self.consecutive_frames = 0

            return {
                "violation": False,
                "confirmed": False,
                "incident": None
            }


        # Continue existing violation

        if violation == self.current_violation:

            self.consecutive_frames += 1

        else:

            self.current_violation = violation
            self.consecutive_frames = 1


        # Confirm after threshold

        if (
            self.consecutive_frames
            >= VIOLATION_THRESHOLD_FRAMES
        ):

            # Avoid creating an incident
            # on every frame.

            existing_active = any(
                incident["violation"] == violation
                and incident["active"]
                for incident in self.incidents
            )

            if not existing_active:

                incident = {
                    "id": len(self.incidents) + 1,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "violation": violation,
                    "risk": "HIGH",
                    "duration_seconds": round(
                        self.consecutive_frames * 0.5,
                        1
                    ),
                    "active": True
                }

                self.incidents.append(
                    incident
                )

                return {
                    "violation": True,
                    "confirmed": True,
                    "incident": incident
                }


        return {
            "violation": True,
            "confirmed": False,
            "incident": None
        }


    def get_incidents(self):

        return self.incidentss