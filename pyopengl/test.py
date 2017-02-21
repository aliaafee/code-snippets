from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from Vector import *

from numpy import matrix

import random

import Image


class Object(object):
    def __init__(self):
        self.color = Vector(1.0, 1.0, 1.0)
        self.material = None
        self.position = Vector(0, 0, 0)
        pass
        
        
    def animate(self):
        pass
        
        
    def gl_render_object(self):
        pass
        
        
    def gl_render(self):
        glColor3f(self.color.x, self.color.y, self.color.z)
        
        if self.material == None:
            glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0]);
            glMaterialfv(GL_FRONT, GL_DIFFUSE, [self.color.x, self.color.y, self.color.z, 1.0]);
            glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0]);
            glMaterialfv(GL_FRONT, GL_SHININESS, 60.0);
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0]);
        else:
            self.material.gl_render()
            
        glPushMatrix()
        
        glTranslatef(self.position.x, self.position.y, self.position.z)
        
        self.gl_render_object()
        
        glPopMatrix()
        
        if self.material != None:
            self.material.gl_end()
        
        
        
        
        
class Material(object):
    def __init__(self, ambient, diffuse, specular, shininess, emission):
        self.ambient = ambient # vector
        self.diffuse = diffuse # vector
        self.specular = specular
        self.shininess = shininess # float
        self.emission = emission # vector
        
        
    def gl_render(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT, [self.ambient.x, self.ambient.y, self.ambient.z, 1.0]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [self.diffuse.x, self.diffuse.y, self.diffuse.z, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [self.specular.x, self.specular.y, self.specular.z, 1.0]);
        glMaterialfv(GL_FRONT, GL_SHININESS, self.shininess);
        glMaterialfv(GL_FRONT, GL_EMISSION, [self.emission.x, self.emission.y, self.emission.z, 1.0]);
        
        
    def gl_end(self):
        pass
        
        
class Texture(Material):
    def __init__(self, texturefile):
        self.imageID = self.loadImage(texturefile)
        
        
    def loadImage(self, name):
        image = Image.open(name)
        
        ix = image.size[0]
        iy = image.size[1]
        try:
            image = image.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            image = image.tostring("raw", "RGBX", 0, -1)
            
        id = glGenTextures(1)
        
        print "image id = {0}".format(id)
        
        glBindTexture(GL_TEXTURE_2D, id)
        
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	    
        return id
	    
    def gl_render(self):
        
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glDisable(GL_LIGHTING)
        #glDisable(GL_DEPTH_TEST)
        glDepthMask( GL_FALSE)
        
        
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.imageID)
 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)    
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
        
    def gl_end(self):
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        #glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        
        
        
        
                 
class Vertex(object):
    def __init__(self, position, normal, uv=Vector(0.0, 0.0)):
        self.p = position
        self.n = normal
        self.uv = uv
        
        
class Face3(object):
    def __init__(self, v1, v2, v3):
        self.vertices = []
        self.vertices.append(v1)
        self.vertices.append(v2)
        self.vertices.append(v3)
        
        
    def gl_render(self):
        glBegin(GL_TRIANGLES)
        for vertex in self.vertices:
            glTexCoord2f(vertex.uv.x, vertex.uv.y)
            glNormal3f(vertex.n.x, vertex.n.y, vertex.n.z)
            glVertex3f(vertex.p.x, vertex.p.y, vertex.p.z)
        glEnd()
        
    
    
        
class VertexObject(Object):
    def __init__(self, color, material=None):
        Object.__init__(self)
        
        self.vertices = []
        self.faces = []
        self.color = color
        self.material = material
        
        
    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        
        
    def add_face(self, face):
        self.faces.append(face)
        
        
    def gl_render_object(self):
        for face in self.faces:
            face.gl_render()
           
        
        
        
class Sphere(Object):
    def __init__(self, position, radius, color, material=None):
        Object.__init__(self)
        
        self.position = position
        self.radius = radius
        self.color = color
        self.material = material
        
        
    def animate(self):
        pass
        
        
    def gl_render_object(self):
        glutSolidSphere(self.radius, 100, 100)
        '''
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        glEnd()
        '''
        

