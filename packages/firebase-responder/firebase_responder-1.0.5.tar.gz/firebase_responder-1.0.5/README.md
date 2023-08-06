# Firebase Responder
[![PyPI version](https://badge.fury.io/py/firebase-responder.svg)](https://badge.fury.io/py/firebase-responder) ![Build Test](https://github.com/edward62740/firebase-responder/actions/workflows/python-package.yml/badge.svg)<br>
Used to perform predetermined function calls on IoT devices when a given value in Firebase RTDB is detected. Actions are performed asynchronously and delays/args can be used to customize responses.
### Usage
Initialize group of responses and pass handler() as callback function for Firebase listener.
```
responder = ResponderGroup(1, 3, "ok")
firebase_admin.db.reference('path/to/value').listen(responder.handler)
```

Add device along with sequence of functions to be called, delays, args etc.
```
# led1 init goes here
responder.add(ResponderCustom(3, 2, [led1.turn_on, led1.set_colour, led1.set_colour], [500, 500, 500],
                             [None, [255, 0, 0], [0, 0, 30]]))
responder.add(ResponderStatic("test", led2.turn_on, led2.turn_off, 1500)
```
