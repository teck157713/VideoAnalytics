from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from DetectAnalytics.utils.common import decodeImage
from DetectAnalytics.pipeline.predict import PredictionPipeline
import http.client


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

# conn = http.client.HTTPSConnection("")

# payload = "grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&audience=YOUR_API_IDENTIFIER"

# headers = { 'content-type': "application/x-www-form-urlencoded" }

# conn.request("POST", "/{yourDomain}/oauth/token", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "input.mp4"
        self.classifier = PredictionPipeline(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    return "Training done successfully!"



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    conn = http.client.HTTPSConnection("")
    video = request.json['video']
    result = clApp.classifier.predictvid(video)
    return jsonify(result)


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=8080) #local host
    headers = { 'content-type': "application/x-www-form-urlencoded" }
    # app.run(host='0.0.0.0', port=8080) #for AWS
    # app.run(host='0.0.0.0', port=80) #for AZURE