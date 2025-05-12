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


def auto_move_to_enemy():
    global player_x, player_z, move_forward
    
    if not target_enemy:
        return
    
    dx = target_enemy[0] - player_x
    dz = target_enemy[2] - player_z
    distance = math.sqrt(dx * dx + dz * dz)
    
    if distance > 5:
        move_forward = True
    else:
        move_forward = False

def draw_fence(x, z, length, rotation=0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)
    
    post_spacing = 5.0
    num_posts = int(length / post_spacing) + 1
    
    for i in range(num_posts):
        glColor3f(0.4, 0.2, 0.1)
        glPushMatrix()
        glTranslatef(i * post_spacing, 1, 0)
        glScalef(0.2, 2, 0.2)
        glutSolidCube(1.0)
        glPopMatrix()
        
        if i < num_posts - 1:
            glColor3f(0.5, 0.3, 0.2)
            glPushMatrix()
            glTranslatef(i * post_spacing + post_spacing/2, 1.8, 0)
            glScalef(post_spacing, 0.1, 0.1)
            glutSolidCube(1.0)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(i * post_spacing + post_spacing/2, 1.0, 0)
            glScalef(post_spacing, 0.1, 0.1)
            glutSolidCube(1.0)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(i * post_spacing + post_spacing/2, 0.2, 0)
            glScalef(post_spacing, 0.1, 0.1)
            glutSolidCube(1.0)
            glPopMatrix()
    glPopMatrix()

def draw_boundaries():
    fence_length = world_size * 2
    draw_fence(-world_size, -world_size, fence_length, 0)
    draw_fence(-world_size, world_size, fence_length, 0)
    draw_fence(world_size, -world_size, fence_length, 90)
    draw_fence(-world_size, -world_size, fence_length, 90)

