from PIL import Image
from tqdm import tqdm
import numpy as np
import os, cv2

os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # no GPU, comment this line out to use GPU

parentPath = 'models'

def bigPred(x, gen): # upscale non-32x32 images; x=np.array, gen=Keras model
    m, h, w, c = x.shape
    ret = np.zeros((m, 4*h, 4*w, c), dtype=np.float16)
    wDiv = (w % 32 == 0)
    hDiv = (w % 32 == 0)

    for i in tqdm(range(0, h//32)):
        for j in range(0, w//32):
            ret[:, 128*i:128*(i+1), 128*j:128*(j+1), :] = gen.predict(x[:, 32*i:32*(i+1), 32*j:32*(j+1), :]).astype(np.float16)
        if not wDiv:
            ret[:, 128*i:128*(i+1), -128:, :] = gen.predict(x[:, 32*i:32*(i+1), -32:, :]).astype(np.float16) # ending block for each row
    
    if not hDiv:
        for j in tqdm(range(0, w//32)): # fill in black bottom row
            ret[:, -128:, 128*j:128*(j+1), :] = gen.predict(x[:, -32:, 32*j:32*(j+1), :]).astype(np.float16)
    if not (hDiv or wDiv):
        ret[:, -128:, -128:, :] = gen.predict(x[:, -32:, -32:, :]).astype(np.float16) # bottom right block

    return ret

def srImgFromFile(imageName, gen): # modified function to take in an image path and output a numpy array of the rescaled version
    img = cv2.imread(imageName) # BGR -> RGB, divide by 255 to normalize images
    img = img[:, :, ::-1] / 255
    img = np.expand_dims(img, 0)
    pred = (bigPred(img, gen)[0] * 255).astype(np.uint8)
    imgPred = Image.fromarray(pred)
    return imgPred
