from gettext import find
import pygame
from settings import *
from chatbot import Chatbot
from support import update
from llm import LLM

class Tutorial(Chatbot):
    def __init__(self):

        # General Setup
        super().__init__()
        self.end = False
        system = update(tutorial_system)
        self.control_rules = LLM(system).ask_chatgpt(control_rules, 60)
        self.find_rules = LLM(system).ask_chatgpt(find_rules, 60)
        self.found_rules = LLM(system).ask_chatgpt(found_rules, 60)

    def control(self):
        self.draw_dialog(self.control_rules, self.teacher_thumbnail, 810, 20, 400)

    def find(self):
        self.draw_dialog(self.find_rules, self.teacher_thumbnail, 610, 20, 600)

    def found(self):
        self.draw_dialog(self.found_rules, self.teacher_thumbnail, 610, 20, 600)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.end = True
        