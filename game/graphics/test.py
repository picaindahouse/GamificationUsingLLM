import pygame
from PIL import Image

pygame.init()

# Load your 16x16 sprite image
original_sprite = pygame.image.load('EggBoy/Faceset.png')

# Create a new surface with a size of 64x64
scaled_sprite = pygame.transform.scale(original_sprite, (100, 100))

# Display the scaled sprite on the screen (optional for visualization)
pygame.image.save(scaled_sprite, 'EggBoy/Faceset.png')
