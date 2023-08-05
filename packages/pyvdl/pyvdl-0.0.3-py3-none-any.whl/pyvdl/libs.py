try:
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from numba import jit
    import numpy as np
    import cv2
except ImportError as e:
    import os
    os.system("python3 -m pip install matplotlib numpy opencv-python numba")
    raise e