import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 40
GRID_SIZE = 10
NUM_MINES = 10
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE + 50  # Extra space for the timer and reset button

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Cell class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def draw(self, screen):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.is_revealed:
            pygame.draw.rect(screen, GRAY, rect)
            if self.is_mine:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
            elif self.neighbor_mines > 0:
                font = pygame.font.SysFont(None, 24)
                text = font.render(str(self.neighbor_mines), True, BLACK)
                screen.blit(text, text.get_rect(center=rect.center))
        else:
            pygame.draw.rect(screen, WHITE, rect)
            if self.is_flagged:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
        pygame.draw.rect(screen, BLACK, rect, 1)

# Board class
class Board:
    def __init__(self, grid_size, num_mines):
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.cells = [[Cell(x, y) for y in range(grid_size)] for x in range(grid_size)]
        self.place_mines()
        self.calculate_neighbors()

    def place_mines(self):
        mines = random.sample(range(self.grid_size * self.grid_size), self.num_mines)
        for mine in mines:
            x, y = divmod(mine, self.grid_size)
            self.cells[x][y].is_mine = True

    def calculate_neighbors(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.cells[x][y].is_mine:
                    continue
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.cells[nx][ny].is_mine:
                            self.cells[x][y].neighbor_mines += 1

    def reveal_cell(self, x, y):
        if self.cells[x][y].is_flagged or self.cells[x][y].is_revealed:
            return
        self.cells[x][y].is_revealed = True
        if self.cells[x][y].is_mine:
            return
        if self.cells[x][y].neighbor_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        self.reveal_cell(nx, ny)

    def flag_cell(self, x, y):
        if not self.cells[x][y].is_revealed:
            self.cells[x][y].is_flagged = not self.cells[x][y].is_flagged

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.board = Board(GRID_SIZE, NUM_MINES)
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.win = False

    def draw_timer(self):
        if not self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        else:
            elapsed_time = self.elapsed_time_at_game_end
        timer_text = self.font.render(f"Time: {elapsed_time}", True, BLACK)
        self.screen.blit(timer_text, (10, HEIGHT - 40))

    def draw_reset_button(self):
        reset_button = pygame.Rect(WIDTH - 100, HEIGHT - 40, 80, 30)
        pygame.draw.rect(self.screen, GRAY, reset_button)
        reset_text = self.font.render("Reset", True, BLACK)
        self.screen.blit(reset_text, (WIDTH - 90, HEIGHT - 35))
        return reset_button

    def check_win_condition(self):
        for row in self.board.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def run(self):
        while True:
            self.screen.fill(WHITE)
            self.board.draw(self.screen)
            self.draw_timer()
            reset_button = self.draw_reset_button()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if reset_button.collidepoint(x, y):
                        self.reset_game()
                    elif y < HEIGHT - 50 and not self.game_over:
                        cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
                        if event.button == 1:  # Left-click
                            self.board.reveal_cell(cell_x, cell_y)
                            if self.board.cells[cell_x][cell_y].is_mine:
                                self.game_over = True
                                self.elapsed_time_at_game_end = (pygame.time.get_ticks() - self.start_time) // 1000
                                print("Game Over!")
                            elif self.check_win_condition():
                                self.game_over = True
                                self.win = True
                                self.elapsed_time_at_game_end = (pygame.time.get_ticks() - self.start_time) // 1000
                                print("You won!")
                        elif event.button == 3:  # Right-click
                            self.board.flag_cell(cell_x, cell_y)

            if self.win:
                win_text = self.font.render("You Won!", True, RED)
                self.screen.blit(win_text, (WIDTH // 2 - 40, HEIGHT // 2))

            pygame.display.flip()

# Start the game
if __name__ == "__main__":
    Game().run()
import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 40
GRID_SIZE = 10
NUM_MINES = 10
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE + 50  # Extra space for the timer and reset button

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Cell class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def draw(self, screen):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.is_revealed:
            pygame.draw.rect(screen, GRAY, rect)
            if self.is_mine:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
            elif self.neighbor_mines > 0:
                font = pygame.font.SysFont(None, 24)
                text = font.render(str(self.neighbor_mines), True, BLACK)
                screen.blit(text, text.get_rect(center=rect.center))
        else:
            pygame.draw.rect(screen, WHITE, rect)
            if self.is_flagged:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
        pygame.draw.rect(screen, BLACK, rect, 1)

# Board class
class Board:
    def __init__(self, grid_size, num_mines):
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.cells = [[Cell(x, y) for y in range(grid_size)] for x in range(grid_size)]
        self.place_mines()
        self.calculate_neighbors()

    def place_mines(self):
        mines = random.sample(range(self.grid_size * self.grid_size), self.num_mines)
        for mine in mines:
            x, y = divmod(mine, self.grid_size)
            self.cells[x][y].is_mine = True

    def calculate_neighbors(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.cells[x][y].is_mine:
                    continue
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.cells[nx][ny].is_mine:
                            self.cells[x][y].neighbor_mines += 1

    def reveal_cell(self, x, y):
        if self.cells[x][y].is_flagged or self.cells[x][y].is_revealed:
            return
        self.cells[x][y].is_revealed = True
        if self.cells[x][y].is_mine:
            return
        if self.cells[x][y].neighbor_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        self.reveal_cell(nx, ny)

    def flag_cell(self, x, y):
        if not self.cells[x][y].is_revealed:
            self.cells[x][y].is_flagged = not self.cells[x][y].is_flagged

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.board = Board(GRID_SIZE, NUM_MINES)
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.win = False

    def draw_timer(self):
        if not self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        else:
            elapsed_time = self.elapsed_time_at_game_end
        timer_text = self.font.render(f"Time: {elapsed_time}", True, BLACK)
        self.screen.blit(timer_text, (10, HEIGHT - 40))

    def draw_reset_button(self):
        reset_button = pygame.Rect(WIDTH - 100, HEIGHT - 40, 80, 30)
        pygame.draw.rect(self.screen, GRAY, reset_button)
        reset_text = self.font.render("Reset", True, BLACK)
        self.screen.blit(reset_text, (WIDTH - 90, HEIGHT - 35))
        return reset_button

    def check_win_condition(self):
        for row in self.board.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def run(self):
        while True:
            self.screen.fill(WHITE)
            self.board.draw(self.screen)
            self.draw_timer()
            reset_button = self.draw_reset_button()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if reset_button.collidepoint(x, y):
                        self.reset_game()
                    elif y < HEIGHT - 50 and not self.game_over:
                        cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
                        if event.button == 1:  # Left-click
                            self.board.reveal_cell(cell_x, cell_y)
                            if self.board.cells[cell_x][cell_y].is_mine:
                                self.game_over = True
                                self.elapsed_time_at_game_end = (pygame.time.get_ticks() - self.start_time) // 1000
                                print("Game Over!")
                            elif self.check_win_condition():
                                self.game_over = True
                                self.win = True
                                self.elapsed_time_at_game_end = (pygame.time.get_ticks() - self.start_time) // 1000
                                print("You won!")
                        elif event.button == 3:  # Right-click
                            self.board.flag_cell(cell_x, cell_y)

            if self.win:
                win_text = self.font.render("You Won!", True, RED)
                self.screen.blit(win_text, (WIDTH // 2 - 40, HEIGHT // 2))

            pygame.display.flip()

# Start the game
if __name__ == "__main__":
    Game().run()
