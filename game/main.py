import pygame, sys
from settings import *
from debug import debug
from level import Level
from intro import Intro

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Learning with AI')
        self.clock = pygame.time.Clock()
        
        # Set to 'play' while creating control panel
        self.state = 'intro'
        self.intro = Intro()
        self.level = None  #Initialise after intro finishes

        # sound
        self.main_sound = pygame.mixer.Sound('audio/main.ogg')
        self.main_sound.set_volume(0.3)
        self.main_sound.play(loops = -1)
        self.pos = None

        # tome
        self.tome_open = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if self.state == 'intro':
                    self.intro.input(event)

                elif self.state == 'play':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.level.toggle_menu()
                        
                        elif event.key == pygame.K_c:
                            self.level.toggle_controls()
                        
                        elif event.key == pygame.K_k:
                            if self.level.tome and self.level.tome.discuss_text == "Leave" or self.level.tome.test_text == "Leave":
                                pass
                            else:
                                self.tome_open = not self.tome_open
                                if self.tome_open:
                                    pygame.mixer.pause()
                                else:
                                    pygame.mixer.unpause()
                                self.level.toggle_tome()


                    if self.level.open_tome:
                        self.level.tome.mouse(event)
                    
                    elif self.level.summarise:
                        self.level.summary.mouse(event)
                
            self.screen.fill(WATER_COLOR)
            if self.state == 'intro':
                self.intro.run()
                if self.intro.state == 'play':
                    self.state = 'play'
                    self.level = Level()
            else:
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()