def draw_enemy_bullet(x, y, z, direction):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(direction, 0, 1, 0)
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    glScalef(0.2, 0.2, 0.4)
    glutSolidCube(1.0)
    glPopMatrix()
    glColor3f(1.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(0, 0.5, 0.3)
    glScalef(0.1, 0.1, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()
    
    glPopMatrix()

def update_enemy_positions():
    global enemies, enemy_bullets, last_enemy_shot_time
    current_time = time.time()
    if current_level == 3:
        enemy_speed = 0.4
    else:
        enemy_speed = 0.2
    for i, enemy in enumerate(enemies):
        x, y, z, angle = enemy
        dx = player_x - x
        dz = player_z - z
        distance = math.sqrt(dx * dx + dz * dz)
        target_angle = math.degrees(math.atan2(dx, dz))
        angle_diff = (target_angle - angle) % 360
        if angle_diff > 180:
            angle_diff -= 360
        new_angle = angle + angle_diff * 0.1
        if distance > 2.0:
            new_x = x + math.sin(math.radians(new_angle)) * enemy_speed
            new_z = z + math.cos(math.radians(new_angle)) * enemy_speed
            if not check_boundary_collision(new_x, new_z):
                x = new_x
                z = new_z
        enemies[i] = (x, y, z, new_angle)
        if current_time - last_enemy_shot_time.get(i, 0) >= enemy_shoot_cooldown:
            if distance < 20.0:
                angle_to_player = abs(angle_diff)
                if angle_to_player < 30.0:
                    bullet_x = x + math.sin(math.radians(new_angle)) * 1.5
                    bullet_z = z + math.cos(math.radians(new_angle)) * 1.5
                    enemy_bullets.append((bullet_x, 1.0, bullet_z, new_angle))
                    last_enemy_shot_time[i] = current_time

def update_game():
    global player_x, player_z, player_angle, player_health, player_score
    global enemies, bullets, enemy_bullets, explosions, missed_shots, game_over
    global leg_angle, leg_direction, last_auto_shot_time, scan_angle, normal_speed, cheat_speed, speed_boost
    global move_forward, move_backward, move_left, move_right
    global current_level, winner
    global boss_active, boss_x, boss_y, boss_z, boss_health, boss_max_health, boss_missile_timer, boss_missile_cooldown, boss_missiles
    if game_over or winner or is_paused:
        return
    if player_score <= 50:
        current_level = 1
        boss_active = False
    elif player_score <= 150:
        current_level = 2
        boss_active = False
    elif player_score <= 300:
        current_level = 3
        if not boss_active:
            boss_active = True
            boss_health = boss_max_health
            boss_x = 0.0
            boss_y = 0.0
            boss_z = 60.0
            boss_missile_timer = time.time()
            boss_missiles = []
            enemies.clear()
    else:
        winner = True
        boss_active = False
        return
    auto_avoid = False
    if cheat_mode:
        if boss_active:
            dx = boss_x - player_x
            dz = boss_z - player_z
            target_angle = math.degrees(math.atan2(dx, dz))
            player_angle = target_angle
            current_time = time.time()
            if current_time - last_auto_shot_time >= auto_shot_cooldown:
                bullet_x = player_x + math.sin(math.radians(target_angle)) * 1.5
                bullet_z = player_z + math.cos(math.radians(target_angle)) * 1.5
                bullets.append((bullet_x, 1.0, bullet_z, target_angle))
                last_auto_shot_time = current_time
            boss_dist = math.sqrt(dx*dx + dz*dz)
            if boss_dist < 8.0:
                auto_avoid = True
        else:
            nearest_enemy = None
            min_distance = float('inf')
            for enemy in enemies:
                dx = enemy[0] - player_x
                dz = enemy[2] - player_z
                distance = math.sqrt(dx * dx + dz * dz)
                if distance < min_distance:
                    min_distance = distance
                    nearest_enemy = enemy
            if nearest_enemy:
                dx = nearest_enemy[0] - player_x
                dz = nearest_enemy[2] - player_z
                target_angle = math.degrees(math.atan2(dx, dz))
                player_angle = target_angle
                current_time = time.time()
                if current_time - last_auto_shot_time >= auto_shot_cooldown:
                    bullet_x = player_x + math.sin(math.radians(target_angle)) * 1.5
                    bullet_z = player_z + math.cos(math.radians(target_angle)) * 1.5
                    bullets.append((bullet_x, 1.0, bullet_z, target_angle))
                    last_auto_shot_time = current_time
                if min_distance < 4.0:
                    auto_avoid = True
    current_speed = (cheat_speed if cheat_mode else normal_speed) * (2.0 if speed_boost else 1.0)
    new_x = player_x
    new_z = player_z

    if move_forward:
        new_x += math.sin(math.radians(player_angle)) * current_speed
        new_z += math.cos(math.radians(player_angle)) * current_speed
    if move_backward:
        new_x -= math.sin(math.radians(player_angle)) * current_speed
        new_z -= math.cos(math.radians(player_angle)) * current_speed
    if move_left:
        new_x -= math.sin(math.radians(player_angle - 90)) * current_speed
        new_z -= math.cos(math.radians(player_angle - 90)) * current_speed
    if move_right:
        new_x -= math.sin(math.radians(player_angle + 90)) * current_speed
        new_z -= math.cos(math.radians(player_angle + 90)) * current_speed
    if cheat_mode and auto_avoid:
        new_x -= math.sin(math.radians(player_angle)) * current_speed
        new_z -= math.cos(math.radians(player_angle)) * current_speed

    if not check_boundary_collision(new_x, new_z):
        player_x = new_x
        player_z = new_z
    if move_forward or move_backward or (cheat_mode and auto_avoid):
        leg_angle += leg_speed * leg_direction
        if abs(leg_angle) > 30:
            leg_direction *= -1
    else:
        leg_angle = 0
    new_bullets = []
    for bullet in bullets:
        x, y, z, direction = bullet
        new_x = x + math.sin(math.radians(direction)) * bullet_speed
        new_z = z + math.cos(math.radians(direction)) * bullet_speed
        if not check_boundary_collision(new_x, new_z):
            new_bullets.append((new_x, y, new_z, direction))
        else:
            missed_shots += 1
    bullets = new_bullets
    new_enemy_bullets = []
    for bullet in enemy_bullets:
        x, y, z, direction = bullet
        new_x = x + math.sin(math.radians(direction)) * enemy_bullet_speed
        new_z = z + math.cos(math.radians(direction)) * enemy_bullet_speed
        if not check_boundary_collision(new_x, new_z):
            new_enemy_bullets.append((new_x, y, new_z, direction))
    enemy_bullets = new_enemy_bullets

    #BOSS(Level 3)
    if boss_active:
        dx = player_x - boss_x
        dz = player_z - boss_z
        dist = math.sqrt(dx*dx + dz*dz)
        if dist > 6.0:
            boss_speed = 0.04
            boss_x += (dx/dist) * boss_speed
            boss_z += (dz/dist) * boss_speed
        now = time.time()
        if now - boss_missile_timer > boss_missile_cooldown:
            dx = player_x - boss_x
            dz = player_z - boss_z
            missile_angle = math.degrees(math.atan2(dx, dz))
            missile_x = boss_x + math.sin(math.radians(missile_angle)) * 4.0
            missile_z = boss_z + math.cos(math.radians(missile_angle)) * 4.0
            boss_missiles.append([missile_x, 4.0, missile_z, missile_angle])
            boss_missile_timer = now

        new_boss_missiles = []
        for m in boss_missiles:
            mx, my, mz, mdir = m
            mx += math.sin(math.radians(mdir)) * 0.7
            mz += math.cos(math.radians(mdir)) * 0.7
            if check_collision(mx, mz, player_x, player_z, 1.2):
                if not cheat_mode and not shield_on:
                    player_health -= 20
                    if player_health <= 0:
                        game_over = True
                explosions.append((mx, my, mz, 0.7))
            elif not check_boundary_collision(mx, mz):
                new_boss_missiles.append([mx, my, mz, mdir])
        boss_missiles = new_boss_missiles
        for bullet in bullets[:]:
            if check_collision(bullet[0], bullet[2], boss_x, boss_z, 4.0):
                boss_health -= 10
                if boss_health < 0:
                    boss_health = 0
                explosions.append((bullet[0], bullet[1], bullet[2], 0.7))
                bullets.remove(bullet)
                if boss_health <= 0:
                    boss_active = False
                    winner = True
        return 

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet[0], bullet[2], enemy[0], enemy[2], 1.0):
                player_score += 1
                enemies.remove(enemy)
                bullets.remove(bullet)
                explosions.append((enemy[0], enemy[1], enemy[2], 1.0))
                break

    for bullet in enemy_bullets[:]:
        if check_collision(bullet[0], bullet[2], player_x, player_z, 1.0):
            enemy_bullets.remove(bullet)
            if not cheat_mode and not shield_on:
                player_health -= 10
                if player_health <= 0:
                    game_over = True
            explosions.append((bullet[0], bullet[1], bullet[2], 0.5))

    new_explosions = []
    for explosion in explosions:
        x, y, z, size = explosion
        if size < 2.0:
            new_explosions.append((x, y, z, size + 0.1))
    explosions = new_explosions

    if len(enemies) < 20 and not boss_active:
        spawn_enemies(1)

    if not boss_active:
        update_enemy_positions()

    glutPostRedisplay()

def setup_camera():
    global camera_angle, camera_height, camera_distance
    global target_camera_angle, target_camera_height, target_camera_distance, player_angle, player_x, player_y, player_z, first_person

    # Make camera angle match player angle
    camera_angle = player_angle
    target_camera_angle = player_angle
    
    camera_height += (target_camera_height - camera_height) * camera_smoothness
    camera_distance += (target_camera_distance - camera_distance) * camera_smoothness

    if first_person:
        cam_x = player_x + math.sin(math.radians(player_angle)) * 0.5 
        cam_y = player_y + 1.0
        cam_z = player_z + math.cos(math.radians(player_angle)) * 0.5
        look_x = player_x + math.sin(math.radians(player_angle)) * 2.0
        look_y = player_y + 1.0
        look_z = player_z + math.cos(math.radians(player_angle)) * 2.0
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0)
    else:
        cam_x = player_x - math.sin(math.radians(camera_angle)) * camera_distance
        cam_y = player_y + camera_height 
        cam_z = player_z - math.cos(math.radians(camera_angle)) * camera_distance
        gluLookAt(cam_x, cam_y, cam_z, player_x, player_y + 0.5, player_z, 0, 1, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_camera()
    draw_ground()
    
    for tree in trees:
        x, z, scale, color_var = tree
        draw_tree(x, z, scale)
    draw_player()
    if shield_on:
        draw_shield(player_x, player_y, player_z)
    if boss_active:
        draw_boss_alien(boss_x, boss_y, boss_z)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        bar_width = 400
        bar_height = 20
        x0 = WINDOW_WIDTH/2 - bar_width/2
        y0 = 40
        health_ratio = boss_health / boss_max_health
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(x0, y0)
        glVertex2f(x0+bar_width, y0)
        glVertex2f(x0+bar_width, y0+bar_height)
        glVertex2f(x0, y0+bar_height)
        glEnd()
        glColor3f(0.1, 0.8, 0.1)
        glBegin(GL_QUADS)
        glVertex2f(x0, y0)
        glVertex2f(x0+bar_width*health_ratio, y0)
        glVertex2f(x0+bar_width*health_ratio, y0+bar_height)
        glVertex2f(x0, y0+bar_height)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(x0+bar_width/2-40, y0+bar_height-5)
        for char in "ALIEN BOSS":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        for m in boss_missiles:
            glPushMatrix()
            glTranslatef(m[0], m[1], m[2])
            glColor3f(1.0, 0.2, 0.2)
            glutSolidSphere(0.7, 12, 12)
            glColor3f(1.0, 0.7, 0.0)
            glutSolidSphere(0.4, 8, 8)
            glPopMatrix()
    else:
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1], enemy[2], enemy[3])
        for bullet in enemy_bullets:
            draw_enemy_bullet(bullet[0], bullet[1], bullet[2], bullet[3])
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2], bullet[3])
    for explosion in explosions:
        draw_explosion(explosion[0], explosion[1], explosion[2], explosion[3])
    draw_hud()
    draw_minimap()
    draw_play_pause_button(is_paused)
    draw_quit_button()
    if is_paused:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(WINDOW_WIDTH, 0)
        glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
        glVertex2f(0, WINDOW_HEIGHT)
        glEnd()
        glDisable(GL_BLEND)
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(WINDOW_WIDTH/2 - 40, WINDOW_HEIGHT/2)
        for char in "PAUSED":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
        glRasterPos2f(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 30)
        continue_text = "Press SPACE to continue"
        for char in continue_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    glutSwapBuffers()

