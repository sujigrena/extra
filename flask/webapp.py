# The flask application developed to perform face comparison between two human faces
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
import os
import logging
from datetime import datetime
import numpy as np
from flask import Flask, request, render_template, jsonify
from scipy import misc
from werkzeug import secure_filename
import shutil



flask_file_path = '/home/sudheer/Documents/darknet/flask'#os.path.normpath(os.path.dirname(__file__)+'/../flask/')
UPLOAD_FOLDER =   flask_file_path +  '/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'GIF', 'PNG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_path=''

def allowed_file(filename):
    ## check the allowed file extensions for the input file
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_post_file(input_file):
    ### check the post file input and save it in local folder
    if allowed_file(input_file.filename):
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(input_file.filename))
	print(fullpath)
        #staticfileurl = 'uploads/' + secure_filename(input_file.filename)
	staticfileurl = 'predictions.png' 
        input_file.save(fullpath)
        print('Returning the input file path')
        return fullpath, staticfileurl
    else:
        logger.debug('Invalid file path entered')        
        return "NotAllowed", "NotAllowed"


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    error_text = ""
    if request.method == 'POST':
        start_time = datetime.now()
        ###check the post file variables and load it into array list for processing
        filepath1, staticfileurl = check_post_file(request.files['file1'])
	

        '''if (filepath1 == "NotAllowed"):
            error_text = ' Missing input_file or NotAllowed file type'
            logger.info(error_text)
            return jsonify(success='1', errorMessage=error_text, data='null')'''

        #image_paths = [filepath1]
	#os.system("gnome-terminal -e 'bash -c \"pwd && ./darknet detect /home/sudheer/Documents/darknet/cfg/yolov3.cfg /home/sudheer/Documents/darknet/yolov3.weights "+filepath1 +"; exec bash\"'") 
	#while('predictions.png' not in '/home/sudheer/Documents/darknet/'):
	#	print('continue')
	#	continue
	#os.system('')
	#os.system('pwd')
	#os.system('./darknet detect /home/sudheer/Documents/darknet/cfg/yolov3.cfg /home/sudheer/Documents/darknet/yolov3.weights '+filepath1)
 
	os.system('./darknet detector test cfg/combine9k.data cfg/yolo9000.cfg yolo9000.weights  -thresh 0.1 '+filepath1)
	shutil.move("/home/sudheer/Documents/darknet/predictions.png","/home/sudheer/Documents/darknet/flask/static/predictions.png")

        #print(image_paths)

        #img = misc.imread(os.path.expanduser(image_paths[0]), mode='RGB')
        
        #filename_base, file_extension = os.path.splitext(image_paths[0])
        return render_template("response.html", files='', input_image=staticfileurl)
            # success = '1' if (error_text and error_text.strip()) else '0'

        # return jsonify(success=success,errorMessage=error_text,data=message)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