class Particle(object):
    def __init__(self, position, velocity, scale=1.0, alive=False):
        self.position = position
        self.velocity = velocity
        self.scale = scale
        self.alive = alive
        
        
    def animate(self):
        if self.alive:
            self.position += self.velocity
            self.scale += 0.01
            
            
    def gl_render(self, camera):
        if self.alive:
            glDisable(GL_LIGHTING)
            glBegin(GL_POINTS)
            
            glVertex3f(self.position.x, self.position.y, self.position.z)
            
            glEnd()
            glEnable(GL_LIGHTING)
        
        
        
class ParticleSphere(Particle):
    def __init__(self, position, velocity, scale=1.0, alive=False, radius=0.5):
        Particle.__init__(self, position, velocity, scale, alive)
        self.radius = radius
            
            
    def gl_render(self, camera):
        if self.alive:
            glPushMatrix()
            glTranslatef(self.position.x, self.position.y, self.position.z)
            glutSolidSphere(self.radius, 5, 4)
            glPopMatrix()
            
            
            
            
class ParticleBillboard(Particle):
    def __init__(self, position, velocity, scale=1.0, alive=False):
        Particle.__init__(self, position, velocity, scale, alive)
        
    
    def look_at(self, target):
        at = target - self.position
        at = at.unit()
        
        up = Vector(0.0, 0.0, 1.0)
        
        xaxis = at % up
        
        xaxis = xaxis.unit()
        
        up = xaxis % at
        
        at = at * -1
        
        M = [
            xaxis.x,    xaxis.y,    xaxis.z,    0.0,
            up.x,       up.y,       up.z,       0.0,
            at.x,       at.y,       at.z,       0.0,
            self.position.x, self.position.y, self.position.z, 1]
            
        glMultMatrixf(M)
        
        
    def gl_render(self, camera):
        if self.alive:
        
            glColor4f(0.0, 0.0, 0.0, 1.0/(self.scale*30.0))
            
            glDisable(GL_LIGHTING)
            
            glPushMatrix()
            
            #glTranslatef(self.position.x, self.position.y, self.position.z)
            
            
            
            #glPushMatrix()
            
            
            
            self.look_at(camera.position)
            
            glScalef(self.scale, self.scale, self.scale)
            
            glBegin (GL_QUADS)
            
            glTexCoord2f(1, 1)
            glVertex3f(0.3, 0.3, 0)
            
            glTexCoord2f(1, 0)
            glVertex3f(-0.3, 0.3, 0)
            
            glTexCoord2f(0, 0)
            glVertex3f(-0.3, -0.3, 0)
            
            glTexCoord2f(0, 1)
            
            glVertex3f(0.3, -0.3, 0)
            
            glEnd ()
            
            #glPopMatrix()
            
            glPopMatrix()
            
            glEnable(GL_LIGHTING)
        


class ParticleSystem(Object):
    def __init__(self, position, origin, count, camera, 
                    particle_type=Particle, type_args=[], material=None):
        Object.__init__(self)
        
        self.position = position
        self.origin = origin
        self.material = material
        self.camera = camera
        
        self.particles = []
        
        for c in range(1, count+1):
            args = [Vector(0, 0, 0), Vector(0, 0, 0), 1.0, False] + type_args
                
            self.particles.append(particle_type(*args))
                    
        self.counter = 0
        
        
    def generate_particle(self):
        selected = self.particles[self.counter] 
        selected.position = self.origin + Vector(0, 0, 0)
        selected.velocity = Vector(
            random.uniform(-0.01, 0.01), 
            random.uniform(-0.01, 0.01), 
            random.uniform(0.01, 0.02))
        selected.scale = 1.0
        selected.alive = True
        
        self.counter += 1
        if self.counter >= len(self.particles):
            self.counter = 0
        
        
    def animate(self):
        self.generate_particle()
        
        for particle in self.particles:
            particle.animate()
            
            
    def gl_render_object(self):
        #print self.camera.position
        for particle in self.particles:
            particle.gl_render(self.camera)
        
        
        
        
        
            
            
