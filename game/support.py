from csv import reader
from os import walk
import pygame
from settings import *

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def text_wrap(text, font, max_width):
	words = text.split(' ')
	lines = []
	current_line = ''
	for word in words:
		test_line = current_line + word + ' '
		test_width, _ = font.size(test_line)
		if test_width <= max_width:
			current_line = test_line
		else:
			lines.append(font.render(current_line, True, TEXT_COLOR))
			current_line = word + ' '
	lines.append(font.render(current_line, True, TEXT_COLOR))
	return lines

def background(surface, alpha, ratio = 0.8):
	tran_height = surface.get_size()[1] * ratio
	tran_width = surface.get_size()[0] * ratio
	
	semi_transparent_rect = pygame.Surface((tran_width, 
											tran_height),
											pygame.SRCALPHA)
	pygame.draw.rect(semi_transparent_rect,
						(100, 100, 100, alpha),
						semi_transparent_rect.get_rect(),
						border_radius=10)

	tran_x = (surface.get_size()[0] - tran_width) // 2
	tran_y = (surface.get_size()[1] - tran_height) //2
	
	surface.blit(semi_transparent_rect, (tran_x, tran_y))

def update(story):
	story = story.replace("[persona]", user_info['teacher_persona'])
	story = story.replace("[teacher_name]", user_info['teacher_name'])
	story = story.replace("[player_name]", user_info['name'])
	return story
