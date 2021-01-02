from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from sr import srImgFromFile, parentPath
import os, datetime
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # take out tf logs
from tensorflow.keras.models import load_model as lm

UPLOAD_FOLDER = 'static/pics/lr' # where images are uploaded to
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
pastUpload = '' # used if images are removed from disk
lrImgPath = '' # path location of low-res image to be rescaled
srImgPath = '' # path location of rescaled super-res image

genDict = {} # stores model names with models
model = 'srGAN' # default model is srGAN since it's the fastest
mmn = model # mutable model name, only changes when an image is rescaled with the model

# button colors for each button that corresponds to a model
modelNames = {'srGAN', 'esrGAN_DB', 'esrGAN_RRDB', 'esrGAN_RRDB_v2'}
modelCols = {}
for i in modelNames:
    modelCols[i] = 'gray'

modelCols[model] = 'red'
kwargs = {'model_name': model, 'filename': lrImgPath, 'srimg': srImgPath, 'mmn': mmn}
kwargs = {**kwargs, **modelCols}

app = Flask(__name__)
#print(app.config)
app.config['SECRET_KEY'] = b'sadfl99fsj9(IP(I'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CACHE_TYPE'] = 'null' # not setting this value to null seemed to cause weird issues
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # more caching stuff
app.config['TEMPLATES_AUTO_RELOAD'] = True # more caching stuff

def allowed_file(filename):
    for i in ALLOWED_EXTENSIONS:
        if i in filename:
            return True
    return False

# Deletes old uploaded files from disk
def rmImg():
    try:
        os.remove(pastUpload)
    except IOError:
        print('{} not found, file not removed.'.format(pastUpload))

    #srPath = pastUpload.replace('/lr/', '/sr/{}/'.format(mmn))
    srPath = pastUpload.replace('/lr/', '/sr/')
    try:
        os.remove(srPath)
    except IOError:
        print('{} not found, file not removed.'.format(srPath))

def cleanUp():
    for i in os.listdir(UPLOAD_FOLDER):
        if allowed_file(i):
            os.remove(os.path.join(UPLOAD_FOLDER, i))
    srPath = UPLOAD_FOLDER.replace('lr', 'sr')
    for i in os.listdir(srPath):
        if allowed_file(i):
            os.remove(os.path.join(srPath, i))

# Manages what happens when each button is pressed on the website.
@app.route('/', methods=['POST', 'GET'])
def buttonMgr():
    if request.method == 'POST':
        if 'rescale_button' in request.form:
            try:
                return rescale_img()
            except ValueError: # usually if the picture is smaller than 32x32 px
                flash('Image too small to resize.')
        elif 'srgan_button' in request.form:
            return load_model()
        else:
            return upload_image()

    return render_template('form.html', **kwargs)

'''
Takes uploaded image from website and saves it in disk.
If the image isn't actually an image, the website rejects it.
'''
def upload_image():
    global pastUpload, lrImgPath, kwargs
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('Please insert a file.')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        pastUpload = lrImgPath
        rmImg()

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        lrImgPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        kwargs['filename'] = lrImgPath
        return render_template('form.html', **kwargs)

def rescale_img():
    global srImgPath, mmn, kwargs
    #srImgPath = lrImgPath.replace('/lr/', '/sr/{}/'.format(model))
    srImgPath = lrImgPath.replace('/lr/', '/sr/')
    mmn = model
    srImg = srImgFromFile(lrImgPath, gen=genDict[model])
    print(srImgPath)
    srImg.save(srImgPath)

    kwargs['srimg'] = srImgPath
    kwargs['mmn'] = mmn
    return render_template('form.html', **kwargs)

'''
When a button in the 'Load Model' section,
check if the corresponding model is loaded into memory.
If so, do nothing, if not, load the model.
Then, change the button colors to update which model is active.
'''
def load_model():
    global modelCols, model, genDict, kwargs
    modelCols[model] = 'gray'; kwargs[model] = 'gray'
    model = request.form['srgan_button']
    if model not in genDict:
        genDict[model] = lm(os.path.join(parentPath, model))

    modelCols[model] = 'red'; kwargs[model] = 'red'
    kwargs['model_name'] = model
    return render_template('form.html', **kwargs)

if __name__ == '__main__':
    genDict[model] = lm(os.path.join(parentPath, model)) # load a default model (srGAN) before running web server
    app.run(host='0.0.0.0', debug=False) # run on local network
    #app.run(debug=True)
    cleanUp()
