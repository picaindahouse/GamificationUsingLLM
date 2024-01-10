import pygame
from settings import *
from chatbot import Chatbot
from support import background

class Story(Chatbot):
    def __init__(self):

        # General Setup
        super().__init__()

        self.max_width = self.display_surface.get_width() * 0.8 - 200

    def ask_question(self, question, id):
        background(self.display_surface, 200)
        self.draw_dialog(question, self.teacher_thumbnail, 200, 100, self.max_width)
        
        if len(self.chat_history) == id:
            self.write_reply = True
            self.ready_for_qn = False
            
        else:
            self.ready_for_qn = True

        self.input_box("Please type your question here...")
