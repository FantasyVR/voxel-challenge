from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0.0, exposure=2)
scene.set_floor(-0.99, (1.0, 1.0, 1.0))
scene.set_background_color((0.0, 0.0, 0.0))
scene.set_direction_light((1, 1, 1), 0.1, (0.3, 0.6, 0.9))

@ti.func 
def make_cube(pos,w,l,h, mat, color):
    for i, j, k in ti.ndrange(w, h, l):
        scene.set_voxel(vec3(i, j, k) + pos, mat, color)

@ti.func
def umbralla(pos, h, color1, color2):
    len, r, uh = 2.0, 12.0, 10.0
    for i, j, k in ti.ndrange(len, h+1,len):
        scene.set_voxel(vec3(i,j,k) + pos, 1, vec3(1.0, 0.0, 0.0))
    for i, j, k in ti.ndrange((-r,r+1), (h-uh, h), (-r,r+1)):
        if i**2 + k**2  - ((h-j)*1.2/uh) * r **2 < 1.0e-3:
            if j % 2 == 0:
                scene.set_voxel(vec3(i, j, k) + pos, 1, color1)
            else:
                scene.set_voxel(vec3(i, j, k) + pos, 1, color2)
@ti.func
def chair(pos, towel):
    h, w, l ,head= 3, 5, 15, 5
    # chair legs
    make_cube(vec3(0,0,l)+pos, 1, 1,h, 1, vec3(1.0,1.0,1.0) )
    make_cube(vec3(0,0,0)+pos, 1, 1,h, 1, vec3(1.0,1.0,1.0) )
    make_cube(vec3(w,0,l)+pos, 1, 1,h, 1, vec3(1.0,1.0,1.0) )
    make_cube(vec3(w,0,0)+pos, 1, 1,h, 1, vec3(1.0,1.0,1.0) )
    # chair bed
    make_cube(vec3(0,h,head)+pos,w+1,l-head,1, 1, vec3(0.0, 0.0,1.0))
    make_cube(vec3(0,h-1,0)+pos, w+1, l, 1, 1, vec3(1.0,1.0,1.0))
    make_cube(vec3(0,h, l)+pos,w+1, 1, 1, 1, vec3(0.0, 0.0, 1.0))
    #chair head
    for i, k in ti.ndrange(w+1,head): 
        scene.set_voxel(vec3(i,h+head-k, k)+pos, 1, vec3(0.0,0.0,1.0))
        scene.set_voxel(vec3(i,h+head-k-1, k)+pos, 1, vec3(1.0,1.0,1.0))
    if towel:
        for i, j in ti.ndrange(3,3):
            scene.set_voxel(vec3(i, h+1,l/2 + j)+pos, 1, vec3(1.0, 0.0, 0.0))

@ti.func
def wave(pos, nx, x, nz, z):
    for i, j, k, in ti.ndrange((nx,x),(-3,0), (nz,z)):
        if float(k-nz) > 3 * ti.sin(0.4 * float(i)) + ti.sin(1.5 *float(i)):
            scene.set_voxel(vec3(i,j, k-j)+pos,1, vec3(0.3, 0.2, 0.14))
        if float(k-nz) > 3 * ti.sin(0.4 * float(i)) + ti.sin(1.5 *float(i))+3:
            scene.set_voxel(vec3(i,j, k-j)+pos,1, vec3(0.1, 0.5, 1.0))

@ti.func
def human(pos, h, b_color, h_color, l_color):
    make_cube(vec3(2,h+5,0)+ pos,1,1,2,1, b_color) # neck
    make_cube(vec3(1,h+7,0)+ pos,3,2,3,1, h_color) # head
    make_cube(vec3(0,h,0)+ pos,5,2,5,1, b_color) # body
    make_cube(vec3(1,0,0) + pos,1,2,h,1, l_color) # left leg
    make_cube(vec3(3,0,0)+ pos,1,2,h,1, l_color) # right leg
    make_cube(vec3(-3,h+3,0)+ pos,3,2,1,1, h_color) # left arm
    make_cube(vec3(5,h+3,0)+ pos,3, 2,1,1, h_color) # right arm

@ti.func
def table(pos, radius, color):
    make_cube(pos,1,1,5,1,color)
    for i, j in ti.ndrange((-(radius+5),radius+5), (-(radius+5),radius+5)):
        if i**2 + j**2 < radius**2:
            scene.set_voxel(vec3(i,5,j)+pos,1,color) 

@ti.kernel
def initialize_voxels():
    n, N, pi, R, r = 60, 70, 3.1415926, 3, 0.8
    for i, j, k in ti.ndrange((-n, n), (-3, 0),(-n, n)):
        scene.set_voxel(vec3(i, j, k), 1, vec3(0.6, 0.4, 0.08))
    umbralla(vec3(-20,0,-30),30.0, vec3(1.0, 0.0, 0.0),vec3(1.0, 1.0, 1.0))
    umbralla(vec3(20,0,-30), 25.0,vec3(1.0, 1.0, 1.0),vec3(0.0, 0.5, 0.0))
    chair(vec3(23,0,-27), 1)
    chair(vec3(12,0,-32), 0)
    chair(vec3(-17,0,-28), 0)
    chair(vec3(-31,0,-31), 0)
    wave(vec3(0,0,0), -n, n, n-25 ,n)
    human(vec3(-7,0,11), 7,vec3(0.97, 0.6,0.96), vec3(0.91,0.59,0.48),vec3(0.67,0.94,0.95)) # mother
    human(vec3(0,0,19), 5, vec3(0.96,0.42,0.60),vec3(0.91,0.59,0.48),vec3(0.70,0.96,0.58)) # child
    human(vec3(10,0,10), 7, vec3(0.67,0.94, 0.95), vec3(0.91, 0.588, 0.478), vec3(0.91, 0.588, 0.478)) # father
    table(vec3(-36,0,-20), 5, vec3(1.0,1.0,1.0))
    table(vec3(35,0,-20), 5, vec3(1.0,1.0,1.0))
    v_step = 2 * pi / N
    for i, j in ti.ndrange(N, N):
        u, v= i * v_step, j * v_step
        x = (R + r * ti.cos(u)) * ti.cos(v)
        y = (R + r * ti.cos(u)) * ti.sin(v)
        z = r * ti.sin(u)
        scene.set_voxel(vec3(x,z,y) + vec3(-16,0,46), 1, vec3(1.0, 0.0, 1.0))
initialize_voxels()

scene.finish()
