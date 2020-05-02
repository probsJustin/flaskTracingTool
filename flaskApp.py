from flask import *
import autodynatrace
import requests
import logging
import oneagent

from datetime import datetime

# Justin Hagerty
# Tracing Application Debug Endpoint For Dynatrace Testing

from oneagent.common import DYNATRACE_HTTP_HEADER_NAME
logging.basicConfig(filename='./flaskData', level=logging.DEBUG)

app = Flask("Tracing Application Debug Endpoint")

init_result = oneagent.initialize()
print('OneAgent SDK initialization result' + repr(init_result))
if init_result:
    print('SDK should work (but agent might be inactive).')
else:
    print('SDK will definitely not work (i.e. functions will be no-ops):', init_result)

sdk = oneagent.get_sdk()

## constants
SLRES = "X-dynaSupLabRes-info"
SLREQ = "X-dynaSupLabReq-info"
SLPATH = "X-dynaSupLabPath-info"
SLPOS = "X-dynaSubLabPosition-info"
SLURL = "url_passthrough"
DYNASL = "Dynatrace Support Lab"
CT = "text"
RESPONSECODE = ""

responseHeaders = dict()
returnBody = dict()

def setResponseCode(funcString):
    global RESPONSECODE
    RESPONSECODE = funcString

def setCT(funcString):
    global CT
    CT = funcString

def line(funcString = ""):
    return funcString + '\n'

def clearReturnBody():
    global returnBody
    returnBody = dict()

def returnReturnBody():
    global returnBody
    return returnBody

def addBody(funcStringVar):
    global returnBody
    try:
        returnBody += funcStringVar
    except:
        returnBody = funcStringVar

def appendToResHeaders(funcStringVar, funcIndexVar):
    global responseHeaders
    try:
        responseHeaders[funcIndexVar] += funcStringVar
    except:
        responseHeaders[funcIndexVar] = funcStringVar

def isDebug(funcRequest):
    if(funcRequest.args.get("debug")):
        if(funcRequest.args.get("debug") in ['true', 'True', '1']):
            return True
        else:
            return False
    else:
            return False

def checkForHeader(funcRequest, funcIndex):
    returnObject = dict()
    if(funcRequest.headers.get(funcIndex)):
        returnObject["test"] = True
        returnObject["unit"] = funcRequest.headers[funcIndex]
        return returnObject
    else:
        returnObject["test"] = False
        return returnObject

def checkForArgs(funcRequest, funcIndex):
    returnObject = dict()
    if(funcRequest.args.get(funcIndex)):
        returnObject["test"] = True
        returnObject["unit"] = funcRequest.args.get(funcIndex)
        return returnObject
    else:
        returnObject["test"] = False
        return returnObject

def requestFactory(funcRequest):
    global returnBody
    clearReturnBody()
    newRequest = funcRequest
    if(isDebug(request)):
        addBody(line(DYNASL + " Debug Output:") + line())
        addBody(line(DYNASL + " Debug Header Output:"))
        for x, y in newRequest.headers:
            addBody(line(x + " : " + y))
        addBody(line() + line(DYNASL + " Debug Header Flags Found:"))
        if(checkForHeader(request, SLPATH)["test"] and checkForHeader(request, SLPOS)["test"]):
            addBody(line(SLPATH + " : " + checkForHeader(request, SLPATH)["unit"]))
            addBody(line(SLPOS + " : " + checkForHeader(request, SLPOS)["unit"]))
        if(checkForHeader(request, SLREQ)["test"]):
            addBody(line(SLREQ + " : " + checkForHeader(request, SLREQ)["unit"]))
        if(checkForHeader(request, SLRES)["test"]):
            addBody(line(SLRES + " : " + checkForHeader(request, SLRES)["unit"]))
        addBody(line() + line(DYNASL + " Query Parameters Found:"))
        if(checkForArgs(request, SLURL)["test"]):
            addBody(line(SLURL + " : " + checkForArgs(request, SLURL)["unit"]))
            try:
                requests.get(checkForArgs(request, SLURL)["TEST"])
            except Exception as error:
                addBody(line("Url_Passthrough Failed With: " + str(error)))
                addBody(line("Likely you put in the url wrong."))
        if(checkForArgs(request, "html")["test"]):
            addBody(line("HTML : " + checkForArgs(request, "html")["unit"]))
            setCT("text/html")
            returnBody = "<!DOCTYPE html>" + returnBody
        if(checkForArgs(request, "statusCode")["test"]):
            addBody(line("statusCode : " + checkForArgs(request, "statusCode")["unit"]))
            setResponseCode(checkForArgs(request, "statusCode")["unit"])

    else:
        addBody("Debug is False")
    return returnReturnBody()

@autodynatrace.trace
@app.route("/apiTest_GET", methods=['GET'])
def apiTest_GET():
    return requestFactory(request)

@app.route("/apiTest_POST", methods=['POST'])
def apiTest_POST():
    return requestFactory(request)

@app.route("/apiTest_PUT", methods=['PUT'])
def apiTest_PUT():
    return requestFactory(request)

@app.route("/apiTest_DELTE", methods=['DELETE'])
def apiTest_DELETE():
    return requestFactory(request)

@app.route("/apiTest_FAILURE", methods=['GET', 'POST', 'PUT', 'DELETE'])
def apiTest_FAILURE():
    return requestFactory(request)

@app.route("/apiTest_SUCCESS", methods=['GET', 'POST', 'PUT', 'DELETE'])
def apiTest_SUCCESS():
    return requestFactory(request)

@app.route("/apiTest_Thread", methods=['GET', 'POST', 'PUT', 'DELETE'])
def apiTest_Thread():
    return requestFactory(request)

@app.route("/apiTest_Fork", methods=['GET', 'POST', 'PUT', 'DELETE'])
def apiTest_Fork():
    return requestFactory(request)

if __name__ == "__main__":
    app.run(debug=True)
