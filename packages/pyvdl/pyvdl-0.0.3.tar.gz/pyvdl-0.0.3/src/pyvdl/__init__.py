from .libs import *
from .other import *
__version__ = "0.0.3"
def show(img):
    plt.imshow(img)
def addrend(r1, r2, width, heigth):
    out = []
    for i in range(width):
        out.append([])
        for j in range(heigth):
            r1_ = r1[i][j]
            r2_ = r2[i][j]
            if r1_ == (0, 0, 0) and not r2_ == (0, 0, 0):
                out[len(out)-1].append(r2_)
            elif not r1_ == (0, 0, 0) and r2_ == (0, 0, 0):
                out[len(out)-1].append(r1_)
            else:
                out[len(out)-1].append(r1_)
    return out
def __getattr__(attr):
    raise pyvdl_error(f'attr: {attr} not found in module: pyvdl({__version__})')