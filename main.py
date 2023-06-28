import traceback
from fastapi import Depends, FastAPI, HTTPException, Request, Response


import logging
from app.measurements.models import Measurement
from app.patients.models import Patient
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables, SessionLocal, engine
from .routes import router as routes
app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

@app.on_event("startup")
async def startup_event():
    create_tables()

# Defina o manipulador de exceções

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response



# Configurações CORS para permitir solicitações de diferentes origens
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Adicione outras origens permitidas, se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(patients_router, prefix="/api/v1/patients", tags=["patients"])
# app.include_router(measurements_router, prefix="/api/v1/measurements", tags=["measurements"])
app.include_router(routes, prefix="/api/v1", tags=["api"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
