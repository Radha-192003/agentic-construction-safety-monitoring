from app.graphs.safety_graph import graph

result = graph.invoke(
    {
        "image_path": "uploads/images/006672_jpg.rf.87d5978c486feb53177408cf00a0d87f.jpg",
        "detections": {},
        "risk_level": "",
        "recommendation": "",
        "report": ""
    }
)
print("\nFinal Output")
print(result)