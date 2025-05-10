from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
player_x = 0.0
player_z = 0.0
player_angle = 0.0
player_health = 100
player_score = 0
game_over = False
enemies = []
bullets = []
explosions = []
bullet_speed = 0.5
camera_distance = 10.0
camera_height = 5.0
camera_angle = 0.0
move_forward = move_backward = move_left = move_right = False
movement_speed = 0.3
rotation_speed = 3.0
world_size = 50
trees = []

def init():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Test Case - Small Enemies and Trees")
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 200, 0, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
    
    glClearColor(0.15, 0.15, 0.15, 1.0)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(WINDOW_WIDTH)/float(WINDOW_HEIGHT), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    
    generate_environment()

def generate_environment():
    global trees, enemies
    trees = []
    num_trees = 20
    for _ in range(num_trees):
        x = random.uniform(-world_size + 5, world_size - 5)
        z = random.uniform(-world_size + 5, world_size - 5)
        if abs(x) < 10 and abs(z) < 10:
            continue
        scale = random.uniform(0.5, 0.8) 
        trees.append((x, z, scale))
    enemies = []
    num_enemies = 5
    for _ in range(num_enemies):
        angle = random.uniform(0, 360)
        distance = random.uniform(15, world_size - 5)
        x = math.sin(math.radians(angle)) * distance
        z = math.cos(math.radians(angle)) * distance
        enemies.append({
            "x": x,
            "y": 0,
            "z": z,
            "angle": random.uniform(0, 360),
            "scale": 0.5
        })

def draw_ground():
    glColor3f(0.4, 0.25, 0.1)
    glPushMatrix()
    glTranslatef(0, -0.5, 0)
    glScalef(world_size, 1, world_size)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_tree(x, z, scale=1.0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glColor3f(0.4, 0.2, 0.1)
    glPushMatrix()
    glTranslatef(0, scale * 0.5, 0)
    glScalef(0.2 * scale, scale, 0.2 * scale)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(0.0, 0.6, 0.0)
    glPushMatrix()
    glTranslatef(0, scale * 1.2, 0)
    glScalef(0.8 * scale, 0.8 * scale, 0.8 * scale)
    glutSolidCube(1.0)
    glPopMatrix()
    
    glPopMatrix()

def draw_enemy(enemy):
    x, y, z, angle, scale = enemy["x"], enemy["y"], enemy["z"], enemy["angle"], enemy["scale"]
    
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle, 0, 1, 0)
    glScalef(scale, scale, scale)
    glColor3f(0.8, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(0.4, 0.6, 0.3)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(0.9, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glutSolidSphere(0.2, 16, 16)
    glPopMatrix()
    arm_positions = [(-0.25, 1.0, 0), (0.25, 1.0, 0)]
    for ax, ay, az in arm_positions:
        glPushMatrix()
        glTranslatef(ax, ay, az)
        glScalef(0.1, 0.3, 0.1)
        glColor3f(0.7, 0.1, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()
    leg_positions = [(-0.15, 0.5, 0), (0.15, 0.5, 0)]
    for lx, ly, lz in leg_positions:
        glPushMatrix()
        glTranslatef(lx, ly, lz)
        glScalef(0.1, 0.4, 0.1)
        glColor3f(0.7, 0.1, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()
    
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(player_x, 0, player_z)
    glRotatef(player_angle, 0, 1, 0)
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(0.4, 0.6, 0.3)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(0.0, 0.0, 0.8)
    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glutSolidSphere(0.2, 16, 16)
    glPopMatrix()
    arm_positions = [(-0.25, 1.0, 0), (0.25, 1.0, 0)]
    for ax, ay, az in arm_positions:
        glPushMatrix()
        glTranslatef(ax, ay, az)
        glScalef(0.1, 0.3, 0.1)
        glColor3f(0.0, 0.0, 0.7)
        glutSolidCube(1.0)
        glPopMatrix()
    leg_positions = [(-0.15, 0.5, 0), (0.15, 0.5, 0)]
    for lx, ly, lz in leg_positions:
        glPushMatrix()
        glTranslatef(lx, ly, lz)
        glScalef(0.1, 0.4, 0.1)
        glColor3f(0.0, 0.0, 0.7)
        glutSolidCube(1.0)
        glPopMatrix()
    
    glPopMatrix()

def draw_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.0, 1.0, 0.0)
    glutSolidSphere(0.2, 16, 16)
    glPopMatrix()

def update_bullets():
    global bullets
    new_bullets = []
    for bullet in bullets:
        x, y, z, angle = bullet
        new_x = x + math.sin(math.radians(angle)) * bullet_speed
        new_z = z + math.cos(math.radians(angle)) * bullet_speed
        if abs(new_x) < world_size and abs(new_z) < world_size:
            new_bullets.append((new_x, y, new_z, angle))
    bullets = new_bullets

def setup_camera():
    cam_x = player_x - math.sin(math.radians(camera_angle)) * camera_distance
    cam_y = camera_height
    cam_z = player_z - math.cos(math.radians(camera_angle)) * camera_distance
    gluLookAt(cam_x, cam_y, cam_z, player_x, 0, player_z, 0, 1, 0)

def mouse(button, state, x, y):
    global bullets
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullet_x = player_x + math.sin(math.radians(player_angle)) * 1.5
        bullet_y = 1.0  
        bullet_z = player_z + math.cos(math.radians(player_angle)) * 1.5
        bullets.append((bullet_x, bullet_y, bullet_z, player_angle))

def update(value):
    update_bullets()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_camera()
    
    draw_ground()
    
    for tree in trees:
        x, z, scale = tree
        draw_tree(x, z, scale)
    
    for enemy in enemies:
        draw_enemy(enemy)
    
    for bullet in bullets:
        x, y, z, _ = bullet
        draw_bullet(x, y, z)
    
    draw_player()
    
    glutSwapBuffers()

def keyboard(key, x, y):
    global player_x, player_z, player_angle, camera_angle
    
    if key == b'w':
        player_x += math.sin(math.radians(player_angle)) * 0.5
        player_z += math.cos(math.radians(player_angle)) * 0.5
    elif key == b's':
        player_x -= math.sin(math.radians(player_angle)) * 0.5
        player_z -= math.cos(math.radians(player_angle)) * 0.5
    elif key == b'a':
        player_angle = (player_angle + 5) % 360
        camera_angle = player_angle
    elif key == b'd':
        player_angle = (player_angle - 5) % 360
        camera_angle = player_angle
    elif key == b'q':
        glutLeaveMainLoop()
    
    glutPostRedisplay()

def reshape(w, h):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH = w
    WINDOW_HEIGHT = h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(w)/float(h), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(16, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main() 