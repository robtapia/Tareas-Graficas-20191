

# Library imports
import glfw
from OpenGL.GL import *
import sys

import transformations2 as tr2
import basic_shapes as bs
import easy_shaders as es
import camera as cam
from mathlib import Point3
import numpy as np
import catrom
# Import extended shapes
import basic_shapes_extended as bs_ext

# Import lights
import lights as light


#Copiado de cilindro.py de la auxiliar 6
def createCilindro():
    h = 1
    r = 0.03
    lat = 20
    lon = 20
    dang = 2 * np.pi / lat
    color = {
        'r': 0.6,  # Red
        'g': 0.6,  # Green
        'b': 0.6,  # Blue
    }
    cylinder_shape = []
    for i in range(lon):  # Vertical component
        for j in range(lat):  # Horizontal component

            # Angle on step j
            ang = dang * j

            # Here we create a quad from 4 vertices
            #
            #    a/---- b/
            #    |      |
            #    d ---- c
            a = [r * np.cos(ang), r * np.sin(ang), h / lon * (i + 1)]
            b = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * (i + 1)]
            c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * i]
            d = [r * np.cos(ang), r * np.sin(ang), h / lon * i]

            # Create quad
            shape = bs_ext.create4VertexColor(a, b, c, d, color['r'], color['g'], color['b'])
            cylinder_shape.append(es.toGPUShape(shape))

    # Add the two covers
    for j in range(lat):
        ang = dang * j

        # Bottom
        a = [0, 0, 0]
        b = [r * np.cos(ang), r * np.sin(ang), 0]
        c = [r * np.cos(ang + dang), r * np.sin(ang + dang), 0]
        shape = bs_ext.createTriangleColor(c, b, a, color['r'], color['g'], color['b'])
        cylinder_shape.append(es.toGPUShape(shape))

        # Top
        a = [0, 0, h]
        b = [r * np.cos(ang), r * np.sin(ang), h]
        c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h]
        shape = bs_ext.createTriangleColor(c, b, a, color['r'], color['g'], color['b'])
        cylinder_shape.append(es.toGPUShape(shape))
    
    return cylinder_shape




    
# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()

