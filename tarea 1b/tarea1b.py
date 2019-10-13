import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import sys
import random
from math import *

INT_BYTES = 4

class Controller:
    x=0.0
    y=0.0
    zoom=1
    fillPolygon=True
    useNight=False

controller=Controller()

def on_key(window, key, scancode, action, mods):

    global controller

    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_LEFT:
            controller.x -= 0.1
        elif key == glfw.KEY_RIGHT:
            controller.x += 0.1
        elif key == glfw.KEY_UP:
            controller.y += 0.1
        elif key == glfw.KEY_DOWN:
            controller.y -= 0.1
        elif key==glfw.KEY_Q:
            controller.zoom+=0.1
        elif key==glfw.KEY_W:
            controller.zoom-=0.1

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.useNight = not controller.useNight
    elif key == glfw.KEY_ESCAPE:
        sys.exit()


class GPUShape:
    vao = 0
    vbo = 0
    ebo = 0
    size = 0

def drawShape(shaderProgram, shape, transform):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)
def createCielo():
    gpuShape=GPUShape()
    vertexData=np.array([
        -1, -1, 0, 1,1,1,
         1, -1, 0, 1,1,1,
         1,  1, 0, 0, 191/255.0, 1,
        -1,  1, 0, 0, 191/255.0, 1,

    ],dtype=np.float32)
    indices=np.array(
        [0,1,2,
         2,3,0],dtype=np.uint32)

    gpuShape.size=len(indices)
    
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)
    

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape



def createSuelo():
   # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions  colors
        
        -1,-0.5, 0, 119/255.0, 136/255.0, 153/255.0,
        1, -0.5, 0, 119/255.0, 136/255.0, 153/255.0,
        -1, -1, 0, 119/255.0, 136/255.0, 153/255.0,
        1, -1, 0, 119/255.0, 136/255.0, 153/255.0,
        
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         1, 2, 3], dtype=np.uint32)
    #print(vertexData)
    #print(indices)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape



def createNube():
    gpuShape=GPUShape()
    particiones=100
    angulo=2*pi/particiones
    radio=0.1
    CX1=0.75
    CY1=0.5
    CX2=CX1+radio
    CY2=CY1+radio
    CX3=CX1+2*radio
    CY3=CY1
    
    vertexData=[]
    VD=[CX1,CY1,0,1,1,1]
    VD2=[CX2,CY2,0,1,1,1]
    VD3=[CX3,CY3,0,1,1,1]
    vertexData.extend(VD)
    for i in range(1,particiones+1):
        A=CX1+radio*cos((i)*angulo)
        B=CY1+radio*sin((i)*angulo)
        VD=[A,B,0,1,1,1]
        vertexData.extend(VD)
    vertexData.extend(VD2)
    for i in range(1,particiones+1):
        A=CX2+radio*cos((i)*angulo)
        B=CY2+radio*sin((i)*angulo)
        VD=[A,B,0,1,1,1]
        vertexData.extend(VD)
    vertexData.extend(VD3)
    for i in range(1,particiones+1):
        A=CX3+radio*cos((i)*angulo)
        B=CY3+radio*sin((i)*angulo)
        VD=[A,B,0,1,1,1]
        vertexData.extend(VD)
    triangulos=[]
    triangulos.append(0)
    triangulos.append(1)
    triangulos.append(2)
    for j in range(particiones-1):
        triangulos.append(0)
        triangulos.append(j+1)
        triangulos.append(j+2)
    triangulos.append(0)
    triangulos.append(1)
    triangulos.append(particiones)

    triangulos.append(particiones)
    triangulos.append(1+particiones)
    triangulos.append(2+particiones)
    for j in range(particiones-1):
        triangulos.append(particiones)
        triangulos.append(j+1+particiones)
        triangulos.append(j+2+particiones)
    triangulos.append(particiones)
    triangulos.append(1+particiones)
    triangulos.append(2*particiones)

    triangulos.append(2*particiones)
    triangulos.append(1+2*particiones)
    triangulos.append(2+2*particiones)
    for j in range(particiones-1):
        triangulos.append(2*particiones)
        triangulos.append(j+1+2*particiones)
        triangulos.append(j+2+2*particiones)
    triangulos.append(2*particiones)
    triangulos.append(1+2*particiones)
    triangulos.append(3*particiones)

    vertexData=np.array(vertexData, dtype=np.float32)
    triangulos=np.array(triangulos,dtype=np.uint32)
    indices=triangulos
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


