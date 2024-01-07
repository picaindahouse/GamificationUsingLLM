import pygame
from settings import *
from creation import Creation
from llm import LLM


class Intro:
    def __init__(self):

        # General
        self.display_surface = pygame.display.get_surface()
        self.title = pygame.font.Font(UI_FONT, 36)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # State
        self.state = 'start'

        # Blink
        self.text_visibility = True
        self.blink_timer = 0
        self.blink_interval = 500 # milliseconds

        # Save Dimensions
        self.width = self.display_surface.get_size()[0] * 0.8
        self.height = self.display_surface.get_size()[1] // 5
        self.create_saves()

        # Choose
        self.selection_index = 0
        self.can_move = True
        self.selection_time = None
        self.saves = list(saved_files.values())

        # Creation
        self.creation = Creation()

        # Questions
        self.questions_asked = 0
        self.openai = LLM(introduction_system)
        self.question = self.openai.ask_chatgpt("Introduce Yourself", MAX_TOKENS)

    def intro(self):
        # Font settings
        intro_text = "Learning with AI!"
        text_render = self.title.render(intro_text, False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] // 2
        y = 45
        text_rect = text_render.get_rect(center=(x, y))

        # Draw Background
        floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        floor_rect = floor_surf.get_rect(topleft = (-1335, 100))
        self.display_surface.blit(floor_surf, floor_rect)

        # Display intro text
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_render, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)

        if self.state == 'start':
            
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_timer > self.blink_interval:
                self.text_visibility = not self.text_visibility
                self.blink_timer = current_time
            
            if self.text_visibility:
                start_text = 'PRESS ENTER TO START!'
                self.draw_words(start_text, x,
                                self.display_surface.get_size()[1] - 80,
                                UI_BORDER_COLOR)

        elif self.state == 'choose':
            for index, save in enumerate(self.save_list):
                # Get Attributes:
                name = self.saves[index]

                # Create display
                save.display(self.display_surface, self.selection_index, name)

        elif self.state == 'creation':
            tran_height = self.display_surface.get_size()[1] * 0.7
            tran_width = self.display_surface.get_size()[0] * 0.7
            semi_transparent_rect = pygame.Surface((tran_width, 
                                                    tran_height),
                                                    pygame.SRCALPHA)
            pygame.draw.rect(semi_transparent_rect,
                             (100, 100, 100, 208),
                             semi_transparent_rect.get_rect(),
                             border_radius=10)
            
            tran_x = (self.display_surface.get_size()[0] - tran_width) // 2
            tran_y = 65 + (self.display_surface.get_size()[1] - 65) // 2 - tran_height //2
            
            self.display_surface.blit(semi_transparent_rect, (tran_x, tran_y))

            if self.creation.ready_for_qn:
                if len(self.creation.chat_history) > self.questions_asked:
                    self.questions_asked += 1
                    self.question = self.openai.ask_chatgpt(self.creation.chat_history[-1], MAX_TOKENS)
                    
                    if self.question[-9:].upper().replace(' ', '') == 'HAVEFUN!':
                        findings = self.openai.ask_chatgpt('Summarise your findings in a list as specified, do not add anything else. Do not need create new lines.', MAX_TOKENS)
                        for i, finding in enumerate(findings.split(', ')):
                            user_info[list(user_info.keys())[i]] = finding
                        print(user_info)
                        self.state = 'play'

            if self.state == 'creation':
                self.creation.ask_question(self.question, tran_width - 100, self.questions_asked)

    def input(self, event):
        if self.state == 'creation':
            self.creation.reply(event)
        else:
            if event.type == pygame.KEYDOWN:
                if self.can_move:
                    if event.key == pygame.K_UP and self.selection_index > 0:
                        self.selection_index -= 1
                        self.can_move = False
                        self.selection_time = pygame.time.get_ticks()

                    elif event.key == pygame.K_DOWN and self.selection_index < 2:
                        self.selection_index += 1
                        self.can_move = False
                        self.selection_time = pygame.time.get_ticks()
                    
                    if event.key == pygame.K_RETURN:
                        if self.state == 'start':
                            self.state = 'choose'
                        else:
                            self.can_move = False
                            self.selection_time = pygame.time.get_ticks()
                            triggered = self.save_list[self.selection_index].trigger()
                            if triggered in ['creation', 'play']:
                                self.state = triggered

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def draw_words(self, text, x, y, color):
        surf = self.font.render(text, False, color)
        rect = surf.get_rect(center = pygame.math.Vector2(x, y))
        self.display_surface.blit(surf, rect)

    def create_saves(self):
        self.save_list = []

        for item, index in enumerate(range(3)):
            # horizontal position
            left = self.display_surface.get_size()[0] * 0.1

            # vertical position
            full_height = self.display_surface.get_size()[1]
            increment = full_height // 5
            top = (item * increment) + (increment - self.height) // 2 + 175

            # create the object
            save = Save(left, top, self.width, self.height, index, self.font)
            self.save_list.append(save)

    def run(self):
        self.selection_cooldown()
        self.intro()

class Save:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
        self.name = 'Empty Save'
        self.mistrigger = False

        # Mistake Timer:
        self.mistrigger_time = None
        self.timer = 400

    def display_names(self, surface, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        name = 'save ' + str(self.index + 1)

        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)
    
    def display_bar(self, surface, selected, name):
        self.name = name
        
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)

        if self.name == 'Empty Save':
            color = BAR_COLOR_SELECTED if selected else BAR_COLOR

            # bar setup
            value_rect = pygame.Rect(top[0] - 15, bottom[1], 30, 10)

            # draw elements
            pygame.draw.rect(surface, color, value_rect)
        
        else:
            color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
            surf = self.font.render(name, False, color)
            rect = surf.get_rect(center =  pygame.math.Vector2(self.rect.centerx, bottom[1]))
            surface.blit(surf, rect)

    def trigger(self):
        if self.name == 'Empty Save':
            self.mistrigger = True
            self.mistrigger_time = pygame.time.get_ticks()
            return 'Empty Save'
        else:
            return 'creation'
            #return 'play'

    def display(self,surface, selection_num, name):
            current_time = pygame.time.get_ticks()
            if self.mistrigger and current_time - self.mistrigger_time > self.timer:
                self.mistrigger = False

            if self.mistrigger:
                pygame.draw.rect(surface,RED,self.rect)
                pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
            elif self.index == selection_num:
                pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
                pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
            else:
                pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
                pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        
            self.display_names(surface, self.index == selection_num)
            self.display_bar(surface, self.index == selection_num, name)
