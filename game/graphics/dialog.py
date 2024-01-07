import pygame
import sys

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chat Dialog')

# Load the thumbnail image
thumbnail = pygame.image.load('OldMan/thumbnail.png').convert()
thumbnail = pygame.transform.scale(thumbnail, (100, 100))  # Resize the thumbnail

# Define the font and text size
font = pygame.font.Font(None, 28)

def draw_dialog(message, user_reply):
    # Clear the screen
    screen.fill(WHITE)

    # Render the message text
    message_lines = message.splitlines()
    rendered_lines = []
    for line in message_lines:
        rendered_lines.append(font.render(line, True, BLACK))

    # Calculate the size of the dialog box needed for the message
    message_height = sum([surface.get_height() for surface in rendered_lines]) + 20  # Extra padding
    max_line_width = max([surface.get_width() for surface in rendered_lines])
    message_rect = pygame.Rect(150, 50, max_line_width + 20, message_height)

    # Draw the colored box around the message text
    pygame.draw.rect(screen, GRAY, message_rect)

    # Blit the message text onto the screen
    y_offset = 10
    for surface in rendered_lines:
        screen.blit(surface, (message_rect.x + 10, message_rect.y + y_offset))
        y_offset += surface.get_height()

    # Draw the dialog box for the user's reply
    reply_rect = pygame.Rect(150, message_rect.bottom + 20, WIDTH - 200, 50)
    pygame.draw.rect(screen, BLUE, reply_rect)
    reply_surface = font.render(user_reply, True, BLACK)
    screen.blit(reply_surface, (reply_rect.x + 5, reply_rect.y + 5))

    # Draw the thumbnail
    thumbnail_rect = thumbnail.get_rect(topleft=(50, 50))
    pygame.draw.rect(screen, WHITE, thumbnail_rect)
    screen.blit(thumbnail, thumbnail_rect)

    pygame.display.flip()

running = True
user_reply = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("User replied:", user_reply)
                user_reply = ""
            elif event.key == pygame.K_BACKSPACE:
                user_reply = user_reply[:-1]
            else:
                user_reply += event.unicode

    # Display the dialog with a sample message
    draw_dialog("This is an exam\nple messa\nge from\n the Old Man. Type your re\nply:\nThis is a new line.", user_reply)

pygame.quit()
