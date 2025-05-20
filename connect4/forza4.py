import numpy as np
import math
import pygame
import sys

FULL_COLUMN = 6
COLUMN = 7
ROW = 6
SQUARE_SIZE = 100
CIRCLE_RADIUS = SQUARE_SIZE // 2 - 5
WIDTH = COLUMN * SQUARE_SIZE
HEIGHT = (ROW + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
PLAYER1 = 1
PLAYER2 = 2

WINNER = False
TURN = 0

pygame.init()
FONT = pygame.font.SysFont("monospace", 75)
screen = pygame.display.set_mode(SIZE)

def init_board():
    return np.zeros((ROW, COLUMN))

def validation_row(board, col_selected):
    for r in range(ROW):
        if board[r][col_selected] == 0:
            return r
    return FULL_COLUMN

def place_piece(board, col_selected, row, player):
    board[row][col_selected] = player

def validation_move(board, col_selected, player):
    row = validation_row(board, col_selected)
    if row != FULL_COLUMN:
        place_piece(board, col_selected, row, player)
        return True
    return False

def validation_winning(board, player):

    for c in range(COLUMN - 3):
        for r in range(ROW):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    for c in range(COLUMN):
        for r in range(ROW - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    for c in range(COLUMN - 3):
        for r in range(ROW - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    for c in range(COLUMN - 3):
        for r in range(3, ROW):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def validation_tie(board):
    return not np.any(board == 0)

def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                               int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                               CIRCLE_RADIUS)
    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == PLAYER1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                 HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   CIRCLE_RADIUS)
            elif board[r][c] == PLAYER2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                    HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   CIRCLE_RADIUS)
    pygame.display.update()

def player_turn(col_selected, board, player):
    global WINNER
    if validation_move(board, col_selected, player):
        if validation_winning(board, player):
            label = FONT.render(f"Player {player} wins!", True, GREEN)
            screen.blit(label, (40, 10))
            pygame.display.update()
            WINNER = True
        elif validation_tie(board):
            label = FONT.render("Tie game!", True, GREEN)
            screen.blit(label, (40, 10))
            pygame.display.update()
            WINNER = True

# Main
board = init_board()
draw_board(board)

while not WINNER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            pos_x = event.pos[0]
            color = RED if TURN % 2 == 0 else YELLOW
            pygame.draw.circle(screen, color, (pos_x, int(SQUARE_SIZE / 2)), CIRCLE_RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            pos_x = event.pos[0]
            col_selected = int(math.floor(pos_x / SQUARE_SIZE))
            player = PLAYER1 if TURN % 2 == 0 else PLAYER2
            player_turn(col_selected, board, player)
            TURN += 1
            draw_board(board)

if WINNER:
    pygame.time.wait(3000)
    pygame.quit()
