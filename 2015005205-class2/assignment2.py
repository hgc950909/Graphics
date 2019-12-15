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

threeiarr=np.array([])
threevarr=np.array([])
threevvarr=np.array([])
fourvvarr=np.array([])

isnormal=0
shading=0
control=0

def render():
    global fov,px,py,pz,H,V,Rbut,Lbut,c,a,M,up,at,control,shading,isnormal
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if control == 1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1,.001,1000)
   
    M=np.array([ fov*np.cos(H)*np.sin(V),fov*np.sin(H),fov*np.cos(H)*np.cos(V)])
    up=np.array([0,c,0])
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(M[0],M[1],M[2],at[0],at[1],at[2],up[0],up[1],up[2])
    glTranslatef(a[0],a[1],a[2])
    drawfloor()
    drawFrame()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_RESCALE_NORMAL)
    glPushMatrix()

    lightPos = (30.,40.,50.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    
    lightColor = (1,0,0,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)

    glPushMatrix()
    lightPos = (-30.,40.,50.,0.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()
    
    lightColor = (0,0,1,0.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)


    specularObjectColor = (1.,1.,1.,1.)
    objectColor = (1,1,1,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glPushMatrix()
    if isnormal==1:
        if shading ==0:
            drawMesh()
        elif shading ==1:
            drawcalMesh()
    else:
        drawcalMesh()
    glPopMatrix()
    glDisable(GL_LIGHTING)

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

def key_callback(window, key, scancode, action, mods):
    global control,shading
    if action==glfw.PRESS:
        if key==glfw.KEY_Z:
            if control ==0:
                control=1
            elif control ==1:
                control=0
        elif key==glfw.KEY_S:
            if shading ==0:
                shading =1
            elif shading ==1:
                shading =0


def scroll_callback(window, xoffset, yoffset):
    global fov
    if fov>= 1 :
        fov -=yoffset*0.4
    elif fov <= 1:
        fov = 1


def drop_callback(window, filenames):
    global threevarr,fourvarr,threevvarr,fourvvarr,isnormal
    vline=[]
    vnline=[]
    f3line=[]
    f4line=[]
    f5line=[]
    cntv=0
    cntn=0
    cntface=0
    cntthree=0
    cntfour=0
    cntfive=0
    with open(filenames[0],"r")as fiLE:
        while True:
            line =fiLE.readline()
            if line =="\n":
                continue
            if not line:
                break
            temp= line.split()
            if temp[0] == 'v':
                cntv=cntv+1
                vline.append(line)
            elif temp[0] == 'vn':
                cntn=cntn+1
                vnline.append(line)
            elif temp[0] == 'f':
                cntface=cntface+1
                if len(temp) == 4:
                    cntthree=cntthree+1
                    f3line.append(line)
                elif len(temp) == 5:
                    cntfour=cntfour+1
                    f4line.append(line)
                elif len(temp) >5:
                    cntfive=cntfive+1
                    f3line.append(line)


    ver=np.empty((cntv,3),dtype='float32')
    for i in range(0,cntv):
        temp= vline[i].split()
        ver[i]=np.array([[temp[1],temp[2],temp[3].rstrip('\n')]],dtype='float32')

    nor=np.empty((cntn,3),dtype='float32')
    for i in range(0,cntn):
        temp = vnline[i].split()
        nor[i]=np.array([[temp[1],temp[2],temp[3].rstrip('\n')]],dtype='float32')

    #세개짜리..
    threeiarr=np.empty((cntthree+cntfive,3),dtype='int32')
    threevarr=np.empty(((cntthree+cntfive)*6,3),'float32')
    for i in range(0,cntthree+cntfive):
        temp=f3line[i].split()
        temp1=temp[1].split('/')
        temp2=temp[2].split('/')
        temp3=temp[3].split('/')
        
        threeiarr[i]= np.array([[temp1[0],temp2[0],temp3[0]]],dtype='int32')
        if len(temp1)==3:#normal있을때
            isnormal=1
            threevarr[i*6]=nor[int(temp1[2])-1]
            threevarr[i*6+1]=ver[int(temp1[0])-1]
            threevarr[i*6+2]=nor[int(temp2[2])-1]
            threevarr[i*6+3]=ver[int(temp2[0])-1]
            threevarr[i*6+4]=nor[int(temp3[2])-1]
            threevarr[i*6+5]=ver[int(temp3[0])-1]

    #네개짜리
    fouriarr=np.empty((cntfour,4),dtype='int32')
    fourvarr=np.empty((cntfour*8,3),'float32')
    for i in range(0,cntfour):
        temp=f4line[i].split()
        temp1=temp[1].split('/')
        temp2=temp[2].split('/')
        temp3=temp[3].split('/')
        temp4=temp[4].split('/')
        fouriarr[i]= np.array([[temp1[0],temp2[0],temp3[0],temp4[0]]],dtype = 'int32')
        if len(temp1)==3:#normal있을때
            isnormal=1
            fourvarr[i*8]=nor[int(temp1[2])-1]
            fourvarr[i*8+1]=ver[int(temp1[0])-1]
            fourvarr[i*8+2]=nor[int(temp2[2])-1]
            fourvarr[i*8+3]=ver[int(temp2[0])-1]
            fourvarr[i*8+4]=nor[int(temp3[2])-1]
            fourvarr[i*8+5]=ver[int(temp3[0])-1]
            fourvarr[i*8+6]=nor[int(temp4[2])-1]
            fourvarr[i*8+7]=ver[int(temp4[0])-1]

    #normal벡터 구하기
    threevvarr=np.empty(((cntthree+cntfive)*6,3),'float32')
    fourvvarr=np.empty((cntfour*8,3),'float32')
    norvec=np.zeros((cntv,3),dtype='float32')
    for i in range(0,cntthree+cntfive):
        temp=np.cross(ver[threeiarr[i][1]-1]-ver[threeiarr[i][0]-1], ver[threeiarr[i][2]-1]-ver[threeiarr[i][0]-1])
        for j in range(0,3):
            norvec[threeiarr[i][j]-1]+=temp

    for i in range(0,cntfour):
        temp=np.cross(ver[fouriarr[i][1]-1]-ver[fouriarr[i][0]-1], ver[fouriarr[i][3]-1]-ver[fouriarr[i][0]-1])
        for j in range(0,4):
            norvec[fouriarr[i][j]-1]+=temp

    for i in range(0,cntv):
        temp=np.sqrt(np.dot(norvec[i],norvec[i]))
        if temp !=0:
            norvec[i]=norvec[i]/temp

    for i in range(0,cntthree+cntfive):
        threevvarr[i*6]=norvec[threeiarr[i][0]-1]
        threevvarr[i*6+1]=ver[threeiarr[i][0]-1]
        threevvarr[i*6+2]=norvec[threeiarr[i][1]-1]
        threevvarr[i*6+3]=ver[threeiarr[i][1]-1]
        threevvarr[i*6+4]=norvec[threeiarr[i][2]-1]
        threevvarr[i*6+5]=ver[threeiarr[i][2]-1]
        
    for i in range(0,cntfour):
        fourvvarr[i*8]=norvec[fouriarr[i][0]-1]
        fourvvarr[i*8+1]=ver[fouriarr[i][0]-1]
        fourvvarr[i*8+2]=norvec[fouriarr[i][1]-1]
        fourvvarr[i*8+3]=ver[fouriarr[i][1]-1]
        fourvvarr[i*8+4]=norvec[fouriarr[i][2]-1]
        fourvvarr[i*8+5]=ver[fouriarr[i][2]-1]
        fourvvarr[i*8+6]=norvec[fouriarr[i][3]-1]
        fourvvarr[i*8+7]=ver[fouriarr[i][3]-1]

        #filename
    print("Filename :",filenames[0])
        #total number of faces
    print("Total number of faces:", cntface)
        #Number of faces with 3vertices
    print("Number of faces with 3 vertices:" ,cntthree)
        #Number of faces with 4vertices
    print("Number of faces with 4vertices:" , cntfour)
        #Number of faces with more than 4 vertices
    print("Number of faces with more than 4 vertices:",cntfive)

def drawMesh():
    global threevarr,fourvarr
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glNormalPointer(GL_FLOAT, 6*threevarr.itemsize, threevarr)
    glVertexPointer(3, GL_FLOAT, 6*threevarr.itemsize,ctypes.c_void_p(threevarr.ctypes.data + 3*threevarr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(threevarr.size/6))

    glNormalPointer(GL_FLOAT, 6*fourvarr.itemsize, fourvarr)
    glVertexPointer(3, GL_FLOAT, 6*fourvarr.itemsize,ctypes.c_void_p(fourvarr.ctypes.data + 3*fourvarr.itemsize))
    glDrawArrays(GL_QUADS, 0, int(fourvarr.size/6))

def drawcalMesh():
    global threevvarr,fourvvarr
  
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glNormalPointer(GL_FLOAT, 6*threevvarr.itemsize, threevvarr)
    glVertexPointer(3, GL_FLOAT, 6*threevvarr.itemsize,ctypes.c_void_p(threevvarr.ctypes.data + 3*threevvarr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(threevvarr.size/6))

    glNormalPointer(GL_FLOAT, 6*fourvvarr.itemsize, fourvvarr)
    glVertexPointer(3, GL_FLOAT, 6*fourvvarr.itemsize,ctypes.c_void_p(fourvvarr.ctypes.data + 3*fourvvarr.itemsize))
    glDrawArrays(GL_QUADS, 0, int(fourvvarr.size/6))

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,"2015005205",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
   
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    
    glfw.terminate()
if __name__ == "__main__":
    main()
