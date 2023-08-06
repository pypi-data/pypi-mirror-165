# Responder usage example


from responder import ResponderGroup, ResponderCustom, ResponderStatic, ResponderFlashing
import tinytuya
import firebase_admin
from firebase_admin import credentials, db


sw1 = tinytuya.OutletDevice('', '', '')
led1 = tinytuya.BulbDevice('', '', '')


cred = credentials.Certificate("cert.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})


def main():
    rc = ResponderGroup(0, 1)
    rc.add(ResponderFlashing("1", sw1.turn_on, sw1.turn_off, 2000, 500, 2))
    rc.add(ResponderCustom(3, 2, [led1.turn_on, led1.set_colour, led1.set_colour], [500, 500, 500],
                                 [None, [255, 0, 0], [0, 0, 30]]))

    # Register firebase callback as rc.main
    firebase_admin.db.reference('path/to/device').listen(rc.handler)


if __name__ == "__main__":
    main()
