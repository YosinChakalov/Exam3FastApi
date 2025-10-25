from fastapi import FastAPI, HTTPException
import uvicorn
from db_config import engine, SessionLocal
from accounts.views import account_app
app = FastAPI()


app.include_router(account_app,prefix='/auth')


if __name__ == "__main__":
    print('table created succesfully')
    uvicorn.run("manage:app", host='127.0.0.1', port=8000, reload=True)