from flask import Flask, jsonify, request
from PIL import Image
import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    json_data = request.get_json() #Get the POSTed json
    dict_data = json.loads(json_data) #Convert json to dictionary

    img = dict_data["img"] #Take out base64# str
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img) 
    img_shape = img.size #Appropriately process the acquired image
    
    text = dict_data["text"] + "fuga" #Properly process with the acquired text

    #Return the processing result to the client
    response = {
        "text":text,
        "img_shape":img_shape        
        }

    return jsonify(response)

@app.route("/check", methods=["GET"])
def check():
    msg = "asdasd "
    for i in range(2000):
        msg = msg+"muie  "
    return msg

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)