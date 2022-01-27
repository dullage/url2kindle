import logging
import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, HttpUrl

from url2kindle import url2kindle

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BASIC_AUTH_USERNAME = os.environ["BASIC_AUTH_USERNAME"]
BASIC_AUTH_PASSWORD = os.environ["BASIC_AUTH_PASSWORD"]

app = FastAPI()
security = HTTPBasic()

class DataModel(BaseModel):
    url: HttpUrl

@app.post("/")
def root(
    data: DataModel, credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(
        credentials.username, BASIC_AUTH_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, BASIC_AUTH_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    url2kindle(data.url)