def reshape(w, h):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH = w
    WINDOW_HEIGHT = h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(w)/float(h), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global move_forward, move_backward, move_left, move_right
    global player_x, player_z, player_angle, player_health, player_score
    global enemies, bullets, enemy_bullets, explosions, missed_shots, game_over
    global cheat_mode, speed_boost, scan_angle, shield_on, is_paused

    if key == b' ':
        is_paused = not is_paused
        if is_paused:
            glutSetCursor(GLUT_CURSOR_INHERIT)  # Show cursor when paused
            print("Game Paused")
        else:
            glutSetCursor(GLUT_CURSOR_NONE)  # Hide cursor when resuming
            print("Game Resumed")
        return
    elif key == b'\x1b':  # ESC key
        is_paused = True
        glutSetCursor(GLUT_CURSOR_INHERIT)  # Show cursor when paused
        print("Game Paused")
        return
    elif key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        if cheat_mode:
            player_health = 100
            enemy_bullets = []
            nearest_enemy = None
            min_distance = float('inf')
            for enemy in enemies:
                dx = enemy[0] - player_x
                dz = enemy[2] - player_z
                distance = math.sqrt(dx*dx + dz*dz)
                if distance < min_distance:
                    min_distance = distance
                    nearest_enemy = enemy
            if nearest_enemy:
                dx = nearest_enemy[0] - player_x
                dz = nearest_enemy[2] - player_z
                player_angle = math.degrees(math.atan2(dx, dz))
    elif not is_paused:
        if key == b'w':
            move_forward = True
        elif key == b's':
            move_backward = True
        elif key == b'a':
            move_left = True
        elif key == b'd':
            move_right = True
        elif key == b'b':
            speed_boost = True
        elif key == b'r':
            player_x = 0
            player_z = 0
            player_angle = 0
            scan_angle = 0
            player_health = 100
            player_score = 0
            missed_shots = 0
            game_over = False
            enemies = []
            bullets = []
            enemy_bullets = []
            explosions = []
            spawn_enemies(15)
        elif key == b'q':
            glutLeaveMainLoop()
        elif key == b'i' or key == b'I':
            if not is_paused:
                shield_on = not shield_on

