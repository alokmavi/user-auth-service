from fastapi import FastAPI
from app.api.v1 import users
from app.core.config import app_settings

app = FastAPI(title=app_settings.PROJECT_NAME)

# Mount the user router to the main application
app.include_router(users.router, prefix=f"{app_settings.API_V1_STR}/users", tags=["Users"])

@app.get("/health", tags=["System"])
def system_health_check():
    return {"status": "operational", "environment": "development"}