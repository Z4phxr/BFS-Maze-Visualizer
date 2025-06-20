import pygame
from MazeSolver import Mouse_Position, Menu, Screen


def main():
    pygame.init()
    clock = pygame.time.Clock()
    width, height = 750, 750
    cell_size = 50
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Breadth-first search")
    game_screen = Screen(height, width, cell_size)
    menu = Menu(height, width)
    menu.screen = screen
    mouse_position = Mouse_Position(0, 0, cell_size)
    grid_surface = game_screen.create_grid_surface()
    running = True
    left_mouse_held = False
    right_mouse_held = False
    last_obstacle_pos = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_mouse_held = True
                    game_screen.button_handle(menu, mouse_position, screen)

                elif event.button == 3:
                    right_mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_mouse_held = False
                    last_obstacle_pos = None
                elif event.button == 3:
                    right_mouse_held = False
                    last_obstacle_pos = None

        mx, my = pygame.mouse.get_pos()
        mouse_position.update_mouse_position(mx, my)
        pos = mouse_position.get_squares()
        if left_mouse_held and pos != last_obstacle_pos:
            game_screen.add_component(mouse_position)
            last_obstacle_pos = pos
        elif right_mouse_held and pos != last_obstacle_pos:
            game_screen.remove_component(mouse_position)
            last_obstacle_pos = pos

        screen.fill((246, 239, 250))
        game_screen.draw_grid(screen)
        screen.blit(grid_surface, (0, 0))
        menu.draw_menu(screen, game_screen.bfs_ran)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
