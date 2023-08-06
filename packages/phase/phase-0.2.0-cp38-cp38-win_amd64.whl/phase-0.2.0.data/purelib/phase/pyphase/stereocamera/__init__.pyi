"""stereo camera"""
from __future__ import annotations
import phase.pyphase.stereocamera
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "AbstractStereoCamera",
    "CameraDeviceInfo",
    "CameraDeviceType",
    "CameraInterfaceType",
    "CameraReadResult",
    "DEVICE_TYPE_DEIMOS",
    "DEVICE_TYPE_GENERIC_PYLON",
    "DEVICE_TYPE_GENERIC_UVC",
    "DEVICE_TYPE_INVALID",
    "DEVICE_TYPE_PHOBOS",
    "DEVICE_TYPE_TITANIA",
    "DeimosStereoCamera",
    "INTERFACE_TYPE_GIGE",
    "INTERFACE_TYPE_USB",
    "INTERFACE_TYPE_VIRTUAL",
    "PhobosStereoCamera",
    "PylonStereoCamera",
    "TitaniaStereoCamera",
    "UVCStereoCamera",
    "createStereoCamera"
]


class AbstractStereoCamera():
    """
    Abstract base class for building stereo camera
    classes. Includes functions/structures common across
    all stereo cameras.
    """
    def connect(self) -> bool: 
        """
        Connect to camera
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable/disable saving captured images to file
        Use with setDataCapturePath() to set path to save images

        Parameters
        ----------
        enable : bool
            Enable/disable saving images to file
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        Enable camera hardware trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable hardware trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get number of frames captured since
        initalisation of the camera or last count reset
        Use with resetFrameCount() to reset frame count

        Returns
        -------
        value : int
            Number of frames captured
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor
                    Get current downsample factor
                    
                    Returns
                    -------
                    value : float
                        Downsample factor
                    
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get camera image height

        Returns
        -------
        value : int
            Camera image height
        """
    def getReadThreadResult(self) -> CameraReadResult: 
        """
        Get results from threaded read process
        Should be used with startReadThread()

        Returns
        -------
        CameraReadResult
            Result from read
        """
    def getWidth(self) -> int: 
        """
        Get camera image width

        Returns
        -------
        value : int
            Camera image width
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if continous read thread is running
        Should be used with startContinousReadThread()

        Returns
        -------
        bool
            Continous read thread running status
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera read thread is running

        Returns
        -------
        bool
            True if read thread is running
        """
    def read(self, timeout: int = 1000) -> CameraReadResult: 
        """
        Read image frame from camera

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset captured frame count to zero
        Use with getCaptureCount() to get number of frames captured
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set data capture path to save images
        Use with enableDataCapture() to toggle saving images to file

        path : str
            Directory of desired storage of captured data
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        float : value
            Downsample factor value
        """
    def setExposure(self, arg0: int) -> None: 
        """
        Set exposure value of camera

        Parameters
        ----------

        value : int
            Value of exposure (us)
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        Set frame rate of camera

        Parameters
        ----------
        value : float
            Value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for left camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[CameraReadResult], None]) -> None: 
        """
        Set callback function to run when read thread completes
        Should be used with startReadThread()
        Useful as an external trigger that read is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for right camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        Start stereo camera capture
        Must be started before read() is called
        """
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start threaded process to read stereo images from cameras
        Thread will run continously until stopped
        This is useful for continuous image acquisition

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            Success of starting continous read thread
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread was started successfully
        """
    def stopCapture(self) -> None: 
        """
        Stop stereo camera capture
        Will no longer be able to read() after this is called
        """
    def stopContinousReadThread(self) -> None: 
        """
        Stop continous read thread
        """
    pass
