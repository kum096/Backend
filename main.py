from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import shipments  # keep this

app = FastAPI(
    title="TrackNest Logistics API",
    version="1.0.0",
    description="API backend for tracking shipments and logistics",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://trcknestlogistics.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shipments.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return {"status": "online", "message": "TrackNest Backend Running ✅"}