class Camera(object):
    def __init__(self):
        pass
        
        
    def orbit(self, dt, da):
        pass
        
        
    def dolly(self, d):
        pass
        
        
    def animate(self):
        pass
        
        
    def setup(self, w, h):
        pass
        
        
class TargetCamera(Camera):
    def __init__(self, position, target):
        self.position = position
        self.target = target
    
    
    def orbit(self, dt, da):
        v = self.position - self.target
        
        v.to_spherical()
        
        v.y += dt
        v.z += da
        
        v.to_cartesian()
        
        self.position = self.target + v
        
        
    def dolly(self, d):
        v = self.target - self.position
        
        #vu = v.unit()
        vu = v
        
        vu *= d
        
        self.position += vu
        #self.target += vu
            
        
    def setup(self, width, height):
        glViewport(0, 0, width, height)
        
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, float(width)/float(height), 1, 1000)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        
        gluLookAt(
            self.position.x, self.position.y, self.position.z,
            self.target.x, self.target.y, self.target.z,
            0.0, 0.0, 1.0);
        '''
        F = self.target - self.position
        
        f = F.unit()
        nUP = Vector(0.0, 0.0, 1.0)
        
        s = f % nUP
        s = s.unit()
        u = s % f
        f *= -1
        
        M = [
            s.x,    u.x,    f.x,    0,
            s.y,    u.y,    f.y,    0,
            s.z,    u.z,    f.z,    0,
            0,      0,      0,      1]
        
        glMultMatrixf(M)
        
        glTranslated(
            self.position.x*-1, 
            self.position.y*-1, 
            self.position.z*-1)
        '''
            
            
        
            
            
            
            
class Light(object):
    def __init__(self):
        pass
        
        
    def animate(self):
        pass
        
    def gl_render(self):
        pass
    
    
class PointLight(Light):
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity
        
        
    def gl_render(self):
        light_ambient =  [0.0, 0.0, 0.0, 1.0]
        light_diffuse =  [1.0, 1.0, 1.0, 1.0]
        light_specular =  [1.0, 1.0, 1.0, 1.0]
        #  light_position is NOT default value
        light_position =  [self.position.x, self.position.y, self.position.z, 0.0]

        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHT0)
        
        
            
        
        
class Scene(object):
    def __init__(self, camera):
        self.objs = []
        self.camera = camera
        self.lights = []
        
        self.width = 640
        self.height = 480
        
        
    def add_object(self, obj):
        self.objs.append(obj)
        
        
    def add_light(self, light):
        self.lights.append(light)
        
        
    def animate(self):
        for obj in self.objs:
            obj.animate()
            
        for light in self.lights:
            light.animate()
            
        self.camera.animate()
        
        
    def gl_axes(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(100.0, 0.0, 0.0)
        
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 100.0, 0.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 100.0)
        
        glEnd()
        
        
    def gl_render(self):
        self.camera.setup(self.width, self.height)
        
        if len(self.lights) > 0:
            glEnable(GL_LIGHTING)
            for light in self.lights:
                light.gl_render()
            
        for obj in self.objs:
            obj.gl_render()
            
        self.gl_axes()
            
            
            
            
scene = Scene(
    camera = TargetCamera(
        position = Vector(0,10,1),
        target = Vector(0,0,0)))

origin = Vector(0, 1, 0)
speed = Vector(0, 0.2, 0)

