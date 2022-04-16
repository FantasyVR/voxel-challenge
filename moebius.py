from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.5, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 0, 0))


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    N, pi = 300, 3.1415926
    r_step, t_step = 3.0 / N, 2 * pi / N
    for i, j in ti.ndrange(N, N):
        r, t = -1.5 + i * r_step, j * t_step
        x = ti.cos(t) * (3 + r * ti.cos(t / 2.0))
        y = ti.sin(t) * (3 + r * ti.cos(t / 2.0))
        z = r * ti.sin(t / 2.0)
        if int(r + 1.5) == 0:
            scene.set_voxel(vec3(x, z, y) * 10, 2, vec3(0.9, 0.1, 0.1))
        elif int(r + 1.5) == 1:
            scene.set_voxel(vec3(x, z, y) * 10, 2, vec3(0.0, 0.1, 0.1))
        else:
            scene.set_voxel(vec3(x, z, y) * 10, 2, vec3(0.1, 0.0, 0.1))


initialize_voxels()

scene.finish()
