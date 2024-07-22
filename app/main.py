from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import tune_router, user_router, user_auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.include_router(user_auth_router.router)
app.include_router(user_router.router)
app.include_router(tune_router.router)
