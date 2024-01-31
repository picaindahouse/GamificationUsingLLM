import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from control import Control
from tome import Tome
from tutorial import Tutorial
from summary import Summary

class Level:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.get_controls = True
        self.open_tome = False
        self.summarise = False

        # Sprite Group Setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Tutorial
        self.tutorial_enable = True
        self.tutorial = Tutorial()

        # Sprite Setup
        self.enable = 'yes' in user_info["enable_enemies"].lower()
        self.create_map()

        # User Interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.control = Control()
        self.tome = Tome()
        self.summary = Summary()

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            'map': import_csv_layout('map/game_map.csv'),
            # Testing out scroll
            'entities': import_csv_layout('map/map_Entities_scroll.csv')
        }
        
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/objects'),
            'pages' : import_folder('graphics/scroll')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col not in ['-1', '-5']:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'map':
                            if int(col) < 21:
                                type = 'object'
                                group = [self.visible_sprites, self.obstacles_sprites]
                                surface = graphics['objects'][int(col)]

                            elif col == '21':
                                type = 'grass'
                                group = [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites]
                                surface = choice(graphics['grass'])
                            else:
                                type = 'invisible'
                                group = [self.obstacles_sprites]
                                surface = pygame.Surface((TILESIZE, TILESIZE))

                            Tile((x, y), group, type, surface)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x,y), 
                                                    [self.visible_sprites], 
                                                    self.obstacles_sprites, 
                                                    self.create_attack, self.destroy_attack, self.create_magic)
                            elif col == '400':
                                group = [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites]
                                surface = choice(graphics['pages'])
                                Tile((x, y), group, 'page', surface)

                            else:
                                if col == '390': 
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                if self.enable and not self.tutorial_enable:
                                    Enemy(monster_name,
                                        (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacles_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_xp)
    
    def create_new_day(self):
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/objects'),
            'pages' : import_folder('graphics/scroll')
        }

        # Kill old sprites:
        for sprite in self.attackable_sprites:
            if sprite.sprite_type == 'enemy':
                sprite.kill()

        # Testing out scroll
        layout = import_csv_layout('map/map_Entities_scroll.csv')
        have_page = False
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col not in ['-1', '-5']:
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    if col == '394':
                        self.player.rect.center = (x, y)
                        self.player.hitbox.center = (x, y)
                        if len(self.tome.found_pages) > 2:
                            self.player.next_day()

                    elif col == '400' and not have_page:
                        group = [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites]
                        surface = choice(graphics['pages'])
                        Tile((x, y), group, 'page', surface)
                        have_page = True

                    else:
                        if col == '390': 
                            monster_name = 'bamboo'
                        elif col == '391':
                            monster_name = 'spirit'
                        elif col == '392':
                            monster_name = 'raccoon'
                        else:
                            monster_name = 'squid'

                        if self.enable and not self.tutorial_enable:
                            Enemy(monster_name,
                                (x,y),
                                [self.visible_sprites, self.attackable_sprites],
                                self.obstacles_sprites,
                                self.damage_player,
                                self.trigger_death_particles,
                                self.add_xp,
                                len(self.tome.found_pages))

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def tut(self):
        if self.get_controls:
            self.tutorial.control()
        else:
            if len(self.tome.found_pages) == 2:
                self.tutorial.found()
                self.tutorial.input()
            else:
                self.tutorial.find()

        if self.tutorial.end:
            self.tutorial_enable = False
            self.create_new_day()

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # List of all attackable sprites that attack_sprites have collided with:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,
                                                                self.attackable_sprites,
                                                                False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()

                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                        
                        elif target_sprite.sprite_type == 'page':
                            self.tome.found_page()
                            self.summarise = True
                            target_sprite.kill()
    
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            
            # spawn particles
            pos = self.player.rect.center
            self.animation_player.create_particles(attack_type, pos, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])
    
    def add_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        if not self.get_controls and not self.open_tome:
            self.game_paused = not self.game_paused

    def toggle_controls(self):
        if not self.game_paused and not self.open_tome:
            self.get_controls = not self.get_controls

    def toggle_tome(self):
        if self.summarise:
            self.summarise = False
            self.summary.reset()
        elif not self.game_paused and not self.get_controls:
            if not self.open_tome:
                self.tome.reset()
            self.open_tome = not self.open_tome
        
    def run(self):
        # Update and Draw the Game
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player, self.tome)

        if self.game_paused:
            # display upgrade menu
            self.upgrade.display()
        
        elif self.get_controls:
            self.control.display()
            if self.tutorial_enable:
                self.tut()

        elif self.open_tome:
            self.tome.open()
            if self.tome.next_day == True:
                self.create_new_day()
                self.tome.reset()
                self.open_tome = False
        
        elif self.summarise:
            self.summary.summarise(self.tome.found_pages)

        else:
            # run the game
            if self.tutorial_enable:
                self.tut()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creating the Floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)