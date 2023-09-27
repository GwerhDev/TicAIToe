import pygame
import random
import math

WIDTH = 600
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.Font(None, 60)

class TicTacToe:
    def __init__(self):
        self.board = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.humanPlayer = 'X'
            self.botPlayer = 'O'
        else:
            self.humanPlayer = 'O'
            self.botPlayer = 'X'
        self.currentPlayer = self.humanPlayer

    def draw_board(self):
        window.fill(BLACK)
        pygame.draw.line(window, WHITE, (WIDTH/3, 0), (WIDTH/3, HEIGHT), 5)
        pygame.draw.line(window, WHITE, (2*WIDTH/3, 0), (2*WIDTH/3, HEIGHT), 5)
        pygame.draw.line(window, WHITE, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 5)
        pygame.draw.line(window, WHITE, (0, 2*HEIGHT/3), (WIDTH, 2*HEIGHT/3), 5)

        for i in range(3):
            for j in range(3):
                if self.board[i*3 + j] == 'X':
                    text = font.render('X', True, WHITE)
                    window.blit(text, (j*WIDTH/3 + WIDTH/6 - text.get_width()/2, i*HEIGHT/3 + HEIGHT/6 - text.get_height()/2))
                elif self.board[i*3 + j] == 'O':
                    text = font.render('O', True, WHITE)
                    window.blit(text, (j*WIDTH/3 + WIDTH/6 - text.get_width()/2, i*HEIGHT/3 + HEIGHT/6 - text.get_height()/2))

    def is_board_filled(self):
        return not '-' in self.board

    def is_player_win(self, player):
        if self.board[0] == self.board[1] == self.board[2] == player:
            return True
        if self.board[3] == self.board[4] == self.board[5] == player:
            return True
        if self.board[6] == self.board[7] == self.board[8] == player:
            return True
        if self.board[0] == self.board[3] == self.board[6] == player:
            return True
        if self.board[1] == self.board[4] == self.board[7] == player:
            return True
        if self.board[2] == self.board[5] == self.board[8] == player:
            return True
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True
        return False

    def check_winner(self):
        if self.is_player_win(self.humanPlayer):
            return self.humanPlayer
        if self.is_player_win(self.botPlayer):
            return self.botPlayer
        if self.is_board_filled():
            return 'draw'
        return None

    def make_move(self, position):
        if self.board[position] == '-':
            self.board[position] = self.currentPlayer
            return True
        return False

    def switch_player(self):
        if self.currentPlayer == self.humanPlayer:
            self.currentPlayer = self.botPlayer
        else:
            self.currentPlayer = self.humanPlayer

class HumanPlayer:
    def __init__(self, game):
        self.game = game

    def make_move(self, position):
        return self.game.make_move(position)

class BotPlayer:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        best_score = -math.inf
        best_move = None

        for i in range(9):
            if self.game.board[i] == '-':
                self.game.board[i] = self.game.botPlayer
                score = self.minimax(self.game.board, 0, False)
                self.game.board[i] = '-'

                if score > best_score:
                    best_score = score
                    best_move = i

        self.game.make_move(best_move)

    def minimax(self, board, depth, is_maximizing):
        result = self.game.check_winner()

        if result == self.game.humanPlayer:
            return -1
        elif result == self.game.botPlayer:
            return 1
        elif result == 'draw':
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == '-':
                    board[i] = self.game.botPlayer
                    score = self.minimax(board, depth + 1, False)
                    board[i] = '-'
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == '-':
                    board[i] = self.game.humanPlayer
                    score = self.minimax(board, depth + 1, True)
                    board[i] = '-'
                    best_score = min(score, best_score)
            return best_score

game = TicTacToe()
human_player = HumanPlayer(game)
bot_player = BotPlayer(game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game.currentPlayer == game.humanPlayer:
            x, y = pygame.mouse.get_pos()
            row = y // (HEIGHT // 3)
            col = x // (WIDTH // 3)
            position = row * 3 + col
            if human_player.make_move(position):
                if game.check_winner() is None:
                    game.switch_player()

    if game.currentPlayer == game.botPlayer:
        bot_player.make_move()
        if game.check_winner() is None:
            game.switch_player()

    game.draw_board()

    result = game.check_winner()
    if result:
        if result == 'draw':
            text = font.render('Draw!', True, RED)
        else:
            text = font.render(f'{result} wins!', True, RED)
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))

    pygame.display.update()

pygame.quit()