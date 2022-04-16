from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0.05, exposure=10)
scene.set_floor(-0.99, (1.0, 1.0, 1.0))
scene.set_background_color((0.0, 0.0, 0.0))
scene.set_direction_light((1, 1, 1), 0.1, (0.3, 0.6, 0.9))
@ti.func
def umbralla(pos, h, color1, color2):
    len, r, uh = 2.0, 12.0, 10.0
    for i, j, k in ti.ndrange(len, h+1,len):
        scene.set_voxel(vec3(i,j,k) + pos, 1, vec3(1.0, 0.0, 0.0))
    for i, j, k in ti.ndrange((-r,r+1), (h-uh, h), (-r,r+1)):
        if i**2 + k**2  - ((h-j)/uh) * r **2 < 1.0e-3:
            if j % 2 == 0:
                scene.set_voxel(vec3(i, j, k) + pos, 1, color1)
            else:
                scene.set_voxel(vec3(i, j, k) + pos, 1, color2)
@ti.func
def chair(pos, towel):
    h, w, l ,head= 3, 5, 15, 5
    for j in range(h): #chair leg
        scene.set_voxel(vec3(0,j,l)+pos, 1, vec3(1.0,1.0,1.0))
        scene.set_voxel(vec3(0,j,0)+pos, 1, vec3(1.0,1.0,1.0))
        scene.set_voxel(vec3(w,j,l)+pos, 1, vec3(1.0,1.0,1.0))
        scene.set_voxel(vec3(w,j,0)+pos, 1, vec3(1.0,1.0,1.0))

    for i, j in ti.ndrange(w+1, l-head): #chair bed
        scene.set_voxel(vec3(i,h,head+j)+pos, 1, vec3(0.0, 0.0, 1.0))
    for i, j in ti.ndrange(w+1, l):
        scene.set_voxel(vec3(i,h-1,j)+pos, 1, vec3(1.0, 1.0, 1.0))
    for i in range(w+1):
        scene.set_voxel(vec3(i,h,l)+pos, 1, vec3(0.0, 0.0, 1.0))
    if towel:
        for i, j in ti.ndrange(3,3):
            scene.set_voxel(vec3(i, h+1,l/2 + j)+pos, 1, vec3(1.0, 0.0, 0.0))
    for i, k in ti.ndrange(w+1,head): #chair head
        scene.set_voxel(vec3(i,h+head-k, k)+pos, 1, vec3(0.0,0.0,1.0))
        scene.set_voxel(vec3(i,h+head-k-1, k)+pos, 1, vec3(1.0,1.0,1.0))
@ti.func
def wave(pos, nx, x, nz, z):
    for i, j, k, in ti.ndrange((nx,x),(-3,0), (nz,z)):
        if float(k-nz) > 3 * ti.sin(0.4 * float(i)) + ti.sin(1.5 *float(i)):
            scene.set_voxel(vec3(i,j, k-j)+pos,1, vec3(0.3, 0.2, 0.14))
        if float(k-nz) > 3 * ti.sin(0.4 * float(i)) + ti.sin(1.5 *float(i))+3:
            scene.set_voxel(vec3(i,j, k-j)+pos,1, vec3(0.1, 0.5, 1.0))

@ti.kernel
def initialize_voxels():
    n = 50
    for i, j, k in ti.ndrange((-n, n), (-3, 0),(-n, n)):
        scene.set_voxel(vec3(i, j, k), 1, vec3(0.6, 0.4, 0.08))
    umbralla(vec3(-20,0,-30),30.0, vec3(1.0, 0.0, 0.0),vec3(1.0, 1.0, 1.0))
    umbralla(vec3(20,0,-30), 25.0,vec3(0.0, 1.0, 0.0),vec3(0.1, 0.1, 0.1))
    chair(vec3(23,0,-27), 1)
    chair(vec3(13,0,-32), 0)
    chair(vec3(-18,0,-28), 0)
    chair(vec3(-31,0,-31), 0)
    wave(vec3(0,0,0), -n, n, n-25 ,n)


initialize_voxels()

scene.finish()
