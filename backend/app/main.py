from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth, candidate, company, match

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CogniMatch API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(candidate.router)
app.include_router(company.router)
app.include_router(match.router)

@app.get("/")
def home():
    return {"message": "CogniMatch API is running"}
