import pygame
from settings import *
from support import import_folder, background
from chatbot import Chatbot
from llm import LLM
from random import choice

class Tome(Chatbot):
    def __init__(self):

        super().__init__()

        # Tome Pages
        slides_path = "ModelDeploymentImages"
        self.lost_pages =  import_folder(slides_path)
        self.found_pages = []
        self.searching_page = 0

        # Fade
        self.alpha = 0

        # Buttons
        self.next = None
        self.next_selected = False
        self.prev = None
        self.prev_selected = False
        self.discuss = None
        self.discuss_selected = False
        self.discuss_text = 'Discuss'
        
        self.discuss_ai = None
        self.have_discuss_ai = False
        self.discuss_answer = None
        self.have_discuss_answer = False

        # Test Buttons & Chat Params
        self.test = None
        self.test_selected = False
        self.test_text = 'Test'
        self.test_chat_history = []
        self.test_qns_answered = 0
        self.next_day = False

        self.text_ai = None
        self.have_test_ai = False
        self.test_question = None
        self.have_test_question = False

        # QnA
        self.qns_answered = 0
        self.max_width = self.display_surface.get_width() * 0.8 - 200

        # Final TEST
        self.final_test_qns = 0
        self.have_final_ai = False
        self.final_ai = None
        self.have_final_question = False
        self.final_question = None
 
    def reset(self, alpha = 0):
        self.alpha = alpha
        self.chat_history = []
        self.test_chat_history = []
        self.user_input = ''
        self.write_reply = False
        self.ready_for_qn = True
        self.qns_answered = 0
        self.test_qns_answered = 0
        self.next_day = False
        self.discuss_ai = None
        self.have_discuss_ai = False
        self.discuss_answer = None
        self.have_discuss_answer = False
        self.text_ai = None
        self.have_test_ai = False
        self.test_question = None
        self.have_test_question = False
        self.discuss_text = 'Discuss'
        self.test_text = 'Test'

    def create_test_system(self):
        summary = slides_summary[str(self.searching_page+1) + '.jpg'].lower()
        system = "You are testing " + user_info['name'] + ". on the following topic: [" + summary + \
                 "] You will do this by continuously asking the player questions. " + \
                 "If the answer is correct inform the player how many questions they have gotten right, then proceed to the next question. If the answer is wrong, explain the mistake to the player. " + \
                 "Once the player answers 3 questions correctly just reply with 'pass123' and end the test. " + \
                 "You are to ensure that you strictly follow the topic I gave when checking the answers for questions."
        return system
        
    def create_discussion_system(self):
        summary = slides_summary[str(self.searching_page+1) + '.jpg']
        system = "You are a game character speaking to the player. " + \
                 "Here are the details you should know: " + \
                 "Your name is " + user_info['teacher_name'] + \
                 ". You are to channel your inner " + user_info['teacher_persona'] + ". Keep it subtle and let this personality trait flow seamlessly into your response. " + \
                 "Players name is " + user_info['name'] + ". " +\
                 "The player will now ask you questions about the following page they came across and you are to answer them. "
        return system + summary + " Remember to let your personality flow!"
                
    def found_page(self):
        self.found_pages.append(self.lost_pages.pop(0))

    def button(self, text, x, y, selected):
        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        if selected:
            button_surf = self.font.render(text, True, TEXT_COLOR_SELECTED)
            bg_color = UPGRADE_BG_COLOR_SELECTED
        else:
            button_surf = self.font.render(text, True, TEXT_COLOR)
            bg_color = UI_BG_COLOR

        pygame.draw.rect(self.display_surface, bg_color, rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, rect, 4)
        button_rect = button_surf.get_rect(center=rect.center)
        self.display_surface.blit(button_surf, button_rect)
        return rect

    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.next.collidepoint(mouse_pos):
            self.next_selected = True
        else:
            self.next_selected = False
        
        if self.prev.collidepoint(mouse_pos):
            self.prev_selected = True
        else:
            self.prev_selected = False

        if self.discuss.collidepoint(mouse_pos):
            self.discuss_selected = True
        else:
            self.discuss_selected = False

        if self.test.collidepoint(mouse_pos):
            self.test_selected = True
        else:
            self.test_selected = False

    def fade(self):
        # Apply the fading effect
        if self.alpha < 255:
            self.alpha += 5
            if self.alpha > 255:
                self.alpha = 255

    def mouse(self, event):
        # Left mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.next_selected and self.searching_page < len(self.found_pages) - 1:
                if self.discuss_text == "Discuss":
                    self.searching_page += 1
                    
                    # Reset convo
                    self.reset(255)
            
            elif self.prev_selected and self.searching_page > 0:
                if self.discuss_text == "Discuss":
                    self.searching_page -= 1
                    
                    # Reset convo
                    self.reset(255)

            elif self.discuss_selected:
                if self.discuss_text == "Discuss":
                    self.discuss_text = "Leave"
                    self.write_reply = True

                    self.test_text = "Test"
                else:
                    self.discuss_text = "Discuss"
                    self.write_reply = False

            elif self.test_selected:
                if self.test_text == "Test":
                    self.test_text = "Leave"
                    self.write_reply = True
                    
                    self.discuss_text = "Discuss"
                    
                else:
                    self.test_text = "Test"
                    self.write_reply = False
        else:
            if self.test_text == "Leave":
                self.reply(event, self.test_chat_history)
            elif self.discuss_text == "Leave":
                self.reply(event)

    def display_message(self, message):
        message_surf = self.font.render(message, True, TEXT_COLOR)
        message_rect = message_surf.get_rect(center=(self.display_surface.get_width() // 2,
                                                    self.display_surface.get_height() // 2))
        self.display_surface.blit(message_surf, message_rect)

    def open(self):  
        if self.alpha == 255:      
            if self.found_pages:
                self.display_surface.fill((255, 255, 255))
                image_to_show = pygame.transform.scale(self.found_pages[self.searching_page], (PAGE_WIDTH, PAGE_HEIGHT))
                image_rect = image_to_show.get_rect(midtop=self.display_surface.get_rect().midtop)
                self.display_surface.blit(image_to_show, image_rect)

                self.discuss = self.button(self.discuss_text,
                                           (WIDTH - BUTTON_WIDTH) // 2 - BUTTON_WIDTH // 2 - 1,
                                           HEIGHT - BUTTON_HEIGHT,
                                           self.discuss_selected)
                
                self.test = self.button(self.test_text,
                                           (WIDTH - BUTTON_WIDTH) // 2 + BUTTON_WIDTH // 2 + 1,
                                           HEIGHT - BUTTON_HEIGHT,
                                           self.test_selected)

                if self.discuss_text == "Leave":
                    background(self.display_surface, 200)
                    self.input_box("Please type your question here...")
                    if self.qns_answered < len(self.chat_history):
                        if len(self.chat_history) - self.qns_answered == 2:
                            self.qns_answered += 1
                            self.have_discuss_answer = False

                        self.draw_dialog(self.chat_history[-1], self.user_thumbnail, 200, 100, self.max_width)
                        
                        if not self.have_discuss_ai:
                            self.discuss_ai = LLM(self.create_discussion_system())
                            self.have_discuss_ai = True

                        if not self.have_discuss_answer:
                            self.have_discuss_answer = True
                            self.discuss_answer = self.discuss_ai.ask_chatgpt(self.chat_history[-1], 120)

                        self.draw_dialog(self.discuss_answer, self.teacher_thumbnail, 200, 100 + self.first_message_height + 50, self.max_width)
                        self.write_reply = True
                
                elif self.test_text == "Leave":
                    background(self.display_surface, 200)
                    if len(self.found_pages) == self.searching_page + 1: 
                        if len(self.found_pages) > 2 and len(self.lost_pages) > 0:

                            if not self.have_test_ai:
                                self.test_ai = LLM(self.create_test_system())
                                self.have_test_ai = True

                            if not self.have_test_question:
                                self.test_question = self.test_ai.ask_chatgpt("Please ask the first question.", 120)
                                self.have_test_question = True

                            self.draw_dialog(self.test_question, self.teacher_thumbnail, 200, 100, self.max_width)
                            self.input_box("Please type your answer here...")

                            if self.test_qns_answered < len(self.test_chat_history):
                                self.test_qns_answered += 1
                                self.draw_dialog(self.test_chat_history[-1], self.user_thumbnail, 200, 100 + self.first_message_height + 50, self.max_width)
                                self.test_question = self.test_ai.ask_chatgpt(self.test_chat_history[-1], 120, 0.3)
                                self.write_reply = True

                            if 'pass123' in self.test_question.lower():
                                self.next_day = True

                        elif len(self.lost_pages) == 0:
                            if self.final_test_qns == 10:
                                self.display_message("CONGRATULATIONS YOU PASS! YOU HAVE COMPLETED THE GAME!")
                            else:
                                if not self.have_final_ai:
                                    #print("Number of Questions Answered: " + str(self.final_test_qns))
                                    random_page = choice(range(2, len(self.found_pages))) + 1
                                    content = slides_summary[str(random_page) + '.jpg'].lower()
                                    system = "You are testing a user, they have answered " + str(self.final_test_qns) + " correctly. " + \
                                            "You are testing the user on the following topic: [" + content + "]. " + \
                                            "If the answer is correct just reply with 'pass123' and end the test. " + \
                                            "If the answer is wrong, explain the mistake to the player and then ask another question. Continue asking until user gets one question correct. "
                                    self.final_ai = LLM(system)
                                    self.have_final_ai = True
                                
                                if not self.have_final_question:
                                    self.final_question = self.final_ai.ask_chatgpt("Please ask the question.", 120)
                                    self.have_final_question = True

                                self.draw_dialog(self.final_question, self.teacher_thumbnail, 200, 100, self.max_width)
                                self.input_box("Please type your answer here...")

                                if self.test_qns_answered < len(self.test_chat_history):
                                    self.test_qns_answered += 1
                                    self.draw_dialog(self.test_chat_history[-1], self.user_thumbnail, 200, 100 + self.first_message_height + 50, self.max_width)
                                    self.final_question = self.final_ai.ask_chatgpt(self.test_chat_history[-1], 120, 0.3)
                                    self.write_reply = True

                                if 'pass123' in self.final_question.lower():
                                    #print("passed")
                                    self.have_final_ai = False
                                    self.have_final_question = False     
                                    self.final_test_qns += 1                        



                        else:
                            self.display_message("TESTS ONLY BEGIN FROM THIRD PAGE!")

                    else:
                        self.display_message("Go to last slide to take test!")

                else:
                    self.next = self.button("Next", 
                                            WIDTH - BUTTON_WIDTH, 
                                            HEIGHT - BUTTON_HEIGHT,
                                            self.next_selected)
                    self.prev = self.button("Prev",
                                            0,
                                            HEIGHT - BUTTON_HEIGHT,
                                            self.prev_selected)
                
                self.hover()

            else:
                message = "Find Pages of Tome of Knowledge to View"
                self.display_surface.fill((0, 0, 0))
                background(self.display_surface, 200)
                self.display_message(message)

        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.alpha))
            self.display_surface.blit(overlay, (0, 0))
            self.fade()
    
        
