import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

fov = 90 ; Lbut=0 ; Rbut=0 ; c=1
px=0 ; py=0 ; pz=0
nowx=240 ; nowy=240
H =-31 ; V =-5.0
M=np.array([ 0,0,0])
up=np.array([0,0,0])
a=np.array([0.0,0.0,0.0])
at=np.array([0,0,0])
moving=0
motion=[]
cf=0
frame=None
frametime=None
root=None
def drawfloor():
    glBegin(GL_LINES)
    glColor3ub(100,100,100)
    for i in range(-5,6):
        for j in range(-5,6):
            if i != 0 and j != 0:
                glVertex3f( i, 0, j)
                glVertex3f( -i, 0, j)
                
                glVertex3f( i, 0, j)
                glVertex3f(i, 0 ,-j)
    glVertex3f( 0, 0, 0)
    glVertex3f(-5, 0 ,0)
    
    glVertex3f( 0, 0, 0)
    glVertex3f(0, 0 ,-5)
    
    glColor3ub(255,0,0)
    glVertex3f( -5, 0, 5)
    glVertex3f(5, 0 , 5)
    
    glColor3ub(0,0,255)
    glVertex3f( -5, 0, -5)
    glVertex3f(5, 0 , -5)
    glEnd()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0,0,0]))
    glVertex3fv(np.array([5,0,0]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([0,0,0]))
    glVertex3fv(np.array([0,2,0]))
    glColor3ub(0,0,255)
    glVertex3fv(np.array([0,0,0]))
    glVertex3fv(np.array([0,0,5]))
    glEnd()
def createVertexArraySeparate():
    varr = np.array([
                     [0,1,0],            # v0 normal
                     [ 1.0, 1.0,0],   # v0 position
                     [0,1,0],            # v1 normal
                     [-1.0, 1.0,0],   # v1 position
                     [0,1,0],            # v2 normal
                     [-1.0, 1.0, 1.0],   # v2 position
                     
                     [0,1,0],            # v3 normal
                     [ 1.0, 1.0,0],   # v3 position
                     [0,1,0],            # v4 normal
                     [-1.0, 1.0, 1.0],   # v4 position
                     [0,1,0],            # v5 normal
                     [ 1.0, 1.0, 1.0],   # v5 position
                     
                     [0,-1,0],           # v6 normal
                     [ 1.0,-1.0, 1.0],   # v6 position
                     [0,-1,0],           # v7 normal
                     [-1.0,-1.0, 1.0],   # v7 position
                     [0,-1,0],           # v8 normal
                     [-1.0,-1.0,0],   # v8 position
                     
                     [0,-1,0],
                     [ 1.0,-1.0, 1.0],
                     [0,-1,0],
                     [-1.0,-1.0,0],
                     [0,-1,0],
                     [ 1.0,-1.0,0],
                     
                     [0,0,1],
                     [ 1.0, 1.0, 1.0],
                     [0,0,1],
                     [-1.0, 1.0, 1.0],
                     [0,0,1],
                     [-1.0,-1.0, 1.0],
                     
                     [0,0,1],
                     [ 1.0, 1.0, 1.0],
                     [0,0,1],
                     [-1.0,-1.0, 1.0],
                     [0,0,1],
                     [ 1.0,-1.0, 1.0],
                     
                     [0,0,-1],
                     [ 1.0,-1.0,0],
                     [0,0,-1],
                     [-1.0,-1.0,0],
                     [0,0,-1],
                     [-1.0, 1.0,0],
                     
                     [0,0,-1],
                     [ 1.0,-1.0,0],
                     [0,0,-1],
                     [-1.0, 1.0,0],
                     [0,0,-1],
                     [ 1.0, 1.0,0],
                     
                     [-1,0,0],
                     [-1.0, 1.0, 1.0],
                     [-1,0,0],
                     [-1.0, 1.0,0],
                     [-1,0,0],
                     [-1.0,-1.0,0],
                     
                     [-1,0,0],
                     [-1.0, 1.0, 1.0],
                     [-1,0,0],
                     [-1.0,-1.0,0],
                     [-1,0,0],
                     [-1.0,-1.0, 1.0],
                     
                     [1,0,0],
                     [ 1.0, 1.0,0],
                     [1,0,0],
                     [ 1.0, 1.0, 1.0],
                     [1,0,0],
                     [ 1.0,-1.0, 1.0],
                     
                     [1,0,0],
                     [ 1.0, 1.0,0],
                     [1,0,0],
                     [ 1.0,-1.0, 1.0],
                     [1,0,0],
                     [ 1.0,-1.0,0],
                     # ...
                     ], 'float32')
    return varr

def drawUnitCube_glDrawArray():
    varr = createVertexArraySeparate()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))




