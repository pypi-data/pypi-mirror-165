import asyncio
import time
from typing import Callable
from enum import Enum, auto


class DeviceTypes(Enum):
    DEVICE_STATIC = auto()
    DEVICE_FLASH = auto()
    DEVICE_CUSTOM = auto()


class _ResponderBase(object):
    """ This is the base class for all responder instances. """

    def __init__(self, trig=None, dev_type=None, cb1=None, cb2=None, delay_ms1=None, delay_ms2=None, iterate=None,
                 cblist=None, cbdelays=None, cbargs=None) -> None:
        """
        Initialize a ResponderBase instance. Should be called by inherited classes as checks are done by child classes.
        :param trig value to trigger on
        :param dev_type Enum DeviceTypes
        :param cb1 callback 1 (on) for DEVICE_STATIC, DEVICE_FLASH
        :param cb2 callback 2 (off) ||
        :param delay_ms1 async delay in ms after cb1
        :param delay_ms2 ||                      cb2
        :param iterate number of times to repeat
        :param cblist list of callbacks
        :param cbdelays list of callback delays for cblist
        :param cbargs list of callback arguments for cblist
        """
        self.cb1 = cb1
        self.cb2 = cb2
        self.trig = trig
        self.dev_type = dev_type
        self.delay_ms1 = delay_ms1
        self.delay_ms2 = delay_ms2
        self.iterate = iterate
        if cblist is not None and cbdelays is not None and cbargs is not None:
            self.cblist = [cb for cb in cblist]
            self.cbdelays = [delay for delay in cbdelays]
            self.cbargs = [arg for arg in cbargs]

    async def respond(self, data) -> bool:
        """ Calls callbacks passed during init as configured. Should only be called internally. """
        if data == int(self.trig):
            try:
                if self.dev_type == DeviceTypes.DEVICE_STATIC:
                    print(f"Static device started response at {format(time.time())}")
                    self.cb1()
                    if type(self.cb2) is not None and self.delay_ms1 is not None:
                        await asyncio.sleep(self.delay_ms1 / 1000)
                        print(self.delay_ms1)
                        self.cb2()
                        print(f"Static device finished response at {format(time.time())}")

                elif self.dev_type == DeviceTypes.DEVICE_FLASH:
                    print(f"Flashing device started response at {format(time.time())}")
                    for n in range(self.iterate):
                        self.cb1()
                        await asyncio.sleep(self.delay_ms1 / 1000)
                        self.cb2()
                        await asyncio.sleep(self.delay_ms2 / 1000)
                    print(f"Flashing device finished response at {format(time.time())}")

                elif self.dev_type == DeviceTypes.DEVICE_CUSTOM:
                    print(f"Custom device started response at {format(time.time())}")
                    for cb, delay, args in zip(self.cblist, self.cbdelays, self.cbargs):
                        if args is None:
                            cb()
                        else:
                            cb(*args)
                        await asyncio.sleep(delay / 1000)
                    print(f"Custom device finished response at {format(time.time())}")
            except Exception as e:
                raise ResponderException(e.message)
            return True
        else:
            return False

    @staticmethod
    def is_primitive(val: any) -> bool:
        """ Check if value is a primitive type accepted in FirebaseRTDB. """
        return True if type(val) in [int, float, bool, str] else False


class ResponderGroup(object):
    """ ResponderGroup contains all instances of ResponderBase registered to the same FirebaseRTDB callback. """

    def __init__(self, *defaults) -> None:
        """ Initialize a ResponderGroup instance. Arguments are regarded as don't care values when the handler is
        called. Must be primitive types."""
        self.devices = []
        self._is_running = False
        self.default = [default for default in defaults if _ResponderBase.is_primitive(default)]

    def add(self, device: _ResponderBase) -> bool:
        """ Add a ResponderDevice instance to the list of devices. """
        if not isinstance(device, _ResponderBase):
            return False
        self.devices.append(device)
        return True

    async def _task(self, event) -> None:
        """ Asynchronously run respond() method for each instance of ResponderBase. """
        print("began at {}".format(time.time()))
        await asyncio.wait([
            asyncio.create_task(device.respond(event.data))
            for device in self.devices
        ])
        self._is_running = False

    def handler(self, event) -> None:
        """ Should be registered as callback for FirebaseRTDB listener. """
        if (event.data not in self.default) and (self._is_running == False):
            self._is_running = True
            asyncio.run(self._task(event))


class ResponderStatic(_ResponderBase):
    """ Inherited class to configure a static device. """

    def __init__(self, trig, cb1: Callable, cb2=None, delay_ms=None) -> None:
        """
        Initialize a ResponderBase instance as a static device
        :param trig value to trigger on
        :param cb1 callback 1 (on)
        :param cb2 optional callback 2 (off)
        :param delay_ms if cb2 is passed async delay in ms after cb1
        """

        if not callable(cb1):
            raise ResponderException("callbacks must be callable")
        if not self.is_primitive(trig):
            raise TypeError
        if cb2 is None and delay_ms is None:
            super().__init__(trig, DeviceTypes.DEVICE_STATIC, cb1)
        else:
            if not callable(cb2):
                raise ResponderException("callbacks must be callable")
            super().__init__(trig, DeviceTypes.DEVICE_STATIC, cb1, cb2, delay_ms)


class ResponderFlashing(_ResponderBase):
    """ Inherited class to configure a flashing device. """

    def __init__(self, trig, cb1: Callable, cb2: Callable, delay_ms1=0, delay_ms2=0, iterate=1) -> None:
        """
        Initialize a ResponderBase instance as a flashing device
        :param trig value to trigger on
        :param cb1 callback 1 (on)
        :param cb2 callback 2 (off)
        :param delay_ms1 async delay in ms after cb1
        :param delay_ms2 async delay in ms after cb2
        :param iterate number of times to repeat
        """

        if not callable(cb1) or not callable(cb2):
            raise ResponderException("callbacks must be callable")
        if not self.is_primitive(trig):
            raise TypeError
        if delay_ms1 <= 0 or iterate < 1:
            raise ValueError
        super().__init__(trig, DeviceTypes.DEVICE_FLASH, cb1, cb2, delay_ms1, delay_ms2, iterate)


class ResponderCustom(_ResponderBase):
    """ Inherited class to configure a custom device. """

    def __init__(self, trig, iterate: int, cblist: list, cbdelays: list, cbargs: list) -> None:
        """
        Initialize a ResponderBase instance as a custom device. cblist, cbdelays, and cbargs must be lists of same length.
        :param trig value to trigger on
        :param iterate number of times to repeat
        :param cblist list of callbacks to call
        :param cbdelays list of delays in ms between callbacks, None if no delay
        :param cbargs list of arguments to pass to callbacks, None if no arg
        """

        if not self.is_primitive(trig):
            raise TypeError
        if any(len(lst) != len(cblist) for lst in [cbdelays, cbargs]):
            raise ResponderException("cbdelays and cbargs must be the same length as cblist")
        for cb in cblist:
            if not callable(cb):
                raise ResponderException("cblist must be a list of callables")
        super().__init__(trig, DeviceTypes.DEVICE_CUSTOM, None, None, None, None, iterate, cblist, cbdelays, cbargs)


class ResponderException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)