# Create camera
camera = cam.CameraR(r=3, center=Point3())
camera.set_r_vel(0.1)
#cameraXYZ=cam.CameraXYZ(Point3(1,1,6.45))


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    global controller
    global obj_light

    if action == glfw.REPEAT or action == glfw.PRESS:
        # Move the camera position
        if key == glfw.KEY_LEFT:
            camera.rotate_phi(-4)
        elif key == glfw.KEY_RIGHT:
            camera.rotate_phi(4)
        elif key == glfw.KEY_UP:
            camera.rotate_theta(-4)
        elif key == glfw.KEY_DOWN:
            camera.rotate_theta(4)
        elif key == glfw.KEY_A:
            camera.close()
        elif key == glfw.KEY_D:
            camera.far()

        # Move the center of the camera
        elif key == glfw.KEY_I:
            camera.move_center_x(-0.05)
        elif key == glfw.KEY_K:
            camera.move_center_x(0.05)
        elif key == glfw.KEY_J:
            camera.move_center_y(-0.05)
        elif key == glfw.KEY_L:
            camera.move_center_y(0.05)
        elif key == glfw.KEY_U:
            camera.move_center_z(-0.05)
        elif key == glfw.KEY_O:
            camera.move_center_z(0.05)

        elif key == glfw.KEY_1:
            camera._center.set_x(0)
            camera._center.set_y(0)
            camera._center.set_z(6.45)
            camera.set_radius(3)
            camera.set_phi(90)
            camera.set_theta(90)
        elif key == glfw.KEY_2:
            camera.set_radius(20)
            camera.set_phi(45)
            camera.set_theta(45)
        elif key == glfw.KEY_3:
            camera.set_radius(20)
            camera.set_phi(225)
            camera.set_theta(45)
        elif key == glfw.KEY_4:
            camera.set_radius(20)
            camera.set_phi(45)
            camera.set_theta(90)

                   

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    elif key == glfw.KEY_Z:
        obj_light.change_color(np.random.random(), np.random.random(), np.random.random())


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Willis Tower', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    
    

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    
    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    gpuAxis = es.toGPUShape(bs.createAxis(1))
    obj_axis = bs_ext.AdvancedGPUShape(gpuAxis, shader=colorShaderProgram)

    #gpuBase=es.toGPUShape(bs.createBase(),GL_REPEAT, GL_NEAREST)
    #obj_Base=bs_ext.AdvancedGPUShape(gpuBase,shader=colorShaderProgram)
    
    #Base
    s1 = (1, -1, 0)
    s2 = (-1, -1, 0)
    s3 = (-1, 1, 0)
    s4 = (1, 1, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('concrete.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeB = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeB.rotationZ(np.pi)

    #1
    p1=(30,-30,-30)
    p2=(30,-30,30)
    p3=(30,30,30)
    p4=(30,30,-30)
    gpu1 = es.toGPUShape(bs_ext.create4VertexTexture('sky1.jpg', p1, p2, p3, p4), GL_REPEAT, GL_LINEAR)
    obj_p = bs_ext.AdvancedGPUShape(gpu1, shader=textureShaderProgram)
    obj_p.rotationZ(np.pi)

    #2
    q1=(-30,-30,-30)
    q2=(-30,-30,30)
    q3=(-30,30,30)
    q4=(-30,30,-30)
    gpu2 = es.toGPUShape(bs_ext.create4VertexTexture('sky1.jpg', q1, q2, q3, q4), GL_REPEAT, GL_LINEAR)
    obj_q = bs_ext.AdvancedGPUShape(gpu2, shader=textureShaderProgram)
    obj_q.rotationZ(np.pi)

    #3
    k1=(-30,30,30)
    k2=(30,30,30)
    k3=(30,30,-30)
    k4=(-30,30,-30)
    gpu3 = es.toGPUShape(bs_ext.create4VertexTexture('sky1.jpg', k1, k2, k3, k4), GL_REPEAT, GL_LINEAR)
    obj_k = bs_ext.AdvancedGPUShape(gpu3, shader=textureShaderProgram)
    obj_k.rotationZ(np.pi)

    #4
    c1=(-30,-30,30)
    c2=(30,-30,30)
    c3=(30,-30,-30)
    c4=(-30,-30,-30)
    gpu4 = es.toGPUShape(bs_ext.create4VertexTexture('sky1.jpg', c1, c2, c3, c4), GL_REPEAT, GL_LINEAR)
    obj_c = bs_ext.AdvancedGPUShape(gpu4, shader=textureShaderProgram)
    obj_c.rotationZ(np.pi)

    #5
    z1=(-30,-30,30)
    z2=(30,-30,30)
    z3=(30,30,30)
    z4=(-30,30,30)
    gpu5 = es.toGPUShape(bs_ext.create4VertexTexture('sky2.jpg', z1, z2, z3, z4), GL_REPEAT, GL_LINEAR)
    obj_z = bs_ext.AdvancedGPUShape(gpu5, shader=textureShaderProgram)
    obj_z.rotationZ(np.pi)

    #alto de un piso
    piso=0.0597
    #Primer Segmento
    primerSegmento=bs.createTextureCubeWithPosition(-0.5,0.5,-0.5,0.5,0,0.0597*25,"glass.jpg")
    gpuPrimerSegmento=es.toGPUShape(primerSegmento, GL_REPEAT, GL_LINEAR)
    obj_primerSegmento=bs_ext.AdvancedGPUShape(gpuPrimerSegmento,shader=textureShaderProgram)
    #Segundo Segmento
    segundoSegmento=bs.createTextureCubeWithPosition(-0.5,0.5,-0.5,0.5,0.0597*25,0.0597*27,"black.jpg")
    gpuSegundoSegmento=es.toGPUShape(segundoSegmento, GL_REPEAT, GL_LINEAR)
    obj_segundoSegmento=bs_ext.AdvancedGPUShape(gpuSegundoSegmento,shader=textureShaderProgram)
    #Tercer Segmento
    tercerSegmento=bs.createTextureCubeWithPosition(-0.5,0.5,-0.5,0.5,0.0597*27,0.0597*50,"glass.jpg")
    gpuTercerSegmento=es.toGPUShape(tercerSegmento, GL_REPEAT, GL_LINEAR)
    obj_tercerSegmento=bs_ext.AdvancedGPUShape(gpuTercerSegmento,shader=textureShaderProgram)
    #Cuarto Segmento
    cuartoSegmentoA=bs.createTextureCubeWithPosition(-0.5,0.167,-0.5,0.167,0.0597*50,0.0597*66,"glass.jpg")
    cuartoSegmentoB=bs.createTextureCubeWithPosition(-0.167,0.5,-0.167,0.5,0.0597*50,0.0597*66,"glass.jpg")
    gpuCuartoSegmentoA=es.toGPUShape(cuartoSegmentoA,GL_REPEAT,GL_LINEAR)
    gpuCuartoSegmentoB=es.toGPUShape(cuartoSegmentoB,GL_REPEAT,GL_LINEAR)
    obj_cuartoSegmentoA=bs_ext.AdvancedGPUShape(gpuCuartoSegmentoA,shader=textureShaderProgram)
    obj_cuartoSegmentoB=bs_ext.AdvancedGPUShape(gpuCuartoSegmentoB,shader=textureShaderProgram)
    #Quinto Segmento
    quintoSegmentoA=bs.createTextureCubeWithPosition(-0.5,0.167,-0.5,0.167,0.0597*66,0.0597*68,"black.jpg")
    quintoSegmentoB=bs.createTextureCubeWithPosition(-0.167,0.5,-0.167,0.5,0.0597*66,0.0597*68,"black.jpg")
    gpuQuintoSegmentoA=es.toGPUShape(quintoSegmentoA,GL_REPEAT,GL_LINEAR)
    gpuQuintoSegmentoB=es.toGPUShape(quintoSegmentoB,GL_REPEAT,GL_LINEAR)
    obj_quintoSegmentoA=bs_ext.AdvancedGPUShape(gpuQuintoSegmentoA,shader=textureShaderProgram)
    obj_quintoSegmentoB=bs_ext.AdvancedGPUShape(gpuQuintoSegmentoB,shader=textureShaderProgram)

    #Sexto Segmento
    sextoSegmentoA=bs.createTextureCubeWithPosition(-0.5,0.5,-0.167,0.167,0.0597*68,0.0597*88,"glass.jpg")
    sextoSegmentoB=bs.createTextureCubeWithPosition(-0.167,0.167,-0.5,0.5,0.0597*68,0.0597*88,"glass.jpg")
    gpuSextoSegmentoA=es.toGPUShape(sextoSegmentoA,GL_REPEAT,GL_LINEAR)
    gpuSextoSegmentoB=es.toGPUShape(sextoSegmentoB,GL_REPEAT,GL_LINEAR)
    obj_sextoSegmentoA=bs_ext.AdvancedGPUShape(gpuSextoSegmentoA,shader=textureShaderProgram)
    obj_sextoSegmentoB=bs_ext.AdvancedGPUShape(gpuSextoSegmentoB,shader=textureShaderProgram)

    #Septimo Segmento
    septimoSegmentoA=bs.createTextureCubeWithPosition(-0.5,0.5,-0.167,0.167,0.0597*88,0.0597*90,"black.jpg")
    septimoSegmentoB=bs.createTextureCubeWithPosition(-0.167,0.167,-0.5,0.5,0.0597*88,0.0597*90,"black.jpg")
    gpuSeptimoSegmentoA=es.toGPUShape(septimoSegmentoA,GL_REPEAT,GL_LINEAR)
    gpuSeptimoSegmentoB=es.toGPUShape(septimoSegmentoB,GL_REPEAT,GL_LINEAR)
    obj_septimoSegmentoA=bs_ext.AdvancedGPUShape(gpuSeptimoSegmentoA,shader=textureShaderProgram)
    obj_septimoSegmentoB=bs_ext.AdvancedGPUShape(gpuSeptimoSegmentoB,shader=textureShaderProgram)
    

    #Octavo Segmento
    octavoSegmento=bs.createTextureCubeWithPosition(-0.5,0.167,-0.167,0.167,0.0597*90,0.0597*108,"glass.jpg")
    gpuOctavoSegmento=es.toGPUShape(octavoSegmento,GL_REPEAT,GL_LINEAR)
    obj_octavoSegmento=bs_ext.AdvancedGPUShape(gpuOctavoSegmento,shader=textureShaderProgram)

    #Techos
    techo3=bs.createTextureCubeWithPosition(-0.5,0.5,-0.5,0.5,0.0597*50,0.0597*50+0.01,"roof.jpg")
    gpuTecho3=es.toGPUShape(techo3,GL_REPEAT,GL_LINEAR)
    obj_techo3=bs_ext.AdvancedGPUShape(gpuTecho3,shader=textureShaderProgram)

    techo5A=bs.createTextureCubeWithPosition(-0.5,0.167,-0.5,0.167,0.0597*68,0.0597*68+0.01,"roof.jpg")
    gpuTecho5A=es.toGPUShape(techo5A,GL_REPEAT,GL_LINEAR)
    obj_techo5A=bs_ext.AdvancedGPUShape(gpuTecho5A,shader=textureShaderProgram)
    techo5B=bs.createTextureCubeWithPosition(-0.167,0.5,-0.167,0.5,0.0597*68,0.0597*68+0.01,"roof.jpg")
    gpuTecho5B=es.toGPUShape(techo5B,GL_REPEAT,GL_LINEAR)
    obj_techo5B=bs_ext.AdvancedGPUShape(gpuTecho5B,shader=textureShaderProgram)

    techo7A=bs.createTextureCubeWithPosition(-0.5,0.5,-0.167,0.167,0.0597*90,0.0597*90+0.01,"roof.jpg")
    gpuTecho7A=es.toGPUShape(techo7A,GL_REPEAT,GL_LINEAR)
    obj_techo7A=bs_ext.AdvancedGPUShape(gpuTecho7A,shader=textureShaderProgram)
    techo7B=bs.createTextureCubeWithPosition(-0.167,0.167,-0.5,0.5,0.0597*90,0.0597*90+0.01,"roof.jpg")
    gpuTecho7B=es.toGPUShape(techo7B,GL_REPEAT,GL_LINEAR)
    obj_techo7B=bs_ext.AdvancedGPUShape(gpuTecho7B,shader=textureShaderProgram)
    
    
    techo8=bs.createTextureCubeWithPosition(-0.5,0.167,-0.167,0.167,0.0597*108,0.0597*108+0.01,"roof.jpg")
    gpuTecho8=es.toGPUShape(techo8,GL_REPEAT,GL_LINEAR)
    obj_techo8=bs_ext.AdvancedGPUShape(gpuTecho8,shader=textureShaderProgram)

    #antenas:
    antena1=createCilindro()
    obj_antena1=bs_ext.AdvancedGPUShape(antena1)
    obj_antena1.translate(0,0,6.45)
    obj_antena1.setShader(colorShaderProgram)

    antena2=createCilindro()
    obj_antena2=bs_ext.AdvancedGPUShape(antena2)
    obj_antena2.translate(-0.333,0,6.45)
    obj_antena2.setShader(colorShaderProgram)

    #tapas antenas:
    vertices=[[1,0],[0,1],[-1,0],[0,-1],[1,0]]
    curve=catrom.getSplineFixed(vertices,10)

    obj_tapa1=bs_ext.createColorPlaneFromCurve(curve,True,1,1,1,center=(0,0))
    obj_tapa1.setShader(colorShaderProgram)
    
    # Create light
    #obj_light = light.Light(shader=phongPipeline, position=[5, 5, 5], color=[1, 1, 1])

    # Main execution loop
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Create projection
        # projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)

        # Get camera view matrix
        view = camera.get_view()

        # Place light
        #obj_light.place()

        # Draw objects
        
        #obj_axis.draw(view, projection, mode=GL_LINES)
        obj_p.draw(view,projection)
        obj_q.draw(view,projection)
        obj_k.draw(view,projection)
        obj_c.draw(view,projection)
        obj_z.draw(view,projection)
        
        obj_planeB.draw(view, projection)
        obj_primerSegmento.draw(view, projection)
        obj_segundoSegmento.draw(view, projection)
        obj_tercerSegmento.draw(view, projection)
        obj_cuartoSegmentoA.draw(view,projection)
        obj_cuartoSegmentoB.draw(view,projection)
        obj_quintoSegmentoA.draw(view,projection)
        obj_quintoSegmentoB.draw(view,projection)
        obj_sextoSegmentoA.draw(view,projection)
        obj_sextoSegmentoB.draw(view,projection)
        obj_septimoSegmentoA.draw(view,projection)
        obj_septimoSegmentoB.draw(view,projection)
        obj_octavoSegmento.draw(view,projection)


        obj_techo3.draw(view,projection)
        obj_techo5A.draw(view,projection)
        obj_techo5B.draw(view,projection)
        obj_techo7A.draw(view,projection)
        obj_techo7B.draw(view,projection)
        obj_techo8.draw(view,projection)

        
        obj_antena1.draw(view,projection)
        obj_antena2.draw(view,projection)
        
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()
