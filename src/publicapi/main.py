from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from publicapi.core.configs import settings
from publicapi.api.v1.api import router

app = FastAPI(title="API Publica",
              version="1.0"
)
app.include_router(router, prefix=settings.API_V1_STR)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8080, log_level="info" ,reload=True)