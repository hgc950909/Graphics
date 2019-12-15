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

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawUnitCube():
    glBegin(GL_QUADS)
    glColor3ub(0,255,255)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
    
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()


def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) /float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def Running():
    t = glfw.get_time()*5
    glPushMatrix()
    glTranslatef(0,-.1,0)
    glPushMatrix()
    glTranslatef(0,5,0)
    glScale(.2,.2,.2)
    drawSphere()
    glPopMatrix()
    #몸통
    glPushMatrix()
    glTranslate(0,4,0)
    glScale(.2,.7,.4)
    drawCube()
    glPopMatrix()
    
    #오른쪽다리
    glPushMatrix()
    glTranslatef(0,3,0)
    glRotatef(-np.cos(t)*30-10,0,0,1)
    glTranslatef(0,-3.2,0)
    glPushMatrix()
    glTranslate(0,2.5,-.3)
    glScale(.2,.7,.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,1.6,0)
    glRotatef(-np.cos(t)*30+30,0,0,1)
    glTranslatef(0,-1.6,0)
    glPushMatrix()
    glTranslate(0,1.1,-.3)
    glScale(.2,.6,.1)
    drawCube()
    glPopMatrix()
    #
    glPushMatrix()
    glTranslatef(0.1,-0.3,0)
    glRotatef(-np.cos(t)*10+10,0,0,1)
    glTranslatef(-0.1,0.3,0)
    glPushMatrix()
    glTranslate(-.2,.3,-.3)
    glScale(.4,.1,.1)
    drawCube()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    #왼쪽다리
    glPushMatrix()
    glTranslatef(0,3,0)
    glRotatef(np.cos(t)*30-10,0,0,1)
    glTranslatef(0,-3.2,0)
    glPushMatrix()
    glTranslate(0,2.5,.3)
    glScale(.2,.7,.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,1.6,0)
    glRotatef(np.cos(t)*30+30,0,0,1)
    glTranslatef(0,-1.6,0)
    glPushMatrix()
    glTranslate(0,1.1,.3)
    glScale(.2,.6,.1)
    drawCube()
    glPopMatrix()
    #
    glPushMatrix()
    glTranslatef(0.1,-0.3,0)
    glRotatef(np.cos(t)*10+10,0,0,1)
    glTranslatef(-0.1,0.3,0)
    glPushMatrix()
    glTranslate(-.2,.3,.3)
    glScale(.4,.1,.1)
    drawCube()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    #왼쪽팔
    glPushMatrix()
    glTranslate(0,4.5,0)
    glRotatef(-np.cos(t)*35,0,0,1)
    glTranslate(0,-4.5,0)
    glPushMatrix()
    glTranslate(0,4.25,.6)
    glScale(.2,.45,.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslate(0,3.8,0)
    glRotatef(-np.cos(t)*20-40,0,0,1)
    glTranslate(0,-3.8,0)
    glPushMatrix()
    glTranslate(0,3.25,.6)
    glScale(.2,.45,.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslate(0,2.55,.6)
    glScale(.15,.15,.15)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    #오른쪽팔
    glPushMatrix()
    glTranslate(0,4.5,0)
    glRotatef(np.cos(t)*35,0,0,1)
    glTranslate(0,-4.5,0)
    glPushMatrix()
    glTranslate(0,4.25,-.6)
    glScale(.2,.45,.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslate(0,3.8,0)
    glRotatef(-np.cos(t)*20-40,0,0,1)
    glTranslate(0,-3.8,0)
    glPushMatrix()
    glTranslate(0,3.25,-.6)
    glScale(.2,.45,.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslate(0,2.55,-.6)
    glScale(.15,.15,.15)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def render():
    global fov,px,py,pz,H,V,Rbut,Lbut,c,a,M,up,at
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    M=np.array([ 10*np.cos(H)*np.sin(V),10*np.sin(H),10*np.cos(H)*np.cos(V)])
    up=np.array([0,c,0])
    gluPerspective(fov, 1,.001,1000)
    gluLookAt(M[0],M[1],M[2],at[0],at[1],at[2],up[0],up[1],up[2])
    glTranslatef(a[0],a[1],a[2])
    drawfloor()
    drawFrame()
    Running()
   


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
    if fov>= 2 and fov <= 160:
        fov -=yoffset*0.4
    elif fov <= 2:
        fov = 2
    elif fov > 160:
        fov = 160
          
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2015005205",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
	main()
	
