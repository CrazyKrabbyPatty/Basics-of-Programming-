import pygame
import random
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.SysFont("Arial", 36)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Цвета
BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Игровое поле
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def spawn_tile():
    empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if not empty:
        return
    r, c = random.choice(empty)
    board[r][c] = 2 if random.random() < 0.9 else 4

def draw_board():
    SCREEN.fill(BG_COLOR)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = board[r][c]
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, TILE_COLORS.get(val, (60, 58, 50)), rect)
            if val:
                text = FONT.render(str(val), True, (0, 0, 0) if val < 8 else (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                SCREEN.blit(text, text_rect)
    pygame.display.flip()

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def merge(row):
    for i in range(GRID_SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left():
    changed = False
    for r in range(GRID_SIZE):
        original = list(board[r])
        row = compress(board[r])
        row = merge(row)
        row = compress(row)
        board[r] = row
        if row != original:
            changed = True
    return changed

def move_right():
    for r in range(GRID_SIZE):
        board[r].reverse()
    changed = move_left()
    for r in range(GRID_SIZE):
        board[r].reverse()
    return changed

def transpose():
    global board
    board = [list(row) for row in zip(*board)]

def move_up():
    transpose()
    changed = move_left()
    transpose()
    return changed

def move_down():
    transpose()
    changed = move_right()
    transpose()
    return changed

def can_move():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return True
            if c < GRID_SIZE - 1 and board[r][c] == board[r][c + 1]:
                return True
            if r < GRID_SIZE - 1 and board[r][c] == board[r + 1][c]:
                return True
    return False

# Начальные плитки
spawn_tile()
spawn_tile()

# Главный цикл
clock = pygame.time.Clock()
while True:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            moved = False
            if event.key == pygame.K_LEFT:
                moved = move_left()
            elif event.key == pygame.K_RIGHT:
                moved = move_right()
            elif event.key == pygame.K_UP:
                moved = move_up()
            elif event.key == pygame.K_DOWN:
                moved = move_down()
            if moved:
                spawn_tile()
            if not can_move():
                print("Game Over")
                pygame.quit()
                sys.exit()
    clock.tick(60)