col = 0
def render():
    global fov,px,py,pz,H,V,Rbut,Lbut,c,a,M,up,at,root,frametime,frame,col,cf
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1,.001,1000)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    M=np.array([ fov*np.cos(H)*np.sin(V),fov*np.sin(H),fov*np.cos(H)*np.cos(V)])
    up=np.array([0,c,0])
    gluLookAt(M[0],M[1],M[2],at[0],at[1],at[2],up[0],up[1],up[2])
    glTranslatef(a[0],a[1],a[2])
    drawfloor()
    drawFrame()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    glEnable(GL_RESCALE_NORMAL)
    
    glPushMatrix()
    
    lightPos = (3.,4.,5.,0.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    
    lightColor = (1,1,1,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    
    specularObjectColor = (1.,1.,1.,1.)
    objectColor = (1,0,0,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glPushMatrix()
    
    gVertexArraySeparate = createVertexArraySeparate()
   
    if root != None:
        col=0
        draw_skeleton(root,cf)
    
    glPopMatrix()
    glDisable(GL_LIGHTING)



def drop_callback(window, filenames):
    global root,motion,frame,frametime,cf,long_dis
    long_dis=0
    cnt=0
    hierarchy=0
    stack=[]
    motion=[]
    cf=0
    root=[]
    name=[]
    node={
        "TYPE" : "",
        "NAME" : "",
        "OFFSET" : None,
        "CHANNELS" : None,
        "CHILDS" : None
    }
    with open(filenames[0],"r")as fiLE:
        while True:
            line =fiLE.readline()
            if line =="\n":
                continue
            if not line:
                break
            if line =="MOTION\n":
                hierarchy=1
            if line == "HIERARCHY\n":
                hierarchy=0
            
            if hierarchy ==0:
                temp= line.split()
                if temp[0] == "ROOT" or temp[0] == "JOINT" or temp[0] == "End":
                    
                    data = node.copy()
                    data["TYPE"] = temp[0]
                    data["NAME"] = temp[1]
                    if temp[0] != "End":
                        cnt+=1
                        name.append(temp[1])
                    stack.append(data)
                elif temp[0] == "OFFSET":
                    data=stack[-1]
                    data["OFFSET"]=np.array(temp[1:],'float32')
                elif temp[0] == "CHANNELS":
                    data=stack[-1]
                    data["CHANNELS"]=temp[2:]
                elif temp[0] == "}":
                    if len(stack) ==0:
                        print("error")
                    elif len(stack)==1:
                        root=stack[-1]
                        stack.pop()
                    else:
                        data=stack.pop()
                        if stack[-1]["CHILDS"] == None:
                            stack[-1]["CHILDS"] =[]
                        stack[-1]["CHILDS"].append(data)

            if hierarchy ==1:
                
                temp=line.split()
          
                if temp[0] == "Frames:":
                    frame = int(temp[1])
                elif temp[0] == "Frame":
                    frametime = float(temp[2])
                elif temp[0] != "MOTION":
                    a=np.array(temp,dtype = 'float32')
                    motion.append(a)
    print("FILENAME:",filenames[0])
    print("NUMBER OF FRAME:" , frame )
    print("FPS:",1/frametime)
    print("Number of joints:", cnt)
    print("List of all joint names:",name)
    long_distance(root)

long_dis=0
def long_distance(V):
    global long_dis
    if V ==None:
        return
    if V["CHILDS"] != None:
        for i in V["CHILDS"]:
            o=np.array((0,0,0))
            p=np.array(i["OFFSET"])
        length = np.sqrt(np.dot(p-o,p-o))
        if long_dis<length:
            long_dis=length
        long_distance(i)

def draw_skeleton(V,frame_cnt):
    global moving,frame,motion,col,long_dis
    
    if V ==None:
        return
    glPushMatrix()
    if V["TYPE"]=="ROOT":
        glTranslatef(V["OFFSET"][0],V["OFFSET"][1],V["OFFSET"][2])

    if V["CHANNELS"] != None and moving ==1:
        for i in V["CHANNELS"]:
            i=i.lower()
            if i == "xrotation":
                glRotatef(motion[frame_cnt][col],1,0,0)
            elif i == "yrotation":
                glRotatef(motion[frame_cnt][col],0,1,0)
            elif i == "zrotation":
                glRotatef(motion[frame_cnt][col],0,0,1)
            elif i == "xposition":
                glTranslatef(motion[frame_cnt][col],0,0)
            elif i == "yposition":
                glTranslatef(0,motion[frame_cnt][col],0)
            elif i == "zposition":
                glTranslatef(0,0,motion[frame_cnt][col])
            col+=1
    if V["CHILDS"] != None:
        
        for i in V["CHILDS"]:
            glPushMatrix()
            o=np.array((0,0,0))
            p=np.array(i["OFFSET"])
            
            
            new=np.array(i["OFFSET"])
            length=np.sqrt(np.dot(new,new))
            b=np.array([0-new[0],0-new[1],0-new[2]])
            if np.sqrt(np.dot(b,b))==0:
                w =np.array([0,0,0])
            else:
                w=b/np.sqrt(np.dot(b,b))
            up=np.array([0,1,0])
            u=np.cross(up,w)
            if np.sqrt(np.dot(u,u)) ==0:
                u=np.array([0,0,0])
            else:
                u=u/np.sqrt(np.dot(u,u))
            v=np.cross(w,u)
            M=np.array([[u[0],v[0],w[0],0],
                        [u[1],v[1],w[1],0],
                        [u[2],v[2],w[2],0],
                        [0,0,0,1]])
            glPushMatrix()
            glMultMatrixf(M.T)

            #glVertex3fv((0,0,0))
            #glVertex3fv(i["OFFSET"])
            glScalef(.05*long_dis,.05*long_dis,-length)
            drawUnitCube_glDrawArray()
            glPopMatrix()
            glTranslatef(i["OFFSET"][0],i["OFFSET"][1],i["OFFSET"][2])
            draw_skeleton(i,frame_cnt)

            glPopMatrix()

    glPopMatrix()

def button_callback(window,button,action,mod):
    global Lbut,Rbut,nowx,nowy
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            Lbut=1
            a=glfw.get_cursor_pos(window)
            nowx=a[0]
            nowy=a[1]
        elif action == glfw.RELEASE:
            Lbut=0
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            Rbut=1
            a=glfw.get_cursor_pos(window)
            nowx=a[0]
            nowy=a[1]
        elif action == glfw.RELEASE:
            Rbut=0

def cursor_callback(window,xpos,ypos):
    global px,py,pz,Lbut,Rbut,nowx,nowy,H,V,c,a,M,up,at
    
    if Rbut==1:
        px+=(xpos-nowx)*0.05
        py+=(nowy-ypos)*0.05
        w=(M-at)/np.sqrt(np.dot(M-at,M-at))
        u=np.cross(up,w)/np.sqrt(np.dot(np.cross(up,w),np.cross(up,w)))
        v=np.cross(w,u)
        a+=u*(xpos-nowx)*0.005+v*(nowy-ypos)*0.005
    
    elif Lbut ==1:
        H += 0.01 * (-nowy+ypos)
        if  np.cos(H)>=0:
            c=1
            V += 0.005* (nowx-xpos)
        elif np.cos(H)<0:
            c=-1
            V += 0.005* (xpos-nowx)
    nowx=xpos
    nowy=ypos


def scroll_callback(window, xoffset, yoffset):
    global fov
    if fov>= 1 :
        fov -=yoffset*0.4
    elif fov <= 1:
        fov = 1

def key_callback(window,key, scancode, action, mods):
    global moving,frame
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_SPACE:
            if moving ==1:
                moving =0
            else:
                moving =1

def main():
    global cf
    if not glfw.init():
        return
    window = glfw.create_window(640,640,"2015005205",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window,key_callback)
    glfw.make_context_current(window)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)


    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        if moving ==1:
            cf=(cf+1)%frame
        
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__ == "__main__":
    main()


