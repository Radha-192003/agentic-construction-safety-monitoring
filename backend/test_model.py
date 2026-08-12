from app.services.safety_service import detect

result=detect(
    r"C:\Users\majji\OneDrive\Desktop\Agentic-Construction-Risk-Intelligence-Platform\datasets\safety_monitoring\safety\css-data\test\images\006672_jpg.rf.87d5978c486feb53177408cf00a0d87f.jpg"
)

print(result)