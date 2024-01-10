import pygame
from PIL import Image

pygame.init()

# Load your 16x16 sprite image
original_sprite = pygame.image.load('NinjaAdventure/Items/Scroll/ScrollEmpty.png')
original_sprite1 = pygame.image.load('NinjaAdventure/Items/Scroll/ScrollRock.png')

# Create a new surface with a size of 64x64
scaled_sprite = pygame.transform.scale(original_sprite, (64, 64))
scaled_sprite1 = pygame.transform.scale(original_sprite1, (64, 64))

# Display the scaled sprite on the screen (optional for visualization)
pygame.image.save(scaled_sprite, 'scroll.png')
pygame.image.save(scaled_sprite1, 'scroll1.png')
