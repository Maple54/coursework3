import pygame
from pygame.math import Vector2 as vec



class Player():
    def __init__(self, game):
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()  # rect attribute for collision detection

        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.direction = vec(0, 0)        
        self.current_frame, self.last_frame_update = 0, 0

   
    def get_input(self, actions):
        if actions['right']:
            self.direction.x = 1 
        elif actions['left']:
            self.direction.x = -1 
        else:
            self.direction.x = 0
        if actions['up']:
            self.jump()

    def jump(self):
      self.direction.y = self.jump_speed

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y   


    def update(self, delta_time, actions):
        # Get the direction from inputs
        self.get_input(actions)
        self.apply_gravity()
        self.rect.x += self.direction.x * self.speed * delta_time

    def render(self, display):
        display.blit(self.image, self.rect)
   
       