def main():
    global scene, origin

    glutInit(sys.argv)
    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 100)
    
    #glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    
    glutCreateWindow("Test")
    
    init()

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutMouseFunc(mousebutton)
    glutMotionFunc(mousemove)
    
    #############################################
    
        
    mat = Material(
        ambient = Vector(0.7, 0.7, 0.7), 
        diffuse = Vector(0.1, 0.5, 0.8), 
        specular = Vector(1.0, 1.0, 1.0), 
        shininess = 50.0, 
        emission = Vector(0.3, 0.2, 0.2))
        
    tex1 = Texture('myfire.jpg')
    tex2 = Texture('smoke.png')
    
    thing = VertexObject(
        color = Vector(1.0, 0.0, 0.0),
        material = tex2)
    
    scene.add_light(
        PointLight(
            position = Vector(10.0, 10.0, 10.0), intensity = 1.0))
    
    thing.add_vertex(
        Vertex(
            position = Vector(0.0, 0.0, 0.0),
            normal = Vector(0.0, 0.0, 1.0),
            uv = Vector(0.0, 0.0)))
            
    thing.add_vertex(
        Vertex(
            position = Vector(0.0, 1.0, 0.0),
            normal = Vector(0.0, 0.0, 1.0),
            uv = Vector(0.0, 1.0)))
            
    thing.add_vertex(
        Vertex(
            position = Vector(0.5, 1.0, 0.0),
            normal = Vector(0.0, 0.0, 1.0),
            uv = Vector(0.5, 1.0)))
            
    thing.add_face(
        Face3(
            v1 = thing.vertices[0],
            v2 = thing.vertices[1],
            v3 = thing.vertices[2]))
            
    
        
            
    #scene.add_object(thing)
    
    
    
    scene.add_object(
        Sphere(origin, 0.2, Vector(1.0, 0.0, 0.0), mat))
    
    
    
    scene.add_object(
        ParticleSystem(
            position = Vector(0, 0, 0),
            origin = origin,
            count = 100,
            camera = scene.camera,
            particle_type = ParticleBillboard,
            type_args = [],
            material = tex1))
    
    
    ################################################
    
    
    animate(0)
    
    glutMainLoop()
    
def init():
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)
    
    glClearDepth(1.0)
    glClearColor(0.0, 0.0, 0.0, 0.0)    
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel (GL_SMOOTH)
    
    #####
    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
    glHint(GL_POINT_SMOOTH_HINT,GL_NICEST); 
    
    
def animate(etc):
    global scene, origin
    
    #Animation here
    scene.animate()
    
    #origin += speed
    
    if origin.y > 5.0:
        speed.y = -0.1
    if origin.y < -5.0:
        speed.y = 0.1
        
    
    
    glutPostRedisplay()
    glutTimerFunc(10, animate, 0)
    
    
def reshape(w, h):
    global scene
    
    scene.width = w
    scene.height = h
    
    glutPostRedisplay()
    
    
def mousebutton(button, state, x, y):
    global mouse_startx, mouse_starty, mouse_button
    
    if state == GLUT_DOWN:
        mouse_startx = x
        mouse_starty = y
        if button == GLUT_LEFT_BUTTON:
            mouse_button = "L"
        if button == GLUT_MIDDLE_BUTTON:
            mouse_button = "M"
        if button == GLUT_RIGHT_BUTTON:
            mouse_button = "R"
            
    
            
    if state == GLUT_UP:
        mouse_button = ""
        
    if button == 3:
        scene.camera.dolly(0.1)
        
    if button == 4:
        scene.camera.dolly(-0.1)
        
            
            
def mousemove(x, y):
    global mouse_startx, mouse_starty, mouse_button, scene
    
    if mouse_button == "R":
        dx = x - mouse_startx
        dy = mouse_starty - y
        
        mouse_startx = x
        mouse_starty = y
        
        scene.camera.orbit(float(dy) * 0.02, float(dx) * -0.02)
        glutPostRedisplay()
        
    if mouse_button == "M":
        dx = x - mouse_startx
        dy = mouse_starty - y
        
        mouse_startx = x
        mouse_starty = y
        
        scene.camera.dolly(float(dy)/100.0)
        glutPostRedisplay()
    
        
    
    
def display():
    global scene
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    scene.gl_render()

    glutSwapBuffers()
    glFlush()
    
    


main()
