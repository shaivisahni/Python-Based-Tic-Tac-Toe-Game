# import libraries
import pygame
import sys
import random
import time

# initialize pygame
pygame.init()

# set screen and box size
screen_Width, screen_Height = 600, 600
square_Size = screen_Width / 3

# create game screen
screen = pygame.display.set_mode((screen_Width, screen_Height))
pygame.display.set_caption("Tic Tac Toe")

# set fonts (larger size for bold marks)
large_font = pygame.font.SysFont("Comic Sans MS", 100)
small_font = pygame.font.SysFont("Comic Sans MS", 30)

# define theme dictionaries using Canadian spelling
themes = [
    {
        "name": "Light",
        "background": (250, 250, 250),
        "text": (0, 0, 0),
        "lines": (75, 75, 75),
        "x": (0, 0, 255),
        "o": (255, 0, 0)
    },
    {
        "name": "Dark",
        "background": (20, 20, 20),
        "text": (250, 250, 250),
        "lines": (180, 180, 180),
        "x": (255, 100, 100),
        "o": (100, 150, 255)
    },
    {
        "name": "Sunset",
        "background": (255, 204, 128),
        "text": (80, 0, 0),
        "lines": (255, 140, 105),
        "x": (255, 94, 98),
        "o": (255, 180, 0)
    },
    {
        "name": "Ombré",
        "background": (0, 64, 128),
        "text": (255, 255, 255),
        "lines": (0, 128, 128),
        "x": (0, 255, 200),
        "o": (0, 255, 100)
    }
]

current_theme_index = 0
current_theme = themes[current_theme_index]

# game variables
rows, cols = 3, 3
board = [[None for _ in range(cols)] for _ in range(rows)]
current_player = 'X'
game_over = False
winner = None
one_player = False  # default to two-player

def draw_board():
    screen.fill(current_theme["background"])
    for i in range(1, rows):
        pygame.draw.line(screen, current_theme["lines"], (0, i * square_Size), (screen_Width, i * square_Size), 4)
        pygame.draw.line(screen, current_theme["lines"], (i * square_Size, 0), (i * square_Size, screen_Height), 4)

    for row in range(rows):
        for col in range(cols):
            mark = board[row][col]
            if mark:
                colour = current_theme["x"] if mark == 'X' else current_theme["o"]
                text_surface = large_font.render(mark, True, colour)
                rect = text_surface.get_rect(center=(col * square_Size + square_Size // 2, row * square_Size + square_Size // 2))
                screen.blit(text_surface, rect)

def check_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(cols):
        if all(board[row][col] == player for row in range(rows)):
            return True
    if all(board[i][i] == player for i in range(rows)):
        return True
    if all(board[i][cols - 1 - i] == player for i in range(rows)):
        return True
    return False

def is_draw():
    return all(cell is not None for row in board for cell in row)

def draw_result():
    if winner:
        message = f"{winner} wins!"
    else:
        message = "It's a draw!"
    result = small_font.render(message, True, current_theme["text"])
    rect = result.get_rect(center=(screen_Width // 2, screen_Height - 30))
    screen.blit(result, rect)

def reset_game():
    global board, current_player, game_over, winner
    board = [[None for _ in range(cols)] for _ in range(rows)]
    current_player = 'X'
    game_over = False
    winner = None

def ai_move():
    empty_cells = [(r, c) for r in range(rows) for c in range(cols) if board[r][c] is None]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'

clock = pygame.time.Clock()
running = True

while running:
    draw_board()
    if game_over:
        draw_result()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = event.pos
            row = int(mouse_y // square_Size)
            col = int(mouse_x // square_Size)

            if board[row][col] is None:
                board[row][col] = current_player
                if check_winner(current_player):
                    game_over = True
                    winner = current_player
                elif is_draw():
                    game_over = True
                else:
                    current_player = 'O' if current_player == 'X' else 'X'

                    if one_player and not game_over:
                        time.sleep(0.4)  # delay before AI moves
                        ai_move()
                        if check_winner('O'):
                            game_over = True
                            winner = 'O'
                        elif is_draw():
                            game_over = True
                        else:
                            current_player = 'X'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_t:
                current_theme_index = (current_theme_index + 1) % len(themes)
                current_theme = themes[current_theme_index]
            if event.key == pygame.K_1:
                one_player = True
                reset_game()
            if event.key == pygame.K_2:
                one_player = False
                reset_game()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