def keyboard_up(key, x, y):
    global move_forward, move_backward, move_left, move_right, speed_boost
    if key == b'w':
        move_forward = False
    elif key == b's':
        move_backward = False
    elif key == b'a':
        move_left = False
    elif key == b'd':
        move_right = False
    elif key == b'b': 
        speed_boost = False

def mouse(button, state, x, y):
    global bullets, first_person, is_paused, WINDOW_WIDTH, WINDOW_HEIGHT
    global player_x, player_z, player_angle, scan_angle, player_health, player_score, missed_shots, game_over, enemies, bullets, enemy_bullets, explosions
    ogl_x = x
    ogl_y = y
    btn_x = WINDOW_WIDTH - 60
    btn_y = 40
    btn_size = 30
    quit_x = WINDOW_WIDTH - 60 - 40
    quit_y = 40
    quit_size = 30

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        dist = math.sqrt((ogl_x - btn_x)**2 + (ogl_y - btn_y)**2)
        if dist <= btn_size/2:
            is_paused = not is_paused
            if is_paused:
                print("Game Paused")
            else:
                print("Game Resumed")
            return
        dist_quit = math.sqrt((ogl_x - quit_x)**2 + (ogl_y - quit_y)**2)
        if dist_quit <= quit_size/2:
            glutLeaveMainLoop()
            return

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullet_x = player_x + math.sin(math.radians(player_angle)) * 1.5
        bullet_y = player_y + 0.5
        bullet_z = player_z + math.cos(math.radians(player_angle)) * 1.5
        bullets.append([bullet_x, bullet_y, bullet_z, player_angle])

