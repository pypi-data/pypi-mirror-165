# vectors-draw-lib or pyvdl
## request
matplotlib

numpy

cv2
## Docs
install:
```shell
pip install pyvdl matplotlib opencv-python numpy
```
init:
```python
import pyvdl as vl
print(f'install pyvdl: {vl.__version__}')
```
create_obj:
```python
class example(vl.obj):
    def __init__(self):
        self.color = (255, 255, 255)
    def render(self, x, y):
        return self.abs_(x, y) - 20 < 0
```
create_animation:
```python
class p(vl.animation):
    def __init__(self):
        self.size = (500, 500)
        self.form = lambda x : x
        self.t = 5
        self.obj_ = example()
```
render:
```python
# obj
obj = example()
r = vl.render(obj)
vl.show(r)  # show render-obj: r, only works on pykernel
vl.save("test.png", r)  # save render-obj: r as "test.png"
# animation
animate = p()
animate.render()
animate.video("animation.avi")  # filename.avi
```