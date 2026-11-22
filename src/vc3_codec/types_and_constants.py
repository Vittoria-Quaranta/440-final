import numpy as np
from numpy.typing import NDArray

Int64Array = NDArray[np.int64]
Int64OrArray = np.int64 | Int64Array
LITTLE_ENDIAN_2_BYTE_INT = "<i2"
LITTLE_ENDIAN_4_BYTE_INT = "<i4"
LITTLE_ENDIAN_8_BYTE_INT = "<i8"