class CameraDeviceInfo():
    """
    Camera info class contains camera serials, camera type and connection type
    """
    def __init__(self, arg0: str, arg1: str, arg2: str, arg3: CameraDeviceType, arg4: CameraInterfaceType) -> None: 
        """
        Variable contains the camera info need to run pyPhase

        Parameters
        ----------
        left_camera_serial : str
        right_camera_serial : str
        unique_serial : str
        device_type : enum
        interface_type : enum
        """
    def getLeftCameraSerial(self) -> str: 
        """
        Get the left camera serial

        Returns
        -------
        left_camera_serial : str
        """
    def getRightCameraSerial(self) -> str: 
        """
        Get the right camera serial

        Returns
        -------
        right_camera_serial : str
        """
    def getUniqueSerial(self) -> str: 
        """
        Get the camera unique serial

        Returns
        -------
        unique_serial : str
        """
    def setLeftCameraSerial(self, arg0: str) -> None: 
        """
        Set the left camera serial

        Parameters
        ----------
        left_camera_serial : str
        """
    def setRightCameraSerial(self, arg0: str) -> None: 
        """
        Set the right camera serial

        Parameters
        ----------
        right_camera_serial : str
        """
    def setUniqueSerial(self, arg0: str) -> None: 
        """
        Set the camera unique serial

        Parameters
        ----------
        unique_serial : str
        """
    @property
    def device_type(self) -> CameraDeviceType:
        """
                    Device type in enum
                    
                    

        :type: CameraDeviceType
        """
    @device_type.setter
    def device_type(self, arg0: CameraDeviceType) -> None:
        """
        Device type in enum
        """
    @property
    def interface_type(self) -> CameraInterfaceType:
        """
                    Interface type in enum

                    

        :type: CameraInterfaceType
        """
    @interface_type.setter
    def interface_type(self, arg0: CameraInterfaceType) -> None:
        """
        Interface type in enum
        """
    pass
class CameraDeviceType():
    """
            Structure of CameraDeviceType

            

    Members:

      DEVICE_TYPE_GENERIC_PYLON

      DEVICE_TYPE_GENERIC_UVC

      DEVICE_TYPE_DEIMOS

      DEVICE_TYPE_PHOBOS

      DEVICE_TYPE_TITANIA

      DEVICE_TYPE_INVALID
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DEVICE_TYPE_DEIMOS: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_DEIMOS: 2>
    DEVICE_TYPE_GENERIC_PYLON: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_PYLON: 0>
    DEVICE_TYPE_GENERIC_UVC: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_UVC: 1>
    DEVICE_TYPE_INVALID: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_INVALID: 5>
    DEVICE_TYPE_PHOBOS: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_PHOBOS: 3>
    DEVICE_TYPE_TITANIA: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_TITANIA: 4>
    __members__: dict # value = {'DEVICE_TYPE_GENERIC_PYLON': <CameraDeviceType.DEVICE_TYPE_GENERIC_PYLON: 0>, 'DEVICE_TYPE_GENERIC_UVC': <CameraDeviceType.DEVICE_TYPE_GENERIC_UVC: 1>, 'DEVICE_TYPE_DEIMOS': <CameraDeviceType.DEVICE_TYPE_DEIMOS: 2>, 'DEVICE_TYPE_PHOBOS': <CameraDeviceType.DEVICE_TYPE_PHOBOS: 3>, 'DEVICE_TYPE_TITANIA': <CameraDeviceType.DEVICE_TYPE_TITANIA: 4>, 'DEVICE_TYPE_INVALID': <CameraDeviceType.DEVICE_TYPE_INVALID: 5>}
    pass
class CameraInterfaceType():
    """
            Structure of CameraInterfaceType

            

    Members:

      INTERFACE_TYPE_USB

      INTERFACE_TYPE_GIGE

      INTERFACE_TYPE_VIRTUAL
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    INTERFACE_TYPE_GIGE: phase.pyphase.stereocamera.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_GIGE: 1>
    INTERFACE_TYPE_USB: phase.pyphase.stereocamera.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_USB: 0>
    INTERFACE_TYPE_VIRTUAL: phase.pyphase.stereocamera.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_VIRTUAL: 2>
    __members__: dict # value = {'INTERFACE_TYPE_USB': <CameraInterfaceType.INTERFACE_TYPE_USB: 0>, 'INTERFACE_TYPE_GIGE': <CameraInterfaceType.INTERFACE_TYPE_GIGE: 1>, 'INTERFACE_TYPE_VIRTUAL': <CameraInterfaceType.INTERFACE_TYPE_VIRTUAL: 2>}
    pass