def special_input(key, x, y):
    global target_camera_distance, target_camera_height, target_camera_angle
    if key == GLUT_KEY_LEFT:
        target_camera_angle -= 10
    elif key == GLUT_KEY_RIGHT:
        target_camera_angle += 10 
    elif key == GLUT_KEY_UP:
        target_camera_distance = max(5.0, target_camera_distance - 1.0) 
    elif key == GLUT_KEY_DOWN:
        target_camera_distance = min(40.0, target_camera_distance + 1.0) 
    elif key == GLUT_KEY_PAGE_UP:
        target_camera_height = min(20.0, target_camera_height + 0.5)
    elif key == GLUT_KEY_PAGE_DOWN:
        target_camera_height = max(2.0, target_camera_height - 0.5)

def update(value):
    update_game()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def check_boundary_collision(x, z):
    buffer = 30.0  # Buffer zone
    return (abs(x) > world_size - buffer or abs(z) > world_size - buffer)

def check_collision(x1, z1, x2, z2, radius):
    dx = x1 - x2
    dz = z1 - z2
    distance = math.sqrt(dx * dx + dz * dz)
    return distance < radius

def draw_shield(x, y, z, radius=1.2):
    glPushMatrix()
    glTranslatef(x, y+1.0, z)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.4, 0.7, 1.0, 0.25)
    glutSolidSphere(radius, 32, 32)
    glDisable(GL_BLEND)
    glPopMatrix()

