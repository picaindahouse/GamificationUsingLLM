import pygame
from settings import *
from support import import_folder, background
from chatbot import Chatbot

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

        # Test Buttons & Chat Params
        self.test = None
        self.test_selected = False
        self.test_text = 'Test'
        self.test_chat_history = []
        self.test_qns_answered = 0

        # QnA
        self.qns_answered = 0
        self.max_width = self.display_surface.get_width() * 0.8 - 200

    def reset(self, alpha = 0):
        self.alpha = alpha
        self.chat_history = []
        self.test_chat_history = []
        self.user_input = ''
        self.write_reply = False
        self.ready_for_qn = True
        self.qns_answered = 0
        self.test_qns_answered = 0

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
                        self.draw_dialog(self.chat_history[-1], self.user_thumbnail, 200, 100, self.max_width)
                
                elif self.test_text == "Leave":
                    background(self.display_surface, 200)
                    if len(self.found_pages) == self.searching_page + 1: 
                        self.input_box("Please type your answer here...")
                        if self.test_qns_answered < len(self.test_chat_history):
                            self.draw_dialog(self.test_chat_history[-1], self.user_thumbnail, 200, 100, self.max_width)
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
    
        