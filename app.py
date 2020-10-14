from flask import Flask, render_template, request, jsonify
import base64, logging
import numpy as np
from deepface import DeepFace
from glob import glob
from random import choice
from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3
import subprocess

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#here's a ding ding (dict)
error_path = {'race': {'asian': 0, 'indian': 0, 'black': 0, 'white': 0, 'middle eastern': 0, 'latino hispanic': 0}, 'dominant_race': '?'}

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/photocap')
def photo_cap():
    photo_base64 = request.args.get('photo')

    _, encoded = photo_base64.split(",", 1)
    binary_data = base64.b64decode(encoded)

    f = BytesIO()
    f.write(binary_data)
    f.seek(0)
    image =  Image.open(f)
    background = Image.new("RGB", image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[3])
    image = np.array(background)

    try:
        obj = DeepFace.analyze(image, actions = ['race'])

        return jsonify(obj)

    except ValueError:
        other_json = error_path
        
        return jsonify(other_json)

    except Exception as e:
        print(e)
        other_json = error_path
        
        return jsonify(other_json)

if __name__ == "__main__":
    p = subprocess.Popen(['python -m SimpleHTTPServer'], shell=True)
    print(" * Running on http://127.0.0.1:8000/")
    app.run(host='localhost', port=8000)