def createSol():
    gpuShape=GPUShape()    
    particiones=100
    angulo=2*pi/particiones
    CX=-0.5
    CY=0.7
    radio=0.1
    vertexData=[]
    VD=[]
    VD=[CX,CY,0,1,200/255.0,1/255.0]
    vertexData.extend(VD)
    for i in range(1,particiones+1):
        A=CX+radio*cos((i)*angulo)
        B=CY+radio*sin((i)*angulo)
        VD=[A,B,0,1,200/255.0,1/255.0]
        vertexData.extend(VD)
    vertexData=np.array(vertexData,dtype=np.float32)
    triangulos=[]
    triangulos.append(0)
    triangulos.append(1)
    triangulos.append(2)

    for j in range(particiones-1):
        triangulos.append(0)
        triangulos.append(j+1)
        triangulos.append(j+2)
    triangulos.append(0)
    triangulos.append(1)
    triangulos.append(particiones)
    triangulos=np.array(triangulos,dtype=np.uint32)
    indices=triangulos
    
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

def createEdificio(pX,ancho):
    
    gpuShape=GPUShape()
    gpuShapeVentanas=[]
    pisos=random.randint(5,15)
    anchoVentana=ancho/17    #Cada piso tendra 8 ventanas, independiente del ancho del edificio     
    AP=0.05                     #Altura por piso
    vertexDataEdificio = [
        pX,-0.5, 0, 76/255.0,69/255.0,23/255.0,
        pX+ancho, -0.5, 0, 76/255.0,69/255.0,23/255.0,
        pX,-0.5+ pisos*AP, 0, 76/255.0,69/255.0,23/255.0,
        pX+ancho,-0.5+ pisos*AP, 0, 76/255.0,69/255.0,23/255.0
        
    ]
    
    
    indicesEdificio =   [0, 1, 2,
                1, 2, 3,
                ]
    contador=0
    
    for i in range(pisos):
        for j in range(16):
            if j in [0,2,4,6,8,10,12,14,16]:
                ventana=GPUShape()
                vertexDataVentanas=[]
                indicesVentanas=[]
                punto1=[pX+(j+1)*anchoVentana,-0.5+i*AP+0.01,0,190/255.0,229/255.0,1]
                punto2=[pX+(j+1)*anchoVentana,-0.5+i*AP+0.04,0,190/255.0,229/255.0,1]
                punto3=[pX+(j+2)*anchoVentana,-0.5+i*AP+0.01,0,190/255.0,229/255.0,1]
                punto4=[pX+(j+2)*anchoVentana,-0.5+i*AP+0.04,0,190/255.0,229/255.0,1]
                vertexDataVentanas.extend(punto1)
                vertexDataVentanas.extend(punto2)
                vertexDataVentanas.extend(punto3)
                vertexDataVentanas.extend(punto4)
                indicesVentanas.extend([contador,contador+1,contador+2])
                indicesVentanas.extend([contador+1,contador+2,contador+3])
                #contador=contador+4
                vertexDataVentanas=np.array(vertexDataVentanas,dtype=np.float32)
                indicesVentanas=np.array(indicesVentanas,dtype=np.uint32)
                ventana.size=len(indicesVentanas)
                ventana.vao = glGenVertexArrays(1)
                ventana.vbo = glGenBuffers(1)
                ventana.ebo = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, ventana.vbo)
                glBufferData(GL_ARRAY_BUFFER, len(vertexDataVentanas) * INT_BYTES, vertexDataVentanas, GL_STATIC_DRAW)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ventana.ebo)
                glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indicesVentanas) * INT_BYTES, indicesVentanas, GL_STATIC_DRAW)
                gpuShapeVentanas.append(ventana)
    vertexDataEdificio=np.array(vertexDataEdificio,dtype=np.float32)
    indicesEdificio=np.array(indicesEdificio,dtype=np.uint32)
    
    
    gpuShape.size = len(indicesEdificio)
    

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)
    

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexDataEdificio) * INT_BYTES, vertexDataEdificio, GL_STATIC_DRAW)
    

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indicesEdificio) * INT_BYTES, indicesEdificio, GL_STATIC_DRAW)
    

    return [gpuShape,gpuShapeVentanas]


