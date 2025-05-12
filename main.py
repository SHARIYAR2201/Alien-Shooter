from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random
import time
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
player_x = 0.0
player_y = 0.0
player_z = 0.0
player_angle = 0.0
player_health = 100
player_score = 0
game_over = False
enemies = []
bullets = []
explosions = []
power_ups = []
camera_distance = 10.0
camera_height = 5.0
camera_angle = 0.0
first_person = False
camera_smoothness = 0.1
target_camera_angle = 0.0
target_camera_height = 5.0
target_camera_distance = 10.0
camera_rotation_speed = 5.0
move_forward = move_backward = move_left = move_right = False
turn_left = turn_right = False
movement_speed = 0.3
rotation_speed = 3.0
strafe_speed = 0.2
trees = []
buildings = []
clouds = []
world_size = 200
cheat_mode = False
auto_aim = False
infinite_health = False
speed_boost = False
target_enemy = None
last_auto_fire_time = 0
auto_fire_cooldown = 0.2
missed_shots = 0
enemy_bullets = []
enemy_shoot_cooldown = 2.0 
last_enemy_shot_time = {}
leg_angle = 0.0
leg_direction = 1.0  
leg_speed = 5.0  
last_auto_shot_time = 0
auto_shot_cooldown = 0.3
scan_angle = 0
normal_speed = 0.3 
cheat_speed = 1.0
bullet_speed = 1.5
enemy_bullet_speed = 0.84
shield_on = False
current_level = 1
winner = False
is_paused = False

# (Level 3 boss Alien)
boss_active = False
boss_x = 0.0
boss_y = 0.0
boss_z = 0.0
boss_health = 300
boss_max_health = 300
boss_missile_timer = 0.0
boss_missile_cooldown = 2.0
boss_missiles = []

def init():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Shooting Game")
    
    glutSetCursor(GLUT_CURSOR_NONE)  # Hide cursor
    
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
    spawn_enemies(15)
    
def draw_player():
    global leg_angle
    
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
    for i, (ax, ay, az) in enumerate(arm_positions):
        glPushMatrix()
        glTranslatef(ax, ay, az)
        if i % 2 == 0:
            glRotatef(-leg_angle, 1, 0, 0)
        else:
            glRotatef(leg_angle, 1, 0, 0)
        glScalef(0.1, 0.3, 0.1)
        glColor3f(0.0, 0.0, 0.7)
        glutSolidCube(1.0)
        glPopMatrix()
    
    leg_positions = [(-0.15, 0.5, 0), (0.15, 0.5, 0)]
    for i, (lx, ly, lz) in enumerate(leg_positions):
        glPushMatrix()
        glTranslatef(lx, ly, lz)
        if i % 2 == 0:
            glRotatef(leg_angle, 1, 0, 0)
        else:
            glRotatef(-leg_angle, 1, 0, 0)
        glScalef(0.1, 0.4, 0.1)
        glColor3f(0.0, 0.0, 0.7)
        glutSolidCube(1.0)
        glPopMatrix()
    
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0.35, 1.0, 0)
    glRotatef(90, 0, 1, 0)
    glScalef(0.05, 0.05, 0.3)
    glutSolidCube(1.0)
    glPopMatrix()
    
    glPopMatrix()

