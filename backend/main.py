from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.safety import router as safety_router

app = FastAPI(
    title="AI Construction Monitoring System"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register Safety API
app.include_router(safety_router)

# Expose YOLO output images
app.mount("/results", StaticFiles(directory="runs"), name="results")


@app.get("/")
def home():
    return "AI-powered Construction Monitoring System"


@app.get("/health")
def health():
    return {"status": "Healthy"}

