# srGAN (and company) Image Rescaler

A web app thing that I made to make it relatively easy to upload your images and try out my srGAN models for yourself. Not much to say other than the fact it uses Flask, TF 2.2 models (which apparently works on TF 2.4 now...).
![srGAN on a moose](/figs/srMoose.png)

## Install necessary packages <h2>
Windows:
`pip install -r requirements.txt`

Mac/Linux:
`pip3 install -r requirements.txt`

## Run the program <h2>
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
2. The website can't serve multiple users at the same time
