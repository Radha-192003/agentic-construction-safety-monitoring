from langgraph.graph import StateGraph, END

from app.models.agent_state import SafetyAgentState

from app.agents.safety_agent import (
    detect_safety,
    analyze_detection,
    assess_risk,
    generate_recommendation,
    generate_report
)


builder = StateGraph(SafetyAgentState)


builder.add_node("Tool", detect_safety)
builder.add_node("Analyze", analyze_detection)
builder.add_node("Risk", assess_risk)
builder.add_node("Recommendation", generate_recommendation)
builder.add_node("Report", generate_report)


builder.set_entry_point("Tool")


builder.add_edge("Tool", "Analyze")
builder.add_edge("Analyze", "Risk")
builder.add_edge("Risk", "Recommendation")
builder.add_edge("Recommendation", "Report")
builder.add_edge("Report", END)


graph = builder.compile()