class CameraReadResult():
    """
    Struture to store the result from reading a camera frame. Used in the stereo camera classes.
    """
    def __init__(self, arg0: bool, arg1: numpy.ndarray, arg2: numpy.ndarray) -> None: ...
    @property
    def left(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @left.setter
    def left(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def right(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @right.setter
    def right(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def valid(self) -> bool:
        """
        :type: bool
        """
    @valid.setter
    def valid(self, arg0: bool) -> None:
        pass
    pass
class DeimosStereoCamera():
    """
    Capture data from I3DR's Deimos stereo camera.
    """
    def __init__(self, arg0: CameraDeviceInfo) -> None: 
        """
        Initalise Stereo Camera with the given device_info.

        Parameters
        ----------

        device_info     : CameraDeviceInfo
            Camera device information to use when initalising camera
        """
    def connect(self) -> bool: 
        """
        Connect to camera
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable/disable saving captured images to file
        Use with setDataCapturePath() to set path to save images

        Parameters
        ----------
        enable : bool
            Enable/disable saving images to file
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        Enable camera hardware trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable hardware trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get number of frames captured since
        initalisation of the camera or last count reset
        Use with resetFrameCount() to reset frame count

        Returns
        -------
        value : int
            Number of frames captured
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get current downsample factor

        Returns
        -------
        value : float
            Downsample factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get camera image height

        Returns
        -------
        value : int
            Camera image height
        """
    def getReadThreadResult(self) -> CameraReadResult: 
        """
        Get results from threaded read process
        Should be used with startReadThread()

        Returns
        -------
        CameraReadResult
            Result from read
        """
    def getWidth(self) -> int: 
        """
        Get camera image width

        Returns
        -------
        value : int
            Camera image width
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if continous read thread is running
        Should be used with startContinousReadThread()

        Returns
        -------
        bool
            Continous read thread running status
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera read thread is running

        Returns
        -------
        bool
            True if read thread is running
        """
    def read(self, timeout: int = 1000) -> CameraReadResult: 
        """
        Read image frame from camera

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        CameraReadResult
            result from camera read
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset captured frame count to zero
        Use with getCaptureCount() to get number of frames captured
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            Directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        float : value
            Downsample factor value
        """
    def setExposure(self, arg0: int) -> None: 
        """
        Set exposure value of camera

        Parameters
        ----------

        value : int
            Value of exposure (us)
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        Set frame rate of camera

        Parameters
        ----------
        value : float
            Value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for left camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[CameraReadResult], None]) -> None: 
        """
        Set callback function to run when read thread completes
        Should be used with startReadThread()
        Useful as an external trigger that read is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for right camera
         
         Parameters
         ----------
         x_min : int
             x value of top left corner of targeted AOI
         y_min : int
             y value of top left corner of targeted AOI
         x_max : int
             x value of bottom right corner of targeted AOI
         y_max : int
             y value of bottom right corner of targeted AOI
         
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        Start stereo camera capture
        Must be started before read() is called
        """
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start threaded process to read stereo images from cameras
        Thread will run continously until stopped
        This is useful for continuous image acquisition

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            Success of starting continous read thread
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread was started successfully
        """
    def stopCapture(self) -> None: 
        """
        Stop stereo camera capture
        Will no longer be able to read() after this is called
        """
    def stopContinousReadThread(self) -> None: 
        """
        Stop continous read thread
        """
    pass
class PhobosStereoCamera():
    """
    Capture data from I3DR's Phobos stereo camera.
    """
    def __init__(self, arg0: CameraDeviceInfo) -> None: 
        """
        Initalise Stereo Camera with the given device_info.

        Parameters
        ----------

        device_info     : CameraDeviceInfo
            Camera device information to use when initalising camera
        """
    def connect(self) -> bool: 
        """
        Connect to camera
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable/disable saving captured images to file
        Use with setDataCapturePath() to set path to save images

        Parameters
        ----------
        enable : bool
            Enable/disable saving images to file
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        Enable camera hardware trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable hardware trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get number of frames captured since
        initalisation of the camera or last count reset
        Use with resetFrameCount() to reset frame count

        Returns
        -------
        value : int
            Number of frames captured
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get current downsample factor

        Returns
        -------
        value : float
            Downsample factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get camera image height

        Returns
        -------
        value : int
            Camera image height
        """
    def getReadThreadResult(self) -> CameraReadResult: 
        """
        Get results from threaded read process
        Should be used with startReadThread()

        Returns
        -------
        CameraReadResult
            Result from read
        """
    def getWidth(self) -> int: 
        """
        Get camera image width

        Returns
        -------
        value : int
            Camera image width
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if continous read thread is running
        Should be used with startContinousReadThread()

        Returns
        -------
        bool
            Continous read thread running status
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera read thread is running

        Returns
        -------
        bool
            True if read thread is running
        """
    def read(self, timeout: int = 1000) -> CameraReadResult: 
        """
        Read image frame from camera

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        CameraReadResult
            result from camera read
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset captured frame count to zero
        Use with getCaptureCount() to get number of frames captured
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            Directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        float : value
            Downsample factor value
        """
    def setExposure(self, arg0: int) -> None: 
        """
        Set exposure value of camera

        Parameters
        ----------

        value : int
            Value of exposure (us)
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        Set frame rate of camera

        Parameters
        ----------
        value : float
            Value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for left camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[CameraReadResult], None]) -> None: 
        """
        Set callback function to run when read thread completes
        Should be used with startReadThread()
        Useful as an external trigger that read is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for right camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        Start stereo camera capture
        Must be started before read() is called
        """
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start threaded process to read stereo images from cameras
        Thread will run continously until stopped
        This is useful for continuous image acquisition

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            Success of starting continous read thread
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread was started successfully
        """
    def stopCapture(self) -> None: 
        """
        Stop stereo camera capture
        Will no longer be able to read() after this is called
        """
    def stopContinousReadThread(self) -> None: 
        """
        Stop continous read thread
        """
    pass
class PylonStereoCamera():
    """
    Capture data from a stereo camera using Basler cameras via the Pylon API
    """
    def __init__(self, arg0: CameraDeviceInfo) -> None: 
        """
        Initalise Stereo Camera with the given device_info.

        Parameters
        ----------

        device_info     : CameraDeviceInfo
            Camera device information to use when initalising camera
        """
    def connect(self) -> bool: 
        """
        Connect to camera
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable/disable saving captured images to file
        Use with setDataCapturePath() to set path to save images

        Parameters
        ----------
        enable : bool
            Enable/disable saving images to file
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        Enable camera hardware trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable hardware trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get number of frames captured since
        initalisation of the camera or last count reset
        Use with resetFrameCount() to reset frame count

        Returns
        -------
        value : int
            Number of frames captured
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get current downsample factor

        Returns
        -------
        value : float
            Downsample factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get camera image height

        Returns
        -------
        value : int
            Camera image height
        """
    def getReadThreadResult(self) -> CameraReadResult: 
        """
        Get results from threaded read process
        Should be used with startReadThread()

        Returns
        -------
        CameraReadResult
            Result from read
        """
    def getWidth(self) -> int: 
        """
        Get camera image width

        Returns
        -------
        value : int
            Camera image width
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if continous read thread is running
        Should be used with startContinousReadThread()

        Returns
        -------
        bool
            Continous read thread running status
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera read thread is running

        Returns
        -------
        bool
            True if read thread is running
        """
    def read(self, timeout: int = 1000) -> CameraReadResult: 
        """
        Read image frame from camera

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        CameraReadResult
            Result from camera read
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset captured frame count to zero
        Use with getCaptureCount() to get number of frames captured
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            Directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        float : value
            Downsample factor value
        """
    def setExposure(self, arg0: int) -> None: 
        """
        Set exposure value of camera

        Parameters
        ----------

        value : int
            Value of exposure (us)
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        Set frame rate of camera

        Parameters
        ----------
        value : float
            Value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for left camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[CameraReadResult], None]) -> None: 
        """
        Set callback function to run when read thread completes
        Should be used with startReadThread()
        Useful as an external trigger that read is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for right camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        Start stereo camera capture
        Must be started before read() is called
        """
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start threaded process to read stereo images from cameras
        Thread will run continously until stopped
        This is useful for continuous image acquisition

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            Success of starting continous read thread
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread was started successfully
        """
    def stopCapture(self) -> None: 
        """
        Stop stereo camera capture
        Will no longer be able to read() after this is called
        """
    def stopContinousReadThread(self) -> None: 
        """
        Stop continous read thread
        """
    pass
class TitaniaStereoCamera():
    """
    Capture data from I3DR's Titania stereo camera.
    """
    def __init__(self, arg0: CameraDeviceInfo) -> None: 
        """
        Initalise Stereo Camera with the given device_info.

        Parameters
        ----------

        device_info     : CameraDeviceInfo
            Camera device information to use when initalising camera
        """
    def connect(self) -> bool: 
        """
        Connect to camera
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable/disable saving captured images to file
        Use with setDataCapturePath() to set path to save images

        Parameters
        ----------
        enable : bool
            Enable/disable saving images to file
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        Enable camera hardware trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable hardware trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get number of frames captured since
        initalisation of the camera or last count reset
        Use with resetFrameCount() to reset frame count

        Returns
        -------
        value : int
            Number of frames captured
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get current downsample factor

        Returns
        -------
        value : float
            Downsample factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get camera image height

        Returns
        -------
        value : int
            Camera image height
        """
    def getReadThreadResult(self) -> CameraReadResult: 
        """
        Get results from threaded read process
        Should be used with startReadThread()

        Returns
        -------
        CameraReadResult
            Result from read
        """
    def getWidth(self) -> int: 
        """
        Get camera image width

        Returns
        -------
        value : int
            Camera image width
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if continous read thread is running
        Should be used with startContinousReadThread()

        Returns
        -------
        bool
            Continous read thread running status
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera read thread is running

        Returns
        -------
        bool
            True if read thread is running
        """
    def read(self, timeout: int = 1000) -> CameraReadResult: 
        """
        Read image frame from camera

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        CameraReadResult
            Result from camera read
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset captured frame count to zero
        Use with getCaptureCount() to get number of frames captured
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set data capture path to save images
        Use with enableDataCapture() to toggle saving images to file

        path : str
            Directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        float : value
            Downsample factor value
        """
    def setExposure(self, arg0: int) -> None: 
        """
        Set exposure value of camera

        Parameters
        ----------

        value : int
            Value of exposure (us)
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        Set frame rate of camera

        Parameters
        ----------
        value : float
            Value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for left camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[CameraReadResult], None]) -> None: 
        """
        Set callback function to run when read thread completes
        Should be used with startReadThread()
        Useful as an external trigger that read is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for right camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        Start stereo camera capture
        Must be started before read() is called
        """
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start threaded process to read stereo images from cameras
        Thread will run continously until stopped
        This is useful for continuous image acquisition

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            success of starting continous read thread
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread was started successfully
        """
    def stopCapture(self) -> None: 
        """
        Stop stereo camera capture
        Will no longer be able to read() after this is called
        """
    def stopContinousReadThread(self) -> None: 
        """
        Stop continous read thread
        """
    pass
class UVCStereoCamera():
    """
    UVC Stereo Camera class
    Capture data from a stereo camera using UVC cameras
    where left and right is transported via green and red channels.
    """
    def __init__(self, arg0: CameraDeviceInfo) -> None: 
        """
        Initalise Stereo Camera with the given device_info.

        Parameters
        ----------

        device_info     : CameraDeviceInfo
            Camera device information to use when initalising camera
        """
    def connect(self) -> bool: 
        """
        Connect to camera
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable/disable saving captured images to file
        Use with setDataCapturePath() to set path to save images

        Parameters
        ----------
        enable : bool
            Enable/disable saving images to file
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        Enable camera hardware trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable hardware trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get number of frames captured since
        initalisation of the camera or last count reset
        Use with resetFrameCount() to reset frame count

        Returns
        -------
        value : int
            Number of frames captured
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get current downsample factor

        Returns
        -------
        value : float
            Downsample factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get camera image height

        Returns
        -------
        value : int
            Camera image height
        """
    def getReadThreadResult(self) -> CameraReadResult: 
        """
        Get results from threaded read process
        Should be used with startReadThread()

        Returns
        -------
        CameraReadResult
            Result from read
        """
    def getWidth(self) -> int: 
        """
        Get camera image width

        Returns
        -------
        value : int
            Camera image width
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if continous read thread is running
        Should be used with startContinousReadThread()

        Returns
        -------
        bool
            Continous read thread running status
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera read thread is running

        Returns
        -------
        bool
            True if read thread is running
        """
    def read(self, timeout: int = 1000) -> CameraReadResult: 
        """
        Read image frame from camera

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        CameraReadResult
            Result from camera read
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset captured frame count to zero
        Use with getCaptureCount() to get number of frames captured
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set data capture path to save images
        Use with enableDataCapture() to toggle saving images to file

        path : str
            Directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        float : value
            Downsample factor value
        """
    def setExposure(self, arg0: int) -> None: 
        """
        Set exposure value of camera

        Parameters
        ----------

        value : int
            Value of exposure (us)
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        Set frame rate of camera

        Parameters
        ----------
        value : float
            Value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for left camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[CameraReadResult], None]) -> None: 
        """
        Set callback function to run when read thread completes
        Should be used with startReadThread()
        Useful as an external trigger that read is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set area of interest for right camera

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        Start stereo camera capture
        Must be started before read() is called
        """
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start threaded process to read stereo images from cameras
        Thread will run continously until stopped
        This is useful for continuous image acquisition

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            Success of starting continous read thread
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            Timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread was started successfully
        """
    def stopCapture(self) -> None: 
        """
        Stop stereo camera capture
        Will no longer be able to read() after this is called
        """
    def stopContinousReadThread(self) -> None: 
        """
        Stop continous read thread
        """
    pass
def createStereoCamera(arg0: CameraDeviceInfo) -> AbstractStereoCamera:
    """
    Read device type and return in related camera variable
    """
DEVICE_TYPE_DEIMOS: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_DEIMOS: 2>
DEVICE_TYPE_GENERIC_PYLON: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_PYLON: 0>
DEVICE_TYPE_GENERIC_UVC: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_UVC: 1>
DEVICE_TYPE_INVALID: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_INVALID: 5>
DEVICE_TYPE_PHOBOS: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_PHOBOS: 3>
DEVICE_TYPE_TITANIA: phase.pyphase.stereocamera.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_TITANIA: 4>
INTERFACE_TYPE_GIGE: phase.pyphase.stereocamera.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_GIGE: 1>
INTERFACE_TYPE_USB: phase.pyphase.stereocamera.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_USB: 0>
INTERFACE_TYPE_VIRTUAL: phase.pyphase.stereocamera.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_VIRTUAL: 2>
