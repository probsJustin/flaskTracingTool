from flask import *
import autodynatrace
import requests
import logging
import oneagent

from datetime import datetime

# Justin Hagerty
# Tracing Application Debug Endpoint For Dynatrace Testing

from oneagent.common import DYNATRACE_HTTP_HEADER_NAME
logging.basicConfig(filename='./flaskData',level=logging.DEBUG)

app = Flask("Tracing Application Debug Endpoint")

init_result = oneagent.initialize()
print('OneAgent SDK initialization result' + repr(init_result))
if init_result:
    print('SDK should work (but agent might be inactive).')
else:
    print('SDK will definitely not work (i.e. functions will be no-ops):', init_result)

sdk = oneagent.get_sdk()

def logRequest(requestFuncVar):
    print(requestFuncVar.args)
    logging.info(request.args)

def isDebug(requestFuncVar):
    if(requestFuncVar.args.get("debug")):
        print("Dynatrace SUPLAB Debug Variable is set to True")
        if(requestFuncVar.args.get("debug") == "True" or requestFuncVar.args.get("debug") == "1"):
            return True
        else:
            return False
    else:
        return False

def isPassThrough(requestFuncVar):
    if(requestFuncVar.args.get("url_passthrough")):
        print("Dynatrace SUPLAB Url Passthrough Variable is set.")
        return True
    else:
        return False


def processRequest(requestFuncVar):
    newResponse = dict()
    newResponse['data'] = ""
    newResponse['unit'] = False
    if(isPassThrough(requestFuncVar)):
        try:
            newResponse['url_passthrough'] = requestFuncVar.args.get('url_passthrough')
        except Exception as error:
            newResponse['url_passthrough'] = False
            print(error)
    else:
        newResponse['url_passthrough'] = False
    if(isDebug(requestFuncVar)):
        newResponse['unit'] = True

        newResponse['data'] = newResponse['data'] + "\n Dynatrace SUPLAB Debug Request URL \n"
        newResponse['data'] = newResponse['data'] + "PATH : " + requestFuncVar.path + "\n"
        newResponse['data'] = newResponse['data'] + "URL : " + requestFuncVar.url + "\n"

        newResponse['data'] = newResponse['data'] + "Method : " + requestFuncVar.method + '\n'
        newResponse['data'] = newResponse['data'] + "Remote Address : " + requestFuncVar.remote_addr + '\n'

        newResponse['data'] = newResponse['data'] + "\n Dynatrace SUPLAB Debug Request Arguments: \n"
        for x in requestFuncVar.args:
            newResponse['data'] = newResponse['data'] + str(x) + " : " + requestFuncVar.args.get(x) + '\n'
        newResponse['data'] = newResponse['data'] + "\n Dynatrace SUPLAB Debug Request Headers: \n"
        for x in requestFuncVar.headers:
            newResponse['data'] = newResponse['data'] + str(x) + '\n'
        newResponse['data'] = newResponse['data'] + "\n Dynatrace SUPLAB Debug Cookies: \n"
        for x in requestFuncVar.cookies:
            newResponse['data'] = newResponse['data'] + str(x) + " : " + requestFuncVar.cookies.get(x) + '\n'
    logRequest(requestFuncVar)
    return newResponse

def getCurrentAddress(headers):
    return headers.args.get('X-dynaSupLabPath-info')


def addRequestHeaderInfo(headers, requestIp, messageHeader, contentLength, requestURI):
    newHeader = dict()
    newHeader = headers
    newHeader['X-dynaSupLabReq-info'] = newHeader['X-dynaSupLabReq-info'] + "ts=" + datetime.now() + ",client-ip=" + requestIp + ",message=" + messageHeader + ",content-length=" + contentLength + ",requestURI=" + requestURI + "$"
    return newHeader

def addRequestHeaderInfo(headers, requestIp, messageHeader, contentLength, requestURI):
    newHeader = dict()
    newHeader = headers
    newHeader['X-dynaSupLabRes-info'] = newHeader['X-dynaSupLabRes-info'] + "ts=" + datetime.now() + ",client-ip=" + requestIp + ",message=" + messageHeader + ",content-length=" + contentLength + ",requestURI=" + requestURI + "$"
    return newHeader

def getNewHeaders(headers):
    newHeader = dict()
    newHeader['X-dynaSupLabPosition-info'] = str(headers['X-dynaSupLabPosition-info'])
    newHeader['X-dynaSupLabPath-info'] = str(headers['X-dynaSupLabPath-info'])
    if(newHeader['X-dynaSupLabPath-info'] == 'False'):
        newHeader['X-dynaSupLabPosition-info'] = str(int(newHeader['X-dynaSupLabPosition-info']) + 1)
    else:
        newHeader['X-dynaSupLabPosition-info']
    return newHeader


def getNewPath(headers):
    newHeader = dict()
    newHeader['X-dynaSupLabPosition-info'] = str(headers['X-dynaSupLabPosition-info'])
    newHeader['X-dynaSupLabPath-info'] = str(headers['X-dynaSupLabPath-info'])
    splitNewHeader = str(newHeader['X-dynaSupLabPath-info']).split(',')
    if(newHeader['X-dynaSupLabPosition-info'] == 'False'):
        return splitNewHeader
    else:
        return splitNewHeader[int(newHeader['X-dynaSupLabPosition-info'])]

@autodynatrace.trace
@app.route("/apiTest_GET", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_GET():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    return responseObject

@app.route("/apiTest_POST", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_POST():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    return responseObject

@app.route("/apiTest_DELETE", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_DELETE():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    return responseObject

@app.route("/apiTest_PUT", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_PUT():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    return responseObject





@app.route("/apiTest_CUSTOM", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_CUSTOM():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    return responseObject





@app.route("/apiTest_FAILURE", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_FAILURE():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    abort(500)
    return responseObject

@app.route("/apiTest_SUCCESS", methods=['GET', 'POST'])
def apiTest_SUCCESS():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)
    return responseObject


@app.route("/apiTest_PATH", methods=['GET', 'POST'])
def apiTest_PATH():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        print(getCurrentAddress(request))
        if(str(request.headers['X-dynaSupLabPosition-info']) == 'False'):
            for x in getNewPath(request.headers):
                response = requests.get(str(x))
        else:
            response = requests.get(getNewPath(request.headers), headers=getNewHeaders(request.headers))
    return responseObject



@app.route("/apiTest_responseCodeCheck", methods=['GET', 'POST', 'DELETE', 'PUT'])
def apiTest_responseCodeCheck():
    responseObject = Response("Hello World!")
    processObject = processRequest(request)
    if(processObject['unit']):
        responseObject = Response(processObject['data'])
        if(processObject['url_passthrough'] != False):
            url = processObject['url_passthrough']
            response = requests.get(url)

    if(request.args.get('responseCode') and request.args.get('responseCode') != "200"):
        print(str("Response: " + request.args.get('responseCode')))
        abort(int(request.args.get('responseCode')))
    else:
        if(request.args.get('responseCode') == "200"):
            print(str("Response: " + request.args.get('responseCode')))
            print("Success - 200 received for response code checker")
        else:
            abort(500)
            print("No Response Specified")
    return responseObject


if __name__ == "__main__":
    app.run(debug=True)