from langgraph.graph import StateGraph, END

from app.models.agent_state import SafetyAgentState

from app.agents.safety_agent import (
    analyze_detection,
    generate_recommendation,
    generate_report
)


def assess_video_risk(state: SafetyAgentState):

    print("\n========== VIDEO RISK NODE ==========")

    compliance = state.get("compliance_score", 0)

    if compliance >= 90:
        risk = "LOW"

    elif compliance >= 70:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    state["risk_level"] = risk

    print("Compliance:", compliance)
    print("Video Risk Level:", risk)

    return state


builder = StateGraph(SafetyAgentState)

builder.add_node("Analyze", analyze_detection)
builder.add_node("Risk", assess_video_risk)
builder.add_node("Recommendation", generate_recommendation)
builder.add_node("Report", generate_report)

builder.set_entry_point("Analyze")

builder.add_edge("Analyze", "Risk")
builder.add_edge("Risk", "Recommendation")
builder.add_edge("Recommendation", "Report")
builder.add_edge("Report", END)

video_graph = builder.compile()