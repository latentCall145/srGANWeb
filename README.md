#srGAN (and company) Image Rescaler

A web app thing that I made to make it relatively easy to upload your images and try out my srGAN models for yourself. Not much to say other than the fact it uses Flask, TF 2.2 models (sorry TF 2.3 and above).
![srGAN on a moose](/figs/srMoose.png)

## Install necessary packages
Windows:
`pip install -r requirements.txt`

Mac/Linux:
`pip3 install -r requirements.txt`

## Run the program
Windows:
`python app.py`

Mac/Linux:
`python3 app.py`

You can also rescale images using different models and compare their looks.

The image below uses srGAN.
![srGAN on a turtle](/figs/srTurt.png)

The image below uses esrGAN on the same image above.
![esrGAN on the same turtle](/figs/esrTurt.png)


Currently, there are some problems with the app although it doesn't matter too much with such a small app that is meant to be run locally;
1. Wide images will overlap each other (which isn't that much of an issue but still kind of annoying)
2. Images that don't have a dimension divisible by 32 (i.e. 32x32, 128x32, etc.) will have a black section on the right and bottom since I didn't code the prediction function to assume that images wouldn't be divisible
3. Uploaded images aren't deleted once a new image is uploaded (although there is a commented line in the app.py (rmImg()) that should remove most images)
4. The website can't serve multiple users at the same time
