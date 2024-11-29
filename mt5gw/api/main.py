from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import argparse

from .endpoints import router

app = FastAPI(
    title="MT5 Gateway API",
    description="REST API wrapper for MetaTrader 5 Gateway",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

# Include router
app.include_router(router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def start_server():
    """Entry point for the API server"""
    parser = argparse.ArgumentParser(description='MT5 Gateway API Server')
    parser.add_argument('--host', type=str, default="0.0.0.0",
                      help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=8000,
                      help='Port to bind the server to')
    parser.add_argument('--reload', action='store_true',
                      help='Enable auto-reload on code changes')
    
    args = parser.parse_args()
    
    print(f"Starting MT5 Gateway API server on {args.host}:{args.port}")
    uvicorn.run(
        "mt5gw.api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    start_server()
