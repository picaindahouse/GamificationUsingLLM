import pygame
from settings import *
from support import background

class Control:
    def __init__(self):
        
        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 30)
        self.line_height = 30  # Adjust this for spacing between lines

    def display(self):
        
        # Create semi-transparent background
        background(self.display_surface, 238)

        # Title
        title_surf = self.title_font.render("Control Menu", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(self.display_surface.get_width() // 2, 110))
        self.display_surface.blit(title_surf, title_rect)

        ### Creating Controls ###

        # Finding Column width
        max_width_left = max(len(action) for action in controls.keys())
        max_width_right = max(len(description) for description in controls.values())
        max_width = max(max_width_right, max_width_left) * 18

        # Display controls as a table
        table_x = self.display_surface.get_width() * 0.2
        table_y = self.display_surface.get_height() * 0.25

        for control, description in controls.items():
            action_text = f"{control}"
            action_surf = self.font.render(action_text, True, TEXT_COLOR)
            action_rect = action_surf.get_rect(topleft=(table_x, table_y))
            self.display_surface.blit(action_surf, action_rect)

            description_text = f"{description}"
            description_surf = self.font.render(description_text, True, TEXT_COLOR)
            description_rect = description_surf.get_rect(topleft=(max_width + table_x - 27, table_y))
            self.display_surface.blit(description_surf, description_rect)

            table_y += self.line_height

        # Add lines at the start and end of controls
        line_start = (self.display_surface.get_width() * 0.2, self.display_surface.get_height() * 0.3 - 10)
        line_end = (self.display_surface.get_width() * 0.8, table_y)
        pygame.draw.line(self.display_surface, TEXT_COLOR, line_start, (line_end[0], line_start[1]), 5)
        pygame.draw.line(self.display_surface, TEXT_COLOR, (line_start[0], line_end[1]), line_end, 5)