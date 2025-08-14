# level.py
import os
import pygame
from settings import WIDTH, HEIGHT, FPS

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
BG_PATH = os.path.join(ASSETS, "img", "level-1.png")
HERO_PATH = os.path.join(ASSETS, "img", "hero.png")

GROUND_Y = HEIGHT - 118
MOVE_VX = 6
JUMP_VY = -14
GRAVITY = 0.8

# размеры ячейки
FRAME_W = 150
FRAME_H = 220

def get_frame(sheet, row, col, scale=1.0):
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    frame = sheet.subsurface(rect)
    if scale != 1.0:
        frame = pygame.transform.smoothscale(
            frame, (int(FRAME_W * scale), int(FRAME_H * scale))
        )
    return frame

class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, scale=0.8):
        super().__init__()
        # Бег
        self.walk_left = [get_frame(sheet, 1, c, scale) for c in range(3)]
        self.walk_right = [pygame.transform.flip(img, True, False) for img in self.walk_left]
        self.idle_right = self.walk_right[0]
        self.idle_left = self.walk_left[0]
        # Удар
        self.attack_left = [get_frame(sheet, 5, c, scale) for c in range(8)]
        self.attack_right = [get_frame(sheet, 4, c, scale) for c in range(8)]

        self.image = self.idle_right
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, GROUND_Y))

        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.facing_right = True
        self.anim_timer = 0
        self.anim_idx = 0

        # Состояния
        self.attacking = False
        self.attack_frame = 0

    def input(self, keys):
        if not self.attacking:  # нельзя двигаться во время удара
            self.vx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vx = -MOVE_VX
                self.facing_right = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vx = MOVE_VX
                self.facing_right = True
            if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
                self.vy = JUMP_VY
                self.on_ground = False
        # Удар (Ctrl)
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if not self.attacking:
                self.attacking = True
                self.attack_frame = 0

    def physics(self):
        self.rect.x += self.vx
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.vy += GRAVITY
        self.rect.y += self.vy
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vy = 0
            self.on_ground = True

    def animate(self):
        if self.attacking:
            # проигрываем анимацию удара
            frames = self.attack_right if self.facing_right else self.attack_left
            self.image = frames[self.attack_frame]
            self.attack_frame += 1
            if self.attack_frame >= len(frames):
                self.attacking = False  # конец удара
        else:
            moving = self.vx != 0 and self.on_ground
            if moving:
                self.anim_timer = (self.anim_timer + 1) % 8
                if self.anim_timer == 0:
                    self.anim_idx = (self.anim_idx + 1) % len(self.walk_left)
                self.image = self.walk_right[self.anim_idx] if self.facing_right else self.walk_left[self.anim_idx]
            else:
                self.image = self.idle_right if self.facing_right else self.idle_left

    def update(self, keys):
        self.input(keys)
        self.physics()
        self.animate()

class Level:
    def __init__(self):
        self.bg = pygame.image.load(BG_PATH).convert()
        self.bg = pygame.transform.smoothscale(self.bg, (WIDTH, HEIGHT))
        sheet = pygame.image.load(HERO_PATH).convert_alpha()
        self.hero = Hero(sheet, scale=1.0)
        self.sprites = pygame.sprite.Group(self.hero)

    def update(self, keys):
        self.sprites.update(keys)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        self.sprites.draw(screen)
