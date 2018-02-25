import base64

import itertools
from flask import Flask, Blueprint, render_template, abort, request, redirect, Response, stream_with_context, \
    render_template_string, url_for
from waitrely import settings
from flask import Flask, jsonify
import json
import requests
import random
import nexmo
import time
import cv2
import random
from time import gmtime, strftime


client = nexmo.Client(key="b526e0a6", secret="BK0lyP7Uz4xH2WVe")

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

log = settings.logging

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['TEMPLATES_AUTO_RELOAD'] = settings.TEMPLATES_AUTO_RELOAD

def sendMessage(number):

    # number = "+4917663177714"
    messageTxt = "Table 17. Empty glass"

    print (number)
    # messageTxt = message
    try:
        client.send_message({'from': 'Waiterly','to': number,'text': messageTxt})

        log.info("Message has been sent. Content: %s" % messageTxt)

    except Exception as error:
        log.error("Error while sending message")


def closest(waiter_locations, table_location):
    dist = []

    if len(waiter_locations) != 0:
        if len(waiter_locations[0]) < 2:
            return 0

        else:
            for x in waiter_locations:
                dist.append((x[0] - table_location[0]) ** 2 + (x[1] - table_location[1]) ** 2)

            return dist.index(min(dist))

    else:
        print("Error in calc locations")

def getStaffLocation():

    url = "https://www.tondakozak.cz/waiterly/?getlocation"

    response = requests.post(url)

    data = json.loads(response.text)

    toReturn = json.dumps(data)

    staff = []

    for e in data:

        element = data.get(e)

        locationX = float(element.get("x"))
        locationY = float(element.get('y'))
        userID = element.get('tel')

        # RANDOM TO REMOVE
        # locationX = random.randint(5, 100)
        # locationY = random.randint(5, 100)

        staff.append([locationX, locationY, userID])

    log.debug("Staff member found %s" % staff)

    table = [10, 10]

    closestWaiter = closest(staff, table)

    numberToSend = staff[closestWaiter][2]

    log.info("Found closest waiter with id: %s" % staff[closestWaiter][2])

    log.info("Details, location request %s" % response)

    # print ( data)
    # print(staff)

    return [data, numberToSend]


def get_frame(camera):

    success, image = camera.read()

    ret, jpeg = cv2.imencode('.jpg', image)

    cv2.imwrite('image.jpg', image)

    return jpeg.tobytes()

def gen():

    while True:
        video = cv2.VideoCapture(0)

        frame = get_frame(video)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        time.sleep(0.0001)


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def getPicture():
    cap = cv2.VideoCapture(0)  # video capture source camera (Here webcam of laptop)
    time.sleep(0.1)

    ret, frame = cap.read()  # return a single frame in variable `frame`

    cv2.imwrite('image.jpg', frame)

    cap.release()

# msgsent = False

@app.route('/drawing')
def mainPage():
    global msgsent

    reply = get_prediction("image.jpg")

    # prediction = get_prediction('/Users/Isaac/Desktop/Languages_Tools_Projects/waiterly_v2/capture.jpg')

    setempty = (reply == 'empty')

    endpoint = 'https://www.tondakozak.cz/waiterly/'
    params = {'setempty': setempty}

    r = requests.post(endpoint, params=params)

    response = json.loads(r.text)

    # toReturn = json.dumps(data)

    print(response)

    # response = json.loads(r.)

    isSame = response['isSame']

    number = response['number']

    print (isSame)

    if (isSame == 'false'):
        log.debug("Number is: %s . Message sent!" % number)

        sendMessage(number)

    # print prediction, r.url
    # print r.text
    # print response, isSame, number

    print("\nResponse:  " + reply + "\n")

    locationReply = "{}"

    if reply == "empty":

        log.info("Glass is empty")

        replyStaff = getStaffLocation()

        # Location
        locationReply = replyStaff[0]

        # number
        number = replyStaff[1]

        # if not msgsent:
        #     sendMessage(number)
        #     msgsent =True

    elif reply == "full":
        log.info("Glass if full")
        pass

    return render_template('drawing.html', locationData=locationReply)

    # timeS = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #
    # return render_template('index.html', info=reply, timeStamp = timeS, location = locationReply)


def get_prediction(img):
    # global valueFromPrediction
    # print(img)

    with open(img, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
        'Authorization': 'Key f52f407580fb4adeb0263201144b2e71',
        'Content-Type': 'application/json',
    }
    data = '\n  {\n    "inputs": [\n      {\n        "data": {\n          "image": {\n            "base64": "'+encoded_string+'"\n          }\n        }\n      }\n    ]\n  }'
    response = requests.post('  https://api.clarifai.com/v2/models/Beer/outputs', headers=headers, data=data)
    prediction = response.json()

    # print(prediction)

    values = [prediction['outputs'][0]['data']['concepts'][0]['value'],
                prediction['outputs'][0]['data']['concepts'][1]['value']]

    ix = values.index(max(values))

    # valueFromPrediction = prediction['outputs'][0]['data']['concepts'][ix]['id']
    return prediction['outputs'][0]['data']['concepts'][ix]['id']



def get_sensor_data():
    '''Presumably you know what actually goes here.'''
    return {'temperature': 5, 'fan speed': 'no, three, sir'}


@app.route("/runTask")
def server_1():
    def generate_output():
        age = 0
        template = '<p>{{ stats }} : {{ data }}</p>'
        context = {'Data': 2}
        while True:
            context['stats'] = timeS = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            yield render_template_string(template, **context)
            time.sleep(1)
            age += 5

            requests.get('http://localhost:5000/drawing')

    return Response(stream_with_context(generate_output()))

@app.route('/_apiQuery')
def api_query_task():
    url = request.args.get('apiQ0', "", type=str).strip()

    data = getStaffLocation()

    return jsonify(data[0])


@app.route('/')
def hello():
    return redirect("/waiter")


def main():
    app.debug = True
    # app.run(host='0.0.0.0',port=5000)
    app.run(threaded=True)

if __name__ == "__main__":
    main()