def createArbol(x,y):
    gpuShape=GPUShape()
    vertexData=np.array([
        x,y+0.05,0,58/255.0,2/255.0,2/255.0,
        x+0.01,y,0,58/255.0,2/255.0,2/255.0,
        x-0.01,y,0,58/255.0,2/255.0,2/255.0,
        x,y+0.02+0.05,0,0,104/255.0,31/255.0,
        x+0.018,y+0.02,0,0,104/255.0,31/255.0,
        x-0.018,y+0.02,0,0,104/255.0,31/255.0],dtype=np.float32)
    indices=np.array([
        0,1,2,
        3,4,5],dtype=np.uint32)
    gpuShape.size=len(indices)
    
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)
    

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

    
        
        



if __name__ == "__main__":
    if not glfw.init():
        sys.exit()
    EDIFICIOS=int(sys.argv[1])
    #EDIFICIOS=random.randint(5,20)
    width = 1000
    height = 1000

    window = glfw.create_window(width, height, "Ciudad", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)

    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
    }
    """


    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    fragment_shader_night = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor.r * 0.2, fragColor.g * 0.2, (fragColor.b + 0.2) * 0.5, 1.0f);
    }
    """

    fragment_shader_night_light="""
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor =vec4((fragColor.r * 0)+0.9, (fragColor.g * 0)+0.9, (fragColor.b * 0.2) * 0.5, 1.0f);
    }
    """

    fragment_shader_moon="""
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor =vec4(fragColor.r+1, fragColor.g + 1, (fragColor.b + 1) * 1, 1.0f);
    }
    """

    
    


    
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    shaderProgramNight = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_night, GL_FRAGMENT_SHADER))

    shaderProgramNightLight=OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_night_light, GL_FRAGMENT_SHADER))

    shaderProgramMoon=OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_moon, GL_FRAGMENT_SHADER))

    glClearColor(0.15, 0.15, 0.15, 1.0)


    gpuCielo=createCielo()
    gpuSuelo=createSuelo()
    gpuSol=createSol()
    gpuNube=createNube()
    arregloArboles=[]
    arregloEscalasArboles=[]
    nArboles=20
    for i in range(nArboles):
        x=random.uniform(-0.9,0.9)
        y=random.uniform(-0.9,-0.6)
        arregloArboles.append(createArbol(x,y))
        arregloEscalasArboles.append(random.uniform(0.5,1.5))

    arregloEdificios=[]
    arregloVentanas=[]
    separacion=(0.2/(EDIFICIOS+1))
    
    ancho=1.8/EDIFICIOS
    px=-1+separacion
    for i in range(EDIFICIOS):
        edificio=createEdificio(px,ancho)
        arregloEdificios.append(edificio[0])
        arregloVentanas.extend(edificio[1])
        
        
        px=px+separacion+ancho

    randomVentanas=[]
    
    for x in range(len(arregloVentanas)):
        rnd=random.randint(1,2)
        if (rnd%2)==0:
            randomVentanas.append(x)
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        transform=tr.matmul([tr.uniformScale(controller.zoom),tr.translate(controller.x,controller.y,0.0)])
        if controller.useNight:
            # Telling OpenGL to use our shader program
            glUseProgram(shaderProgramNight)

            drawShape(shaderProgramNight, gpuCielo,transform)
            drawShape(shaderProgramNight, gpuSuelo,transform)
            
            for j in range(EDIFICIOS):
                glUseProgram(shaderProgramNight)
                drawShape(shaderProgramNight,arregloEdificios[j],transform)
            ventanasPrendidas=[]
            ventanasApagadas=[]
            for i in range(nArboles):
                
                drawShape(shaderProgramNight,arregloArboles[i],transform)
            drawShape(shaderProgramNight, gpuNube, transform)
            
            glUseProgram(shaderProgramNightLight)
            for z in range(len(arregloVentanas)):
                

                if z in randomVentanas:
                    drawShape(shaderProgramNightLight,arregloVentanas[z],transform)
            glUseProgram(shaderProgramMoon)
            drawShape(shaderProgramMoon, gpuSol,transform)
            
           
                
        # Telling OpenGL to use our shader program
        else:
            glUseProgram(shaderProgram)
            
            drawShape(shaderProgram, gpuCielo,transform)
            drawShape(shaderProgram, gpuSuelo,transform)
            drawShape(shaderProgram, gpuSol,transform)
            drawShape(shaderProgram, gpuNube, transform)
            for j in range(EDIFICIOS):
                drawShape(shaderProgram,arregloEdificios[j],transform)
            for l in range(len(arregloVentanas)):
                drawShape(shaderProgram,arregloVentanas[l],transform)
            for i in range(nArboles):
                
                drawShape(shaderProgram,arregloArboles[i],transform)
           
            
            
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)


    glfw.terminate()



