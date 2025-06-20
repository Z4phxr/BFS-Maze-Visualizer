from enum import Enum
from collections import deque
import pygame


class Direction(Enum):
    UP = (0, -50)
    DOWN = (0, 50)
    LEFT = (-50, 0)
    RIGHT = (50, 0)


class Solution:
    def __init__(self, found, length=None):
        self.found = found
        self.length = length


class Mouse_Position:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.x_square = self.calculate_squares(x)
        self.y_square = self.calculate_squares(y)

    def calculate_squares(self, x):
        return (x // self.cell_size) * self.cell_size

    def update_mouse_position(self, x, y):
        self.x = x
        self.y = y
        self.x_square = self.calculate_squares(x)
        self.y_square = self.calculate_squares(y)

    def get_squares(self):
        return self.x_square, self.y_square


class Menu:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = None
        self.buttons = []
        button_color = (143, 122, 185)
        button_width = 160
        button_height = 70
        button_y = self.height - 85
        self.solution = None

        self.button_start = Button(570, button_y, button_width, button_height, button_color, "Start", 30)
        self.button_restart = Button(400, button_y, button_width, button_height, button_color, "Restart grid", 30)
        self.button_start_point = Button(25, self.height - 55, 113, 35, button_color, "Start Point", 22)
        self.button_end_point = Button(143, self.height - 55, 113, 35, button_color, "End Point", 22)
        self.button_obstacles = Button(261, self.height - 55, 113, 35, button_color, "Obstacles", 22)

        self.buttons.extend([
            self.button_start,
            self.button_restart,
            self.button_start_point,
            self.button_end_point,
            self.button_obstacles
        ])

    def draw_text(self):
        text = "Pick a component and click"
        text2 = "on the screen above to create a maze"
        font = pygame.font.Font(None, 22)
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface2 = font.render(text2, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(25 + 374 / 2, self.height - 103 + 20))
        text_rect2 = text_surface2.get_rect(center=(25 + 374 / 2, self.height - 88 + 20))
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(text_surface2, text_rect2)

    def draw_solution(self, solution: Solution):
        path_length = str(self.solution.length)
        menu_rect = pygame.Rect(0, 650, 380, 100)

        if solution.found:
            text = "Solution found!"
            text2 = f"Shortest path length: {path_length}"
            font_main = pygame.font.Font(None, 36)
        else:
            text = "Solution not found!"
            text2 = "The path doesn't exist"
            font_main = pygame.font.Font(None, 34)

        font_sub = pygame.font.Font(None, 24)
        text_surface = font_main.render(text, True, (255, 255, 255))
        text_surface2 = font_sub.render(text2, True, (255, 255, 255))
        center_x = menu_rect.centerx
        text_rect = text_surface.get_rect(center=(center_x, 685))
        text_rect2 = text_surface2.get_rect(center=(center_x, 715))
        background_rect = pygame.Rect(0, 0, 260, 70)
        background_rect.center = menu_rect.center

        gradient_colors = [
            (71, 61, 92),
            (93, 79, 120),
            (114, 97, 148),
            (143, 122, 185)
        ]

        for i, color in enumerate(gradient_colors):
            inflate = (len(gradient_colors) - i) * 16
            rect = background_rect.inflate(inflate, 0)
            rect.clamp_ip(menu_rect)
            pygame.draw.rect(self.screen, color, rect, border_radius=16)

        pygame.draw.rect(self.screen, (143, 122, 185), background_rect, border_radius=10)
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(text_surface2, text_rect2)

    def draw_menu(self, screen, bfs_run):
        pygame.draw.rect(screen, (190, 160, 210), (0, self.height - 100, self.width, 100))
        pygame.draw.line(screen, (110, 85, 135), (0, self.height - 100), (self.width, self.height - 100), 2)
        if not bfs_run:
            self.draw_text()
        for i, button in enumerate(self.buttons):
            if i < 2:
                button.draw_menu_button(screen)
            elif not bfs_run:
                button.draw_component_button(screen)
        if self.solution:
            self.draw_solution(self.solution)


class Screen:
    def __init__(self, height, width, cell_size):
        self.height = height
        self.width = width
        self.cell_size = cell_size
        self.rows = (height - 100) // cell_size
        self.cols = width // cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.obstacles = set()
        self.screen = None
        self.start_point = None
        self.end_point = None
        self.start_point_color = (125, 200, 185)
        self.end_point_color = (200, 115, 135)
        self.obstacle_color = (160, 120, 200)
        self.button_clicked = None
        self.grid_surface = None
        self.solution = None
        self.solution_found = True
        self.bfs_ran = False

    def button_handle(self, menu: Menu, mouse_position: Mouse_Position, screen):
        temp = None
        if self.button_clicked:
            temp = self.button_clicked
        for button in menu.buttons:
            if button.is_clicked(mouse_position):
                if temp and button != temp:
                    temp.clicked = False
                self.button_clicked = button
                button.clicked = True
                if self.button_clicked.text == "Restart grid":
                    self.clear_grid()
                    menu.solution = None
                elif self.button_clicked.text == "Start":
                    self.run_bfs(screen)
                    menu.solution = self.solution

    def run_bfs(self, screen):
        if not self.start_point or not self.end_point:
            return

        self.bfs_ran = True
        start = self.start_point
        end = self.end_point
        queue = deque([start])
        visited = {start}
        came_from = {}
        while queue:
            current = queue.popleft()
            if current == end:
                break
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = current[0] + dr, current[1] + dc
                neighbor = (nr, nc)
                if (0 <= nr < self.rows and 0 <= nc < self.cols and
                        neighbor not in visited and neighbor not in self.obstacles):
                    queue.append(neighbor)
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    if self.grid[nr][nc] == 0:
                        self.grid[nr][nc] = 4
                        self.draw_grid(screen)
                        screen.blit(self.grid_surface, (0, 0))
                        pygame.display.flip()
                        pygame.time.delay(20)

        self.solution_found = True
        path_length = 0
        current = end

        while current != start:
            if current in came_from:
                y, x = current
                if self.grid[y][x] != 3:
                    self.grid[y][x] = 5
                    self.draw_grid(screen)
                    screen.blit(self.grid_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(20)
                current = came_from[current]
                path_length += 1
            else:
                self.solution_found = False
                path_length = 0
                break
        self.solution = Solution(self.solution_found, path_length)

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.obstacles = set()
        self.button_clicked = None
        self.start_point = None
        self.end_point = None
        self.bfs_ran = False
        self.solution = None

    def add_component(self, mouse_position: Mouse_Position):
        x = mouse_position.x_square // self.cell_size
        y = mouse_position.y_square // self.cell_size
        if not self.bfs_ran and 0 <= y < self.rows and 0 <= x < self.cols:
            if self.button_clicked:
                if self.button_clicked.text == "Obstacles":
                    if (y, x) not in self.obstacles and self.grid[y][x] == 0:
                        self.obstacles.add((y, x))
                        self.grid[y][x] = 1

                elif self.button_clicked.text == "Start Point" and self.grid[y][x] == 0:
                    if self.start_point:
                        old_y, old_x = self.start_point
                        self.grid[old_y][old_x] = 0
                    self.start_point = (y, x)
                    self.grid[y][x] = 2

                elif self.button_clicked.text == "End Point" and self.grid[y][x] == 0:
                    if self.end_point:
                        old_y, old_x = self.end_point
                        self.grid[old_y][old_x] = 0
                    self.end_point = (y, x)
                    self.grid[y][x] = 3

    def remove_component(self, mouse_position: Mouse_Position):
        x = mouse_position.x_square // self.cell_size
        y = mouse_position.y_square // self.cell_size
        if not self.bfs_ran and 0 <= y < self.rows and 0 <= x < self.cols:
            if (y, x) in self.obstacles:
                self.obstacles.remove((y, x))
                self.grid[y][x] = 0
            elif (y, x) == self.start_point:
                self.start_point = None
                self.grid[y][x] = 0
            elif (y, x) == self.end_point:
                self.end_point = None
                self.grid[y][x] = 0

    def draw_grid(self, screen):
        for (row, col) in self.obstacles:
            x = col * self.cell_size
            y = row * self.cell_size
            pygame.draw.rect(screen, self.obstacle_color, (x, y, self.cell_size, self.cell_size))
        if self.start_point:
            row, col = self.start_point
            x = col * self.cell_size
            y = row * self.cell_size
            pygame.draw.rect(screen, self.start_point_color, (x, y, self.cell_size, self.cell_size))
        if self.end_point:
            row, col = self.end_point
            x = col * self.cell_size
            y = row * self.cell_size
            pygame.draw.rect(screen, self.end_point_color, (x, y, self.cell_size, self.cell_size))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 4:
                    pygame.draw.rect(screen, (226, 226, 250), (col * self.cell_size, row * self.cell_size,
                                                               self.cell_size, self.cell_size))
                elif self.grid[row][col] == 5:
                    pygame.draw.rect(screen, (255, 236, 185), (col * self.cell_size, row * self.cell_size,
                                                               self.cell_size, self.cell_size))

    def create_grid_surface(self):
        grid_surface = pygame.Surface((self.width, self.height - 100), pygame.SRCALPHA)
        for i in range(self.rows + 1):
            y = i * self.cell_size
            pygame.draw.line(grid_surface, (211, 211, 211), (0, y), (self.width, y), 1)
        for i in range(self.cols + 1):
            x = i * self.cell_size
            pygame.draw.line(grid_surface, (211, 211, 211), (x, 0), (x, self.height - 100), 1)
        self.grid_surface = grid_surface
        return grid_surface


class Button:
    def __init__(self, x, y, width, height, color, text, text_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_color = color
        self.hover_color = (115, 90, 155)
        self.shadow_color = (100, 70, 120)
        self.text_color = (255, 255, 255)
        self.text = text
        self.text_size = text_size
        self.clicked = False

    def draw_component_button(self, screen):
        color = self.hover_color if self.clicked else self.base_color
        pygame.draw.rect(screen, self.shadow_color, (self.x + 2, self.y + 2, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)
        font = pygame.font.Font(None, self.text_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def draw_menu_button(self, screen):
        color = self.base_color
        pygame.draw.rect(screen, self.shadow_color, (self.x + 2, self.y + 2, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)
        font = pygame.font.Font(None, self.text_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_position: Mouse_Position):
        if self.x < mouse_position.x < self.x + self.width and self.y < mouse_position.y < self.y + self.height:
            self.clicked = True
            return True
        return False
