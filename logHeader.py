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

@autodynatrace.trace
@app.route("/logHeader", methods=['GET', 'POST', 'DELETE', 'PUT'])
def logHeader():
    returnObject = "Success : Logging Headers to Console"
    print('\n')
    for x in request.headers:
        print(x)
    return returnObject




if __name__ == "__main__":
    app.run(debug=True)