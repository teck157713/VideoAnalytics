from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Depends, HTTPException, status, Path
from fastapi import Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import uvicorn
import time
from DetectAnalytics.utils.common import decodeImage
from DetectAnalytics.pipeline.predict import PredictionPipeline
import http.client
from DetectAnalytics.utils.common import VerifyToken
from fastapi import APIRouter
from pydantic import HttpUrl, BaseModel
from DetectAnalytics import logger
from typing import Any, Callable, TypeVar, Dict
from DetectAnalytics.routers.models import OauthException, OauthToken
from DetectAnalytics.routers import auth



os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
# https://surveillance-api.com/cameras/connect/${cameraId}
token_auth_scheme = HTTPBearer()
app = FastAPI()
authen = VerifyToken()
origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
    allow_origins=origins)

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

server_callback_router = APIRouter()

class ClientApp:
    def __init__(self):
        self.filename = "input.mp4"
        self.classifier = PredictionPipeline(self.filename)



@app.post("/predict")
async def predictRoute(request: Request):
    video = await request.json['video']
    result = clApp.classifier.predictvid(video)
    return result

@app.post("/processfeed", callbacks=server_callback_router.routes)
def private(request: Request, token: str = Depends(token_auth_scheme), callback_url: HttpUrl = None):
    
    try:
        payload = Security(authen.verify)
        username: str = payload.get("iat")
        if username is None:
            raise credentials_exception
        # ...
    except:
        raise credentials_exception
    
    result = Security(authen.verify)
    result: str = result.get("")
    return result



class WebHook(BaseModel):
    event: str
    data: Dict[str, str]

@app.post("/webhook")
async def incomingsignal(webhook: WebHook):
    if webhook.event == 'session.start':
        if webhook.data['playlist']:
            
        # Do
    elif webhook.event == 'session.stop':
        # Do
        return webhook.data['cameraId']




# @app.post("/insertvid")
# async def todo(access_token: Depends(token_auth_scheme), user: str = Depends(auth.validate_access_token)):
#     return "success"




F = TypeVar("F", bound=Callable[..., Any])

@app.middleware("http")
async def process_time_log_middleware(request: Request, call_next: F) -> Response:
    """
    Add API process time in response headers and log calls
    """
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = str(round(time.time() - start_time, 3))
    response.headers["X-Process-Time"] = process_time

    logger.info(
        "Method=%s Path=%s StatusCode=%s ProcessTime=%s",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )

    return response

app.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["auth"],
)

if __name__ == "__main__":
    clApp = ClientApp()
    uvicorn.run(app, host='0.0.0.0', port=8080) #local host
    headers = { 'content-type': "application/x-www-form-urlencoded" }
    # app.run(host='0.0.0.0', port=8080) #for AWS
    # app.run(host='0.0.0.0', port=80) #for AZURE