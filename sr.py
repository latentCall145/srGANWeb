from anyInpSize import exactModel
from PIL import Image
from tqdm import tqdm
import numpy as np
import os, cv2

parentPath = 'models'

def bigPred(x, gen, chunkSize=(32, 32)): # upscale non-32x32 images; x=np.array, gen=Keras model
    m, h, w, c = x.shape
    cX, cY = chunkSize
    ret = np.zeros((m, 4*h, 4*w, c), dtype=np.float16)
    hDiv = (h % cY == 0)
    wDiv = (w % cX == 0)

    for i in tqdm(range(0, h//cY)):
        for j in range(0, w//cX):
            ret[:, 4*cY*i:4*cY*(i+1), 4*cX*j:4*cX*(j+1), :] = gen.predict(x[:, cY*i:cY*(i+1), cX*j:cX*(j+1), :]).astype(np.float16)
        if not wDiv:
            ret[:, 4*cY*i:4*cY*(i+1), -4*cX:, :] = gen.predict(x[:, cY*i:cY*(i+1), -cX:, :]).astype(np.float16) # ending block for each row
    
    if not hDiv:
        for j in tqdm(range(0, w//cX)): # fill in black bottom row
            ret[:, -4*cY:, 4*cY*j:4*cY*(j+1), :] = gen.predict(x[:, -cY:, cX*j:cX*(j+1), :]).astype(np.float16)
    if not (hDiv or wDiv):
        ret[:, -4*cY:, -4*cX:, :] = gen.predict(x[:, -cY:, -cX:, :]).astype(np.float16) # bottom right block

    return ret

def srImgFromFile(imageName, gen=None, models={}, modelName='srGAN', exactPred=True): # modified function to take in an image path and output a numpy array of the rescaled version
    img = cv2.imread(imageName) # BGR -> RGB, divide by 255 to normalize images
    img = img[:, :, ::-1] / 255
    cX, cY = 32, 32

    if exactPred:
        cX = min(img.shape[1], 512); cY = min(img.shape[0], 512)
        genName = 'srGAN_{}_{}'.format(cX, cY)

        if genName in models.keys():
            gen = models[genName]
        else:
            gen = exactModel(modelName, (None, cY, cX, img.shape[-1]))

            if genName not in models.keys():
                models[genName] = gen

    img = np.expand_dims(img, 0)
    pred = (bigPred(img, gen, chunkSize=(cX, cY))[0] * 255).astype(np.uint8)
    imgPred = Image.fromarray(pred)
    return imgPred
