import os
import time
from io import BytesIO
from PIL import Image
from flask import Flask, request
from flask_cors import CORS
import random
import datetime

now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d-%H-%M-%S")


app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_data()
    # print(data)
    with Image.open(BytesIO(data)) as im:
        filename = str(random.randrange(0,99999999)) + ".png"
        im.save(os.path.join(app.root_path, filename))
        print(os.path.join(app.root_path, filename))

    return 'Image uploaded'



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")