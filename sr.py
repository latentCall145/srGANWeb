from PIL import Image
from tqdm import tqdm
import numpy as np
import os, cv2

os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # no GPU
#os.environ['CUDA_VISIBLE_DEVICES'] = '0' # yes GPU 

parentPath = 'models/tf_220' # change to tf_230 if your machine doesn't support TF 2.2.0

def bigPred(x, gen): # upscale non-32x32 images; x=np.array, gen=Keras model
    m, h, w, c = x.shape
    ret = np.zeros((m, 4*h, 4*w, c), dtype=np.float16)
    for i in tqdm(range(0, h//32)):
        for j in tqdm(range(0, w//32)):
            ret[:, 128*i:128*(i+1), 128*j:128*(j+1), :] = gen.predict(x[:, 32*i:32*(i+1), 32*j:32*(j+1), :]).astype(np.float16)
    return ret

def srImgFromFile(imageName, gen): # modified function to take in an image path and output a numpy array of the rescaled version
    img = cv2.imread(imageName) # BGR -> RGB, divide by 255 to normalize images
    img = img[:, :, ::-1] / 255
    img = np.expand_dims(img, 0)
    pred = (bigPred(img, gen)[0] * 255).astype(np.uint8)
    imgPred = Image.fromarray(pred)
    return imgPred
