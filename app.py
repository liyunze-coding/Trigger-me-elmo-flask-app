from flask import Flask, render_template, request, jsonify, url_for
import base64, cv2, logging
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

audio_paths = {
    "asian":"static/Sound/Asian/*.mp3",
    "black":"static/Sound/Black/*.mp3",
    "latino hispanic":"static/Sound/Hispanic/*.mp3",
    "error":"static/Sound/Other/*.mp3",
    "white":"static/Sound/White/*.mp3",
    "indian":"static/Sound/Asian/*.mp3",
    "middle eastern":"static/Sound/White/*.mp3"
}

error_path = {'race': {'asian': 0, 'indian': 0, 'black': 0, 'white': 0, 'middle eastern': 0, 'latino hispanic': 0}, 'dominant_race': '?'}

audio_to_name = {
    "static/Sound/Asian/Assembly_Line.mp3" : "assembly_line",
    "static/Sound/Asian/Iphones.mp3" : "iphones",
    "static/Sound/Asian/Puppet.mp3" : "puppet",
    "static/Sound/White/white_meth.mp3" : "meth",
    "static/Sound/White/white_south.mp3" : "south",
    "static/Sound/Hispanic/hispanic.mp3" : "hispanic",
    "static/Sound/Black/black.mp3" : "black",
    "static/Sound/Other/No_idea.mp3" : "no_idea",
    "static/Sound/Other/What.mp3" : "what"
}

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
        audio = choice(glob(audio_paths[obj['dominant_race']]))
        duration = MP3(audio).info.length * 1000 + 200
        audio_name = audio_to_name[audio]
        obj.update({'audio': audio_name})
        obj.update({'duration': duration})
        return jsonify(obj)

    except ValueError:
        other_json = error_path
        other = choice(glob(audio_paths['error']))
        duration = MP3(other).info.length * 1000 + 200
        audio_name = audio_to_name[audio]
        other_json.update({'audio': audio_name})
        other_json.update({'duration': duration})
        
        return jsonify(other_json)

    except Exception as e:
        print(e)
        other_json = error_path
        other = choice(glob(audio_paths['error']))
        duration = MP3(other).info.length * 1000
        other_json.update({'duration': duration})
        
        return jsonify(other_json)

if __name__ == "__main__":
    print(" * Running on http://127.0.0.1:8000/")
    p = subprocess.Popen(['python -m SimpleHTTPServer'], shell=True)
    app.run(host='localhost', port=8000)
