import pygame
import math
import sys

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

pygame.init()

# constantes
WIN_SIZE = 480
TILE_SIZE = WIN_SIZE / len(MAP)
PLAYER_SIZE = 6
PLAYER_SPEED = 5
RAY_NUMBER = 240
WALL_SIZE = WIN_SIZE / TILE_SIZE
DEPTH = WIN_SIZE
FOV = math.pi / 3
STEP_ANGLE = FOV / RAY_NUMBER
DISTANCE_ECRAN = (WIN_SIZE / 2) / math.tan(FOV / 2)
WALL_HEIGHT = TILE_SIZE
SCALE = WIN_SIZE / RAY_NUMBER

# global variables
player_x = WIN_SIZE / 2
player_y = WIN_SIZE / 2
player_rot = math.pi / 2

# initialisation de la fenetre
window = pygame.display.set_mode((WIN_SIZE * 2, WIN_SIZE))
pygame.display.set_caption("raycasting")

clock = pygame.time.Clock()


def draw_map():
    for row in range(len(MAP)):
        for col in range(len(MAP[row])):
            pygame.draw.rect(window, (200, 200, 200) if MAP[row][col] == 1 else (100, 100, 100),
                             (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))


def draw_player():
    pygame.draw.circle(window, (255, 0, 0), (player_x, player_y), PLAYER_SIZE)
    pygame.draw.line(window, (0, 255, 0), (player_x, player_y),
                     (player_x + math.sin(player_rot) * 100, player_y + math.cos(player_rot) * 100))

    # FOV
    pygame.draw.line(window, (0, 0, 255), (player_x, player_y),
                     (player_x + math.sin(player_rot + FOV / 2) * 100, player_y + math.cos(player_rot + FOV / 2) * 100))
    pygame.draw.line(window, (0, 0, 255), (player_x, player_y),
                     (player_x + math.sin(player_rot - FOV / 2) * 100, player_y + math.cos(player_rot - FOV / 2) * 100))


def raycasting():
    start_angle = player_rot + FOV / 2
    for ray in range(RAY_NUMBER):
        for pixel in range(DEPTH):
            target_x = player_x + math.sin(start_angle - STEP_ANGLE * ray) * pixel
            target_y = player_y + math.cos(start_angle - STEP_ANGLE * ray) * pixel
            row = int(target_y / TILE_SIZE)
            col = int(target_x / TILE_SIZE)
            if MAP[row][col] == 1:
                pygame.draw.line(window, (255, 255, 0), (player_x, player_y),
                                 (int(target_x), int(target_y)))
                pygame.draw.rect(window, (0, 255, 0),
                                 (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
                # draw 3D rendering
                color = 255 / (1 + pixel ** 2 * 0.0001)

                projected_wall_height = (WALL_HEIGHT / (int(pixel) + 0.001)) * DISTANCE_ECRAN
                projected_wall_height /= abs(math.cos((start_angle - STEP_ANGLE * ray) - player_rot))
                pygame.draw.rect(window, (color, color, color),
                                 (WIN_SIZE + ray * SCALE, WIN_SIZE / 2 - projected_wall_height / 2,
                                  SCALE, projected_wall_height))

                break


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # clear background
    pygame.draw.rect(window, (0, 0, 0), (0, 0, WIN_SIZE, WIN_SIZE))
    pygame.draw.rect(window, (0, 0, 0), (WIN_SIZE, 0, WIN_SIZE * 2, WIN_SIZE))

    # dessiner sol et le plafond
    pygame.draw.rect(window, (100, 100, 100), (WIN_SIZE, WIN_SIZE / 2, WIN_SIZE * 2, WIN_SIZE))
    pygame.draw.rect(window, (200, 200, 200), (WIN_SIZE, 0, WIN_SIZE * 2, WIN_SIZE / 2))

    draw_map()
    draw_player()
    raycasting()

    events = pygame.key.get_pressed()
    if events[pygame.K_LEFT]: player_rot += 0.15
    if events[pygame.K_RIGHT]: player_rot -= 0.15

    if events[pygame.K_UP]:
        tempo = MAP[int((player_y + math.cos(player_rot) * PLAYER_SPEED)/TILE_SIZE)]
        if tempo[int((player_x + math.sin(player_rot) * PLAYER_SPEED)/TILE_SIZE)] == 0:
            player_x += math.sin(player_rot) * PLAYER_SPEED
            player_y += math.cos(player_rot) * PLAYER_SPEED

    if events[pygame.K_DOWN]:
        tempo = MAP[int((player_y - math.cos(player_rot) * PLAYER_SPEED) / TILE_SIZE)]
        if tempo[int((player_x - math.sin(player_rot) * PLAYER_SPEED) / TILE_SIZE)] == 0:
            player_x -= math.sin(player_rot) * PLAYER_SPEED
            player_y -= math.cos(player_rot) * PLAYER_SPEED

    pygame.display.flip()
    clock.tick(30)
