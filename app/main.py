from fastapi import FastAPI
from app.routes import shipments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TrackNest Logistics API",
    version="1.0.0",
    description="API backend for tracking shipments and logistics",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS setup — allow requests from your frontend origin(s)
origins = [
    "http://127.0.0.1:5500",  # if you serve your track.html locally with a dev server
    "http://localhost:5500",
    # add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your shipments router
app.include_router(shipments.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "online", "message": "TrackNest Backend Running ✅"}
