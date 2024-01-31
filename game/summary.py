import pygame
from settings import *
from chatbot import Chatbot
from support import background
from llm import LLM

class Summary(Chatbot):
    def __init__(self):

        # General Setup
        super().__init__()

        self.max_width = self.display_surface.get_width() * 0.95 - 200
        self.alpha = 0
        self.sum = None
        self.sum_selected = False
        self.sum_text = 'Leave'
        self.ans = ''
        self.create_ans = False

    def reset(self):
        self.alpha = 0
        self.sum_selected = False
        self.sum_text = 'Leave'
        self.create_ans = False
        self.ans = ''

    def fade(self):
        # Apply the fading effect
        if self.alpha < 255:
            self.alpha += 5
            if self.alpha > 255:
                self.alpha = 255
    
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
    
    def mouse(self, event):
        # Left mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.sum_selected:
                if self.sum_text == "Summary":
                    self.sum_text = "Leave"
                    self.write_reply = True
                else:
                    self.sum_text = "Summary"
                    self.write_reply = False
    
    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.sum.collidepoint(mouse_pos):
            self.sum_selected = True
        else:
            self.sum_selected = False

    def ai_summary(self, content):
        question = "The user has come across a slide. Please provide the user with a summary of the content that is on said page." + \
                 " This is the content on said page: " + content + " Remember to subtly bring up your personality trait during your reply."
        
        system = "You are a game character speaking to the player. " + \
                 "Here are the details you should know: " + \
                 "Your name is " + user_info['teacher_name'] + \
                 ". You are to channel your inner " + user_info['teacher_persona'] + ". Keep it subtle and let this personality trait flow seamlessly into your response. " + \
                 "Players name is " + user_info['name'] + ". "
        
        return LLM(system).ask_chatgpt(question, 300)

    def summarise(self, found_pages):
        if self.alpha == 255:
            # Show newly found image
            self.display_surface.fill((255, 255, 255))
            image_to_show = pygame.transform.scale(found_pages[-1], (PAGE_WIDTH, PAGE_HEIGHT))
            image_rect = image_to_show.get_rect(midtop=self.display_surface.get_rect().midtop)
            self.display_surface.blit(image_to_show, image_rect)

            if self.sum_text == "Leave":
                # Show summary
                background(self.display_surface, 200, 0.95)
                page_number = len(found_pages)
                if self.create_ans == False:
                    self.create_ans = True
                    self.ans = self.ai_summary(slides_summary[str(page_number) + '.jpg'])
                summary = self.ans
                self.draw_dialog(summary, self.teacher_thumbnail, 82, 35, self.max_width)

            # Create Button
            self.sum = self.button(self.sum_text,
                                   (WIDTH - BUTTON_WIDTH) // 2,
                                   HEIGHT - BUTTON_HEIGHT,
                                   self.sum_selected)

            self.hover()

        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.alpha))
            self.display_surface.blit(overlay, (0, 0))
            self.fade()
    