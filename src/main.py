from fastapi import FastAPI

from apps.exchange import router
from core.exception_handler import add_exception_handlers
from core.response import default_responses

app = FastAPI(title='Exchange API',version='?')
app.include_router(router)


@app.get("/root", tags=["Root"], responses=default_responses)
def root():
    return {'status': 0}


add_exception_handlers(app=app)
