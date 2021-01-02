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

I've also added a feature which can make the srGAN model more flexibly resize images of all sizes (by disabling 32x32px resizing chunks when rescaling). You can disable this feature, but I'm not really sure why you would.

With chunking (not recommended):
![Chunking on a small image](/figs/cChunk.png)
![Chunking on an image larger than 32x32px](/figs/turtChunk.png)

Without chunking (default):
![No chunking on a small image](/figs/cNoChunk.png)
![No chunking on an image larger than 32x32px](/figs/turtNoChunk.png)

Currently, the website can't serve multiple users at the same time, but it's not like a lot of people are going to use this at the same time, so it doesn't really matter.
