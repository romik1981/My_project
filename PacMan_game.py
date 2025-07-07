import pygame
import random
import sys
import math
import time

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PACMAN_SPEED = 5
ENEMY_SPEED = 3
ENEMY_LIFETIME = 5000  # 5 секунд

# Цвета
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac_Man")

# Фон
background = pygame.Surface(screen.get_size())
background.fill(BLUE)

# Класс для Pac-Man
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.mouth_open = False
        self.angle = 0  # Угол для анимации рта
        self.ang_open = 270 # Угол открытия рта
        self._ = 0 # счётчик проходов

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ограничение движения по краям экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Анимация рта только во время движения
        if self.speed_x != 0 or self.speed_y != 0:
            self.angle += 3  # Изменение угла для анимации
            self.draw_pacman()
        else:
            self.image.fill((0, 0, 0, 0))  # Очистка изображения
            pygame.draw.circle(self.image, YELLOW, (15, 15), 15)  # Полный круг без рта

    def change_angle(self):
        if self.ang_open < 360 and self._ != 30:
            # time.sleep(0.5)
            self.ang_open += 3
            self._ += 1
        elif self._ == 30 and self.ang_open > 270:
            self.ang_open -= 3
        else:
            self.ang_open = 270
            self._ = 0
        return self.ang_open

    def draw_pacman(self):
        self.image.fill((0, 0, 0, 0))  # Очистка изображения
        radius = 15
        center = (15, 15)
        start_angle = math.radians(self.angle)
        end_angle = math.radians(self.angle + self.change_angle())
        pygame.draw.circle(self.image, WHITE, center, radius)
        pygame.draw.arc(self.image, YELLOW, (0, 0, 30, 30), start_angle, end_angle, radius)

# Класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.speed_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.birth_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Изменение направления движения через 5 секунд
        if pygame.time.get_ticks() - self.birth_time > ENEMY_LIFETIME:
            self.speed_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
            self.speed_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
            self.birth_time = pygame.time.get_ticks()

        # Отражение от краев экрана
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Создание Pac-Man
pacman = Pacman()
all_sprites.add(pacman)

# Создание врагов
for _ in range(4):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Основной цикл игры
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.speed_x = -PACMAN_SPEED
                pacman.speed_y = 0
            elif event.key == pygame.K_RIGHT:
                pacman.speed_x = PACMAN_SPEED
                pacman.speed_y = 0
            elif event.key == pygame.K_UP:
                pacman.speed_y = -PACMAN_SPEED
                pacman.speed_x = 0
            elif event.key == pygame.K_DOWN:
                pacman.speed_y = PACMAN_SPEED
                pacman.speed_x = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pacman.speed_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                pacman.speed_y = 0

    # Обновление спрайтов
    all_sprites.update()

    # Проверка столкновений
    collisions = pygame.sprite.spritecollide(pacman, enemies, True)
    if not enemies:
        # Создание новых врагов
        for _ in range(4):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Отрисовка
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

pygame.quit()
sys.exit()
