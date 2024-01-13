from fastapi import FastAPI
from fastapi import Request
from fastapi import Depends
from fastapi import Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
import uvicorn
from DetectAnalytics.utils.common import decodeImage
from DetectAnalytics.pipeline.predict import PredictionPipeline
import http.client
from DetectAnalytics.utils.common import VerifyToken



os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

token_auth_scheme = HTTPBearer()
app = FastAPI()
auth = VerifyToken()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

class ClientApp:
    def __init__(self):
        self.filename = "input.mp4"
        self.classifier = PredictionPipeline(self.filename)

@app.post("/predict")
async def predictRoute(request: Request):
    video = await request.json['video']
    result = clApp.classifier.predictvid(video)
    return result

@app.get("/api/private")
def private(request: Request, token: str = Depends(token_auth_scheme)):
    result = Security(auth.verify)
    
    if result.get("status"):
        return result



if __name__ == "__main__":
    clApp = ClientApp()
    uvicorn.run(app, host='0.0.0.0', port=8080) #local host
    headers = { 'content-type': "application/x-www-form-urlencoded" }
    # app.run(host='0.0.0.0', port=8080) #for AWS
    # app.run(host='0.0.0.0', port=80) #for AZURE