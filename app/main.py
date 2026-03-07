from fastapi import FastAPI
from app.api.v1 import users, auth
from app.core.config import app_settings

app = FastAPI(title=app_settings.PROJECT_NAME)

app.include_router(auth.router, prefix=app_settings.API_V1_STR, tags=["Authentication"])
app.include_router(users.router, prefix=f"{app_settings.API_V1_STR}/users", tags=["Users"])

@app.get("/health", tags=["System"])
def system_health_check():
    return {"status": "operational", "environment": "development"}