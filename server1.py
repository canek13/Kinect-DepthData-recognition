from flask import Flask, jsonify, request, render_template
import os
from flask import  flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import numpy as np

import asyncio
import json
from flask import jsonify
import webbrowser

from psutil import process_iter

import http.server
import socketserver
from threading import Thread

import handler
import base64

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def start():
    app = Flask(__name__)
    
 
    
    UPLOAD_FOLDER = './'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    @app.route('/', methods=['GET', 'POST'])
    def upload_images():
        if request.method == 'POST':
                print(request)
                handled_images = []
      
                pixels = request.form.to_dict(flat=False)['pixels'][0]

                bit = base64.b64decode(pixels)
                des_b = np.frombuffer(bit, dtype=np.uint8)
                answer = handler.get_start(des_b)

                response = app.response_class(
                            response=json.dumps(answer,cls=NumpyEncoder),
                            status=200,
                            mimetype='application/json'
                        )
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    port_main = 8000
        
    app.run(port=port_main,threaded=False)
start()