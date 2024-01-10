import pygame
from settings import *
from support import text_wrap

class Chatbot:
    def __init__(self):

        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.first_message_height = 0

        # Load Images
        self.teacher_thumbnail = pygame.image.load('graphics/OldMan/thumbnail.png').convert()
        self.user_thumbnail = pygame.image.load('graphics/EggBoy/Faceset.png').convert()

        # Reply
        self.chat_history = []
        self.user_input = ''
        self.write_reply = False
        self.ready_for_qn = True

    def draw_dialog(self, message, thumbnail, x, y, max_width, first = True):
        # Render the message text
        rendered_lines = text_wrap(message, self.font, max_width - 50)

        # Calculate the size of the dialog box needed for the message
        message_height = max(100, sum([surface.get_height() for surface in rendered_lines]) + 20)  # Extra padding
        width = max_width - 42
        message_rect = pygame.Rect(x + 100, y, width, message_height)

        # Save message_height for next box
        if first:
            self.first_message_height = message_height

        # Draw the colored box around the message text
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, message_rect.inflate(20,20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, message_rect.inflate(20,20), 3)

        # Blit the message text onto the screen
        y_offset = 10
        for surface in rendered_lines:
            self.display_surface.blit(surface, (message_rect.x + 10, message_rect.y + y_offset))
            y_offset += surface.get_height()

        # Draw the thumbnail
        thumbnail_rect = thumbnail.get_rect(topleft=(x, y))
        pygame.draw.rect(self.display_surface, (0,0,0), thumbnail_rect)
        self.display_surface.blit(thumbnail, thumbnail_rect)

    def reply(self, event, chat = "base"):
        if chat == "base":
            chat = self.chat_history
        if self.write_reply:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(self.user_input) > 0:
                        chat.append(self.user_input)
                        self.write_reply = False
                        self.user_input = ''
                else:
                    self.user_input += event.unicode
    
    def input_box(self, placeholder):
        # Decide how big the input box needs to be
        if self.user_input == '':
            input = placeholder
        else:
            input = "You: " + self.user_input
            
        rendered_lines = text_wrap(input, self.font, 780 - 80)
        input_height = sum([surface.get_height() for surface in rendered_lines]) + 10  # Extra padding
        input_rect = pygame.Rect(250, self.display_surface.get_size()[1] * 0.85 - (input_height + 10), 780, input_height)

        # Draw input box
        pygame.draw.rect(self.display_surface, '#6495ED', input_rect)
        pygame.draw.rect(self.display_surface, '#1E4870', input_rect, 3)

        # Display user input text in the input box
        x_offset = 5
        y_offset = 5
        for surface in rendered_lines:
            self.display_surface.blit(surface, (input_rect.x + x_offset, input_rect.y + y_offset))
            y_offset += surface.get_height()
            if x_offset == 5:
                x_offset = 80