def draw_enemy(x, y, z, angle):
    if current_level == 1:
        body_color = (0.8, 0.2, 0.2) 
        head_color = (0.9, 0.3, 0.3)
        limb_color = (0.7, 0.1, 0.1)
    elif current_level == 2:
        body_color = (0.6, 0.2, 0.8)  
        head_color = (0.7, 0.3, 0.9)
        limb_color = (0.5, 0.1, 0.7)
    else:
        body_color = (0.95, 0.85, 0.1) 
        limb_color = (0.85, 0.75, 0.05)
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle, 0, 1, 0)
    
    glColor3f(*body_color)
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(0.4, 0.6, 0.3)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(*head_color)
    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glutSolidSphere(0.2, 16, 16)
    glPopMatrix()
    arm_positions = [(-0.25, 1.0, 0), (0.25, 1.0, 0)]
    for i, (ax, ay, az) in enumerate(arm_positions):
        glPushMatrix()
        glTranslatef(ax, ay, az)
        if i % 2 == 0:
            glRotatef(-leg_angle, 1, 0, 0)
        else:
            glRotatef(leg_angle, 1, 0, 0)
        glScalef(0.1, 0.3, 0.1)
        glColor3f(*limb_color)
        glutSolidCube(1.0)
        glPopMatrix()
    leg_positions = [(-0.15, 0.5, 0), (0.15, 0.5, 0)]
    for i, (lx, ly, lz) in enumerate(leg_positions):
        glPushMatrix()
        glTranslatef(lx, ly, lz)
        if i % 2 == 0:
            glRotatef(leg_angle, 1, 0, 0)
        else:
            glRotatef(-leg_angle, 1, 0, 0)
        glScalef(0.1, 0.4, 0.1)
        glColor3f(*limb_color)
        glutSolidCube(1.0)
        glPopMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0.35, 1.0, 0)
    glRotatef(90, 0, 1, 0)
    glScalef(0.05, 0.05, 0.3)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

def draw_bullet(x, y, z, direction):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(direction, 0, 1, 0)
    
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    glScalef(0.2, 0.2, 0.4)
    glutSolidCube(1.0)
    glPopMatrix()
    
    glColor3f(0.0, 0.8, 0.0)
    glPushMatrix()
    glTranslatef(0, 0.5, 0.3)
    glScalef(0.1, 0.1, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()
    
    glPopMatrix()

def draw_explosion(x, y, z, size):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    glColor3f(1.0, 0.5, 0.0)
    for i in range(8):
        glPushMatrix()
        glRotatef(45 * i, 0, 1, 0)
        glTranslatef(0, 0, size)
        glutSolidSphere(0.2, 8, 8)
        glPopMatrix()
    
    glPopMatrix()
    
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
    glScalef(0.8 * scale, 0.4 * scale, 0.8 * scale)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(0.0, 0.7, 0.0)
    glPushMatrix()
    glTranslatef(0, scale * 1.6, 0)
    glScalef(0.6 * scale, 0.4 * scale, 0.6 * scale)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(0.0, 0.8, 0.0)
    glPushMatrix()
    glTranslatef(0, scale * 2.0, 0)
    glScalef(0.4 * scale, 0.4 * scale, 0.4 * scale)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

def draw_building(x, z):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(2, 4, 2)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(0.8, 0.8, 1.0)
    window_positions = [
        (-0.5, 1, 1.01),
        (0.5, 1, 1.01),
        (-0.5, 3, 1.01),
        (0.5, 3, 1.01),
        (-0.5, 1, -1.01),
        (0.5, 1, -1.01),
        (-0.5, 3, -1.01),
        (0.5, 3, -1.01)
    ]
    for pos in window_positions:
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(0.3, 0.5, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()
    
    glPopMatrix()

def draw_hud():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 1.0, 0.0)
    level_text = f"LEVEL: {current_level}"
    text_width = len(level_text) * 10
    glRasterPos2f(WINDOW_WIDTH/2 - text_width/2, 30)
    for char in level_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(20, 60)
    score_text = f"Score: {player_score}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glRasterPos2f(20, 90)
    health_text = f"Health: {player_health}"
    for char in health_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glRasterPos2f(20, 120)
    camera_text = f"Camera: {'First Person' if first_person else 'Third Person'}"
    for char in camera_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glRasterPos2f(20, 150)
    missed_text = f"Missed: {missed_shots}"
    for char in missed_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    if cheat_mode:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(20, 180)
        cheat_text = "CHEAT MODE: ON"
        for char in cheat_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        y_pos = 210
        if auto_aim:
            glRasterPos2f(20, y_pos)
            aim_text = "AUTO-AIM: ON"
            for char in aim_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
            y_pos += 30     
        if infinite_health:
            glRasterPos2f(20, y_pos)
            health_text = "INFINITE HEALTH: ON"
            for char in health_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
            y_pos += 30 
        if speed_boost:
            glRasterPos2f(20, y_pos)
            speed_text = "SPEED BOOST: ON"
            for char in speed_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2)
        game_over_text = "GAME OVER"
        for char in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(WINDOW_WIDTH/2 - 70, WINDOW_HEIGHT/2 + 30)
        restart_text = "Press 'R' to restart"
        for char in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    if winner:
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(WINDOW_WIDTH/2 - 60, WINDOW_HEIGHT/2)
        winner_text = "WINNER!"
        for char in winner_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
