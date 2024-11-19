from fastapi import FastAPI

import uvicorn

from settings import Settings
from controllers import *

app = FastAPI()
settings = Settings()

app.include_router(person_router)
app.include_router(pet_router)

uvicorn.run(
    app,
    host=settings.TEST_API_HOST,
    port=settings.TEST_API_PORT
)
