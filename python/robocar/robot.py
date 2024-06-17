import serial

class Robot():
    def __init__(self, port: str = "/dev/ttyACM0") -> None:
        self._serial = None
        self.__running = False
        self.__port = port

        self.speeds = [0, 0, 0, 0]
        ''' Motor speeds [-1,1] in the order FL FR BL BR '''

    @property
    def port(self):
        return self.__port
    
    @property
    def running(self):
        return self.__running
    
    def __enter__(self):
        self.init()
        return self
    
    def __exit__(self, exceptionType, exceptionValue, exceptionTraceback):
        self.deinit()
    
    def init(self):
        if not self.running:
            try:
                # self._serial = serial.Serial(self.port)
                # self._serial.open()
                self.__running = True
                print("Fake opened! Ya!")
            except:
                print("Could not open serial port")
        else:
            print("Already running")

    def deinit(self):
        if self.running:
            # self._serial.close()
            print("Fake close! Ya!")

    def _serialPrint(self, msg: str):
        print("Serial msg:" + msg)

    def sendDriveCommand(self, fl: float = None, fr: float = None, bl: float = None, br: float = None):
        ''' Sends the set speeds to the motors '''
        if fl is not None and (isinstance(fl, list) or isinstance(fl, tuple)):
            # The user gave a list of values. Use it directly
            self.speeds = list(fl)
        elif fl is not None and fr is not None and bl is not None and br is not None:
            # 4 separate values given. Turn them into the list
            self.speeds = [fl, fr, bl, br]
        # Send the values
        self._serialPrint(' '.join([str(s) for s in self.speeds]))

    def driveForward(self, speed: float = 1):
        ''' Drive the robot forward at the set speed. Defaults to 1 if not specified '''
        self.sendDriveCommand(speed, speed, speed, speed)

    def driveBackward(self, speed: float = 1):
        ''' Drive the robot backward at the set speed. Defaults to 1 if not specified '''
        self.sendDriveCommand(-speed, -speed, -speed, -speed)

    def stop(self):
        ''' Stops the car '''
        self.sendDriveCommand(0, 0, 0, 0)
