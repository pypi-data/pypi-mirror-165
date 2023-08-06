"""custom Phase types"""
import phase.pyphase.types
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "MatrixFloat",
    "MatrixUInt8",
    "StereoImagePair"
]


class MatrixFloat():
    """
    Matrix data (float) storage. Targeted towards storing image data.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
                Matrix empty assignment contructor

                


                Matrix assignment contructor
                Initalise Matrix at provided size

                Parameters
                ----------
                rows : int
                cols : int
                channels : int

                


                Matrix copy contructor

                

        Matrix data assignment contructor
        """
    @typing.overload
    def __init__(self, arg0: MatrixFloat) -> None: ...
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: numpy.ndarray[numpy.float32]) -> None: ...
    def getAt(self, arg0: int, arg1: int, arg2: int) -> float: 
        """
        Get the value of an element in the Matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int

        Returns
        -------
        data : float
            The value of data in float
        """
    def getColumns(self) -> int: 
        """
        Get number of columns in Matrix

        Returns
        -------
        columns : int
            Column of the matrix
        """
    def getLayers(self) -> int: 
        """
        Get number of layers in Matrix

        Returns
        -------
        layers : int
            Layer of the matrix
        """
    def getLength(self) -> int: 
        """
        Get length of Matrix
        (rows * columns * layers)

        Returns
        -------
        value : int
            Length of the matrix
        """
    def getRows(self) -> int: 
        """
        Get number of rows in Matrix

        Returns
        -------
        rows : int
            Row of the matrix
        """
    def getSize(self) -> int: 
        """
        Get size of Matrix in bytes
        (element_byte_size * matrix_length)

        Returns
        -------
        value : int
            Size of the matrix
        """
    def isEmpty(self) -> bool: 
        """
        Check if the matrix is empty

        Returns
        -------
        bool
            True if empty
        """
    def setAt(self, arg0: int, arg1: int, arg2: int, arg3: float) -> None: 
        """
        Set the value of an element in the Matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int
        value : float
        """
    pass
class MatrixUInt8():
    """
    Matrix data (uint8) storage. Targeted towards storing image data.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
                Matrix empty assignment contructor

                


                 Matrix assignment contructor
                Initalise Matrix at provided size

                Parameters
                ----------
                rows : int
                cols : int
                channels : int
                


                Matrix copy contructor

                

        Matrix data assignment contructor
        """
    @typing.overload
    def __init__(self, arg0: MatrixUInt8) -> None: ...
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: numpy.ndarray[numpy.uint8]) -> None: ...
    def getAt(self, arg0: int, arg1: int, arg2: int) -> int: 
        """
        Get the value of an element in the Matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int

        Returns
        -------
        data : int
            The value of data in float
        """
    def getColumns(self) -> int: 
        """
        Get number of columns in Matrix

        Returns
        -------
        columns : int
            Column of the matrix
        """
    def getLayers(self) -> int: 
        """
        Get number of layers in Matrix

        Returns
        -------
        layers : int
            Layer of the matrix
        """
    def getLength(self) -> int: 
        """
        Get length of Matrix
        (rows * columns * layers)

        Returns
        -------
        value : int
            Length of the matrix
        """
    def getRows(self) -> int: 
        """
        Get number of rows in Matrix

        Returns
        -------
        rows : int
            Row of the matrix
        """
    def getSize(self) -> int: 
        """
        Get size of Matrix in bytes
        (element_byte_size * matrix_length)

        Returns
        -------
        value : int
            Size of the matrix
        """
    def isEmpty(self) -> bool: 
        """
        Check if the matrix is empty

        Returns
        -------
        bool
            True if empty
        """
    def setAt(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        Set the value of an element in the Matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int
        value : int
        """
    pass
class StereoImagePair():
    """
    Struture to store stereo image pair (left, right)
    """
    def __init__(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: ...
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
    pass
