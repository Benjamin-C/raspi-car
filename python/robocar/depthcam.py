import depthai as dai
import numpy as np

class DepthCamera():
    def __init__(self):

        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define sources and outputs
        self.__monoLeft = self.pipeline.create(dai.node.MonoCamera)
        self.__monoRight = self.pipeline.create(dai.node.MonoCamera)
        self.__color = self.pipeline.create(dai.node.ColorCamera)
        self.__depth = self.pipeline.create(dai.node.StereoDepth)
        self.__xout = self.pipeline.create(dai.node.XLinkOut)
        self.__cout = self.pipeline.create(dai.node.XLinkOut)

        self.__xout.setStreamName("disparity")
        self.__cout.setStreamName("color")

        # Properties
        self.__color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self.__color.setPreviewSize(300, 300)
        self.__color.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        self.__color.setInterleaved(False)
        self.__color.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        self.__monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.__monoLeft.setBoardSocket(dai.CameraBoardSocket.CAM_B)
        self.__monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.__monoRight.setBoardSocket(dai.CameraBoardSocket.CAM_C)

        # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
        self.__depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
        self.__depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
        self.extended_disparity = False
        self.subpixel = False
        self.lr_check = True

        # Linking
        self.__monoLeft.out.link(self.__depth.left)
        self.__monoRight.out.link(self.__depth.right)
        self.__depth.disparity.link(self.__xout.input)
        self.__color.preview.link(self.__cout.input)

        self.__device = None
        self.__dist_q = None
        self.__col_q = None

    @property
    def extended_disparity(self):
        ''' Closer-in minimum depth, disparity range is doubled (from 95 to 190) '''
        return self.__extended_disparity
    
    @extended_disparity.setter
    def extended_disparity(self, extended_disparity):
        self.__extended_disparity = extended_disparity
        self.__depth.setExtendedDisparity(self.__extended_disparity)

    @property
    def subpixel(self):
        ''' Better accuracy for longer distance, fractional disparity 32-levels '''
        return self.__subpixel
    
    @subpixel.setter
    def subpixel(self, subpixel):
        self.__subpixel = subpixel
        self.__depth.setSubpixel(self.__subpixel)

    @property
    def lr_check(self):
        ''' Better handling for occlusions '''
        return self.__lr_check
    
    @lr_check.setter
    def lr_check(self, lr_check):
        self.__lr_check = lr_check
        self.__depth.setLeftRightCheck(self.__lr_check)

    def __enter__(self):
        self.__device = dai.Device(self.pipeline).__enter__()
        # Output queue will be used to get the disparity frames from the outputs defined above
        self.__dist_q = self.__device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
        self.__col_q = self.__device.getOutputQueue(name="color", maxSize=4, blocking=False)
        return self
    
    def __exit__(self, exceptionType, exceptionValue, exceptionTraceback):
        self.__device.__exit__(exceptionType, exceptionValue, exceptionTraceback)

    def getDistFrame(self):
        inDisparity = self.__dist_q.get()  # blocking call, will wait until a new data has arrived
        frame = inDisparity.getFrame()
        # Normalization for better visualization
        frame = (frame * (255 / self.__depth.initialConfig.getMaxDisparity()))
        frame = frame.astype(np.uint8)

        return frame
    
    def getColorFrame(self):
        inFrame = self.__col_q.get()  # blocking call, will wait until a new data has arrived
        frame = inFrame.getCvFrame()
        # frame = frame.getCvFrame()
        # Normalization for better visualization
        # frame = (frame * (255 / self.__depth.initialConfig.getMaxDisparity()))
        # frame[frame < 64] = 0
        # frame /= (256-64)/256
        # frame = frame.astype(np.uint8)

        return frame