def generate_environment():
    global trees, buildings, clouds
    trees = []
    num_trees = 300
    
    for _ in range(num_trees):
        x = random.uniform(-world_size + 120, world_size - 120)
        z = random.uniform(-world_size + 120, world_size - 120)
        scale = random.uniform(0.8, 1.2)
        color_variation = random.uniform(-0.1, 0.1)
        trees.append((x, z, scale, color_variation))
    
    buildings = []
    for _ in range(50):
        x = random.uniform(-world_size + 50, world_size - 50)
        z = random.uniform(-world_size + 50, world_size - 50)
        if abs(x) > 60 and abs(z) > 60:
            buildings.append((x, z))

    clouds = []
    for _ in range(30):
        x = random.uniform(-world_size * 1.5, world_size * 1.5)
        y = random.uniform(30, 50)
        z = random.uniform(-world_size * 1.5, world_size * 1.5)
        clouds.append((x, y, z))

def spawn_enemies(count):
    for _ in range(count):
        angle = random.uniform(0, 360)
        distance = random.uniform(40, world_size - 20)
        x = math.sin(math.radians(angle)) * distance
        z = math.cos(math.radians(angle)) * distance
        enemies.append([x, 0, z, random.uniform(0, 360)])

def check_collisions():
    global player_health, player_score, enemies, bullets, explosions
    
    for bullet in bullets[:]:
        bx, by, bz, _ = bullet
        for enemy in enemies[:]:
            ex, ey, ez, _ = enemy
            distance = math.sqrt((bx - ex)**2 + (by - ey)**2 + (bz - ez)**2)
            if distance < 1.0:
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    player_score += 10
                    explosions.append([ex, ey, ez, 1.0])
                break    
    for enemy in enemies:
        ex, ey, ez, _ = enemy
        distance = math.sqrt((ex - player_x)**2 + (ey - player_y)**2 + (ez - player_z)**2)
        if distance < 1.0:
            player_health -= 1
            if player_health <= 0:
                global game_over
                game_over = True

def find_nearest_enemy():
    if not enemies:
        return None
    nearest_enemy = None
    min_distance = float('inf')
    for enemy in enemies:
        dx = enemy[0] - player_x
        dz = enemy[2] - player_z
        distance = math.sqrt(dx * dx + dz * dz)
        if distance < min_distance:
            min_distance = distance
            nearest_enemy = enemy
    
    return nearest_enemy

def auto_target_enemy():
    global player_angle, bullets, last_auto_fire_time, target_enemy
    
    if not enemies:
        target_enemy = None
        return
    
    if not target_enemy or target_enemy not in enemies:
        target_enemy = find_nearest_enemy()
    
    if target_enemy:
        dx = target_enemy[0] - player_x
        dz = target_enemy[2] - player_z
        target_angle = math.degrees(math.atan2(dx, dz))
        
        angle_diff = (target_angle - player_angle) % 360
        if angle_diff > 180:
            angle_diff -= 360
        
        if abs(angle_diff) > 5:
            player_angle += angle_diff * 0.1
        
        current_time = time.time()
        if current_time - last_auto_fire_time >= auto_fire_cooldown:
            bullet_x = player_x + math.sin(math.radians(player_angle)) * 1.5
            bullet_y = player_y + 0.5
            bullet_z = player_z + math.cos(math.radians(player_angle)) * 1.5
            bullets.append([bullet_x, bullet_y, bullet_z, player_angle])
            last_auto_fire_time = current_time

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
