from fastapi import FastAPI
from mangum import Mangum
from app.api import v1
from app.database.connection import init_local_db


## Initialize DB
init_local_db()

## init Application Instance
app_instance = FastAPI()
app_instance.include_router(v1.router, prefix='/api/v1')

## AWS Lambda
handler = Mangum(app_instance)

## Local Development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_app:app_instance", host="0.0.0.0", port=8881, reload=True)