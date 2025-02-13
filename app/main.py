from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import sendsms_router
from database.database import Base, engine
from routers import tune_router, user_router, user_auth_router,subscriber_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Welcome to crossgate skiza tune app!"}

app.include_router(user_auth_router.router)
app.include_router(user_router.router)
app.include_router(tune_router.router)
app.include_router(sendsms_router.router)
app.include_router(subscriber_router.router)
