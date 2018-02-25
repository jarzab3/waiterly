#!/usr/bin/env python2.7

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# setup clarifai
app = ClarifaiApp(api_key='f52f407580fb4adeb0263201144b2e71')
model = app.models.get("Beer")

def get_prediction (img):
    # predict with the model
    image = ClImage(file_obj=open(img, 'rb'))
    prediction = model.predict([image])

    # get probability that glass is empty or full
    values = [  prediction['outputs'][0]['data']['concepts'][0]['value'],
                prediction['outputs'][0]['data']['concepts'][1]['value']]
    ix = values.index(max(values))
    return prediction['outputs'][0]['data']['concepts'][ix]['id']

img = 'IMG_2895.jpg'

print(get_prediction (img))