# from docsApp.database import db

from flask import Flask, Blueprint, render_template, abort, request, redirect, Response
from waitrely import settings
from flask import Flask, jsonify
import json
import requests
import random
import nexmo
import time
from cameraStream import VideoCamera
import cv2


client = nexmo.Client(key="b526e0a6", secret="BK0lyP7Uz4xH2WVe")

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

log = settings.logging

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['TEMPLATES_AUTO_RELOAD'] = settings.TEMPLATES_AUTO_RELOAD

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    # if request.method == 'GET':
    #     return "ECHO: GET\n"

    number = "+4917663177714"
    messageTxt = "Table 17. Empty glass"

    try:
        client.send_message({'from': 'Waiterly','to': number ,'text': messageTxt})

        log.info("Message has been sent. Content: %s" % messageTxt)

    except Exception as error:
        log.error("Error while sending message")

    return jsonify(
        waiterStatus= "Free",
        id=23
    )


@app.route('/location/<int:data>')
def testLocation(data):
    print ('data is %d!' % (data))
    return 'data is %d!' % (data)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        time.sleep(0.00001)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/waiter/')
def apiQuery():
    return render_template('index.html')


def getAPIRepsone(url, apikey, stringPar, pagePar=1):
    url = url + stringPar
    print (url)

    querystring = {"string": stringPar, "page": pagePar}

    headers = {
        'apikey': apikey,
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    log.info("Successfully call API. Info: %s" % response)

    apiHeaders = {
        "limit-month": response.headers.get('X-RateLimit-Limit-month', "Not provided"),
        "remaining-month": response.headers.get('X-RateLimit-Remaining-month', "Not provided"),
        "limit-minute": response.headers.get('X-RateLimit-Limit-minute', "Not provided"),
        "remaining-minute": response.headers.get('X-RateLimit-Remaining-minute', "Not provided"),
    }

    if apiHeaders.get("limit-month") != "Not provided":
        apiInfo = apiHeaders

    else:
        apiInfo = None

    return [response.text, apiInfo]  # Redirect to doorda docs in case is someone will not type the right url

@app.route('/')
def hello():
    return redirect("/echo")


@app.route('/_apiQuery')
def api_query_task():
    url = request.args.get('apiQ0', "", type=str).strip()
    apikey = request.args.get('apiQ1', "", type=str).strip()
    string = request.args.get('apiQ2', "", type=str).strip()
    page = request.args.get('apiQ3', "", type=str).strip()

    resposneAPI = getAPIRepsone(url, apikey, string, page)
    resposneAPIData = resposneAPI[0]
    apiInfo = resposneAPI[1]

    null = None

    jsonResonse = json.loads(resposneAPIData)

    log.info("Returned JSON object to AJAX call")

    return jsonify(jsonResonse, apiInfo)


def main():
    app.debug = True
    # app.run(host='0.0.0.0',port=5000)
    app.run(threaded=True)

if __name__ == "__main__":
    main()
