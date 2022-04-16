from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.9, (1.0, 1.0, 1.0))
# scene.set_direction_light((1, 1, 1), 0.1, (1, 1, 1))
scene.set_background_color((0.05, 0.05, 0))

pi = 3.1415926


@ti.func
def is_in_tri(p0, p1, p2, p):
    p01, p02, p0p = p1 - p0, p2 - p0, p - p0
    denomiter = p01[0] * p02[1] - p01[1] * p02[0]
    s = (p0p[0] * p02[1] - p0p[1] * p02[0]) / denomiter
    t = (p01[0] * p0p[1] - p01[1] * p0p[0]) / denomiter
    return (s >= 0) and (t >= 0) and (1 - s - t >= 0)


@ti.kernel
def initialize_voxels():
    for i, j, k in ti.ndrange((10, 50), (20, 60), (20, 60)):
        x, y, z = float(i), float(j), float(k)
        if ti.sqrt((x - 30)**2 + (y - 40)**2 + (z - 40)**2) < 20:
            scene.set_voxel(vec3(x, y, z), 2, vec3(1.0, 0.9, 0.1))

    for i, j, k in ti.ndrange((50, 60), (-45, -35), (10, 20)):
        x, y, z = float(i), float(j), float(k)
        if ti.sqrt((x - 55)**2 + (y + 40)**2 + (z - 15)**2) < 5:
            scene.set_voxel(vec3(x, y, z), 1, vec3(0.9, 0.05, 0.05))

    yaw, pitch = ti.cos(pi / 4), ti.sin(pi / 4)
    rotation_y = mat3([[yaw, 0.0, -pitch], [0.0, 1.0, 0.0], [pitch, 0.0, yaw]])
    rotation_x = mat3([[1.0, 0.0, 0.0], [0, yaw, pitch], [0, -pitch, yaw]])
    for i, j, k in ti.ndrange((-15, 15), (-15, 15), (-15, 15)):
        pos = rotation_x @ (rotation_y @ vec3(i, j, k))
        scene.set_voxel(pos, 1, vec3(0.4, 0.0, 1.0))

    p0, p1, p2 = ti.Vector([-20.0, -50.0,
                            0]), ti.Vector([20.0, -50.0,
                                            0]), ti.Vector([0.0, -30, 0])
    for i, j, k in ti.ndrange((-20, 20), (-50, -20), (0, 5)):
        p = ti.Vector([float(i), j, k], ti.f32)
        if is_in_tri(p0, p1, p2, p):
            scene.set_voxel(vec3(i, j, k), 1, vec3(0.2, 0.8, 0.2))


initialize_voxels()

scene.finish()
