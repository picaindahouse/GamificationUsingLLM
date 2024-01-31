import pygame
from settings import *
from chatbot import Chatbot

class Creation(Chatbot):
    def __init__(self):

        # General Setup
        super().__init__()

    def ask_question(self, question, max_width, id):
        self.draw_dialog(question, self.teacher_thumbnail, (WIDTH - max_width)/2, 200, max_width)
        if len(self.chat_history) == id:
            self.write_reply = True
            self.ready_for_qn = False
            
        else:
            y_start = 200 + self.first_message_height + 50
            self.draw_dialog(self.chat_history[-1], self.user_thumbnail, (WIDTH - max_width)/2, y_start, max_width, False)
            self.ready_for_qn = True

        self.input_box("Please type your answer here...")

        

        

                

    