def draw_boss_alien(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(4.0, 4.0, 4.0) 
    # body (green)
    glColor3f(0.1, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glScalef(2.0, 3.0, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()
    # belly (yellow)
    glColor3f(0.8, 0.9, 0.2)
    glPushMatrix()
    glTranslatef(0, 2.5, 0.51)
    glScalef(1.0, 2.0, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()
    # head (green)
    glColor3f(0.1, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(0.7, 4.2, 0)
    glScalef(1.5, 1.2, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()
    # eye (white)
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(1.2, 4.5, 0.4)
    glScalef(0.2, 0.2, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()
    # pupil (black)
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(1.22, 4.5, 0.45)
    glScalef(0.08, 0.08, 0.08)
    glutSolidCube(1.0)
    glPopMatrix()
    # mouth (black)
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(1.1, 4.0, 0.5)
    glScalef(0.5, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()
    # Boss description
    # teeth (white)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(3):
        glPushMatrix()
        glTranslatef(1.0 + 0.1*i, 3.95, 0.55)
        glScalef(0.05, 0.05, 0.05)
        glutSolidCube(1.0)
        glPopMatrix()
    # arms (green)
    glColor3f(0.1, 0.7, 0.1)
    for sign in [-1, 1]:
        glPushMatrix()
        glTranslatef(sign*1.2, 3.2, 0)
        glRotatef(sign*30, 0, 0, 1)
        glScalef(0.3, 1.2, 0.3)
        glutSolidCube(1.0)
        glPopMatrix()
    # Claws (gray)
    glColor3f(0.7, 0.7, 0.7)
    for sign in [-1, 1]:
        for i in range(3):
            glPushMatrix()
            glTranslatef(sign*1.2 + sign*0.1*i, 2.5 - 0.1*i, 0.2)
            glScalef(0.08, 0.18, 0.08)
            glutSolidCube(1.0)
            glPopMatrix()
    # Legs (green)
    for sign in [-1, 1]:
        glPushMatrix()
        glTranslatef(sign*0.5, 0.7, 0)
        glScalef(0.4, 1.2, 0.4)
        glutSolidCube(1.0)
        glPopMatrix()
    # Feet (gray)
    glColor3f(0.7, 0.7, 0.7)
    for sign in [-1, 1]:
        glPushMatrix()
        glTranslatef(sign*0.5, 0.1, 0.2)
        glScalef(0.18, 0.08, 0.18)
        glutSolidCube(1.0)
        glPopMatrix()
    # Tail (green)
    glColor3f(0.1, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(-1.2, 1.2, 0)
    glRotatef(-30, 0, 0, 1)
    glScalef(1.2, 0.3, 0.3)
    glutSolidCube(1.0)
    glPopMatrix()
    # Spikes (purple)
    glColor3f(0.5, 0.2, 0.7)
    for i in range(5):
        glPushMatrix()
        glTranslatef(-0.5 + 0.25*i, 3.5 + 0.2*i, 0.5)
        glScalef(0.08, 0.18, 0.08)
        glutSolidCube(1.0)
        glPopMatrix()
    glPopMatrix()

def draw_play_pause_button(is_paused):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    x = WINDOW_WIDTH - 60
    y = 40
    size = 30

    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1.0, 0.8, 0.0) 
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for angle in range(0, 361, 10):
        glVertex2f(x + size/2 * math.cos(math.radians(angle)), y + size/2 * math.sin(math.radians(angle)))
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    if is_paused:
        glBegin(GL_TRIANGLES)
        glVertex2f(x - size/6, y - size/4)
        glVertex2f(x - size/6, y + size/4)
        glVertex2f(x + size/4, y)
        glEnd()
    else:        
        bar_width = size/8
        bar_height = size/3
        glBegin(GL_QUADS)
        glVertex2f(x - bar_width*2, y - bar_height/2)
        glVertex2f(x - bar_width, y - bar_height/2)
        glVertex2f(x - bar_width, y + bar_height/2)
        glVertex2f(x - bar_width*2, y + bar_height/2)
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(x + bar_width, y - bar_height/2)
        glVertex2f(x + bar_width*2, y - bar_height/2)
        glVertex2f(x + bar_width*2, y + bar_height/2)
        glVertex2f(x + bar_width, y + bar_height/2)
        glEnd()
    
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x - 35, y + 25)
    label = "Play/Pause"
    for char in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def draw_quit_button():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    x = WINDOW_WIDTH - 60 - 40  
    y = 40
    size = 30

    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for angle in range(0, 361, 10):
        glVertex2f(x + size/2 * math.cos(math.radians(angle)), y + size/2 * math.sin(math.radians(angle)))
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    line_width = size/6
    glBegin(GL_QUADS)
    glVertex2f(x - line_width, y - line_width)
    glVertex2f(x + line_width, y + line_width)
    glVertex2f(x + line_width, y + line_width*2)
    glVertex2f(x - line_width, y - line_width*2)
    glEnd()
    
    glBegin(GL_QUADS)
    glVertex2f(x - line_width, y + line_width)
    glVertex2f(x + line_width, y - line_width)
    glVertex2f(x + line_width, y - line_width*2)
    glVertex2f(x - line_width, y + line_width*2)
    glEnd()


    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x - 15, y + 25)
    label = "Quit"
    for char in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def draw_minimap():
    global WINDOW_WIDTH, WINDOW_HEIGHT, player_x, player_z, player_angle, enemies, boss_active, boss_x, boss_z, power_ups, bullets, enemy_bullets
    map_size = 150 
    margin = 20     
    x = margin
    y = WINDOW_HEIGHT - map_size - margin
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.0, 0.0, 0.0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + map_size, y)
    glVertex2f(x + map_size, y + map_size)
    glVertex2f(x, y + map_size)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + map_size, y)
    glVertex2f(x + map_size, y + map_size)
    glVertex2f(x, y + map_size)
    glEnd()
    scale = map_size / (world_size * 2)
    center_x = x + map_size / 2
    center_y = y + map_size / 2
    glColor3f(0.0, 1.0, 0.0)
    for pu in power_ups:
        pu_x, pu_z = pu[0], pu[2]
        dx = pu_x - player_x
        dz = pu_z - player_z
        map_x = center_x + dx * scale
        map_y = center_y + dz * scale
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(map_x, map_y)
        for angle in range(0, 361, 10):
            glVertex2f(map_x + 2 * math.cos(math.radians(angle)),
                      map_y + 2 * math.sin(math.radians(angle)))
        glEnd()
    glColor3f(1.0, 1.0, 1.0)
    for b in bullets:
        b_x, b_z = b[0], b[2]
        dx = b_x - player_x
        dz = b_z - player_z
        map_x = center_x + dx * scale
        map_y = center_y + dz * scale
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(map_x, map_y)
        for angle in range(0, 361, 30):
            glVertex2f(map_x + 1.5 * math.cos(math.radians(angle)),
                      map_y + 1.5 * math.sin(math.radians(angle)))
        glEnd()

    glColor3f(1.0, 0.5, 0.0)
    for b in enemy_bullets:
        b_x, b_z = b[0], b[2]
        dx = b_x - player_x
        dz = b_z - player_z
        map_x = center_x + dx * scale
        map_y = center_y + dz * scale
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(map_x, map_y)
        for angle in range(0, 361, 30):
            glVertex2f(map_x + 1.5 * math.cos(math.radians(angle)),
                      map_y + 1.5 * math.sin(math.radians(angle)))
        glEnd()
    glColor3f(1.0, 0.0, 0.0)
    for enemy in enemies:
        enemy_x = enemy[0]
        enemy_z = enemy[2]
        dx = enemy_x - player_x
        dz = enemy_z - player_z
        map_x = center_x + dx * scale
        map_y = center_y + dz * scale
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(map_x, map_y)
        for angle in range(0, 361, 10):
            glVertex2f(map_x + 2 * math.cos(math.radians(angle)),
                      map_y + 2 * math.sin(math.radians(angle)))
        glEnd()

    if boss_active:
        glColor3f(1.0, 1.0, 0.0)
        dx = boss_x - player_x
        dz = boss_z - player_z
        map_x = center_x + dx * scale
        map_y = center_y + dz * scale
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(map_x, map_y)
        for angle in range(0, 361, 10):
            glVertex2f(map_x + 4 * math.cos(math.radians(angle)),
                      map_y + 4 * math.sin(math.radians(angle)))
        glEnd()
    
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(center_x, center_y)
    for angle in range(0, 361, 10):
        glVertex2f(center_x + 3 * math.cos(math.radians(angle)),
                  center_y + 3 * math.sin(math.radians(angle)))
    glEnd()

    glColor3f(0.0, 0.7, 1.0)
    arrow_length = 12
    angle_rad = math.radians(player_angle)
    arrow_x = center_x + arrow_length * math.sin(angle_rad)
    arrow_y = center_y + arrow_length * math.cos(angle_rad)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(center_x, center_y)
    glVertex2f(arrow_x, arrow_y)
    glEnd()
    glLineWidth(1)
    glColor3f(0.0, 0.7, 0.7)

    font = GLUT_BITMAP_HELVETICA_12
    compass = [('N', 0, -map_size/2 + 10), ('S', 0, map_size/2 - 15), ('E', map_size/2 - 15, 0), ('W', -map_size/2 + 5, 0)]
    for label, dx, dy in compass:
        glRasterPos2f(center_x + dx - 5, center_y + dy + 5)
        for ch in label:
            glutBitmapCharacter(font, ord(ch))

    glBegin(GL_LINES)
    glVertex2f(center_x - map_size/2, center_y)
    glVertex2f(center_x + map_size/2, center_y)
    glVertex2f(center_x, center_y - map_size/2)
    glVertex2f(center_x, center_y + map_size/2)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x + map_size/2 - 30, y - 5)
    label = "MINIMAP"
    for char in "MINIMAP":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    glDisable(GL_BLEND)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def mouse_motion(x, y):
    global player_angle, is_paused
    
    if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
        glutSetCursor(GLUT_CURSOR_INHERIT)
        return
    glutSetCursor(GLUT_CURSOR_NONE)

    center_x = WINDOW_WIDTH // 2
    
    rotation_speed = 0.5
    dx = x - center_x
    player_angle -= dx * rotation_speed

    player_angle %= 360

    glutWarpPointer(center_x, WINDOW_HEIGHT // 2)

def main():
    glutInit(sys.argv)
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_input)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutPassiveMotionFunc(mouse_motion) 
    glutTimerFunc(16, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main() 
