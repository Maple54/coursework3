import pygame,os
from states import State
from pygame.math import Vector2 as vec
from map import Map





class main_game(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.player = Player(self.game)
        self.game_map = Map(self.game,"Map.txt")


        
                
    def update(self, delta_time, actions):
      self.player.update(delta_time, actions)
      self.game_map.update(delta_time,Player)

      
    def render(self, display):
       display.fill('red')
       self.game_map.render(display)
       self.player.render(display)
      


class Player():
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.rect = self.curr_anim_list[0].get_rect()  # rect attribute for collision detection
        self.position = vec(0,0)
        self.speed = 6
        self.gravity = 0.5
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
        self.position += self.direction * self.speed * delta_time
        self.rect.centerx = self.position.x 
        self.rect.bottom = self.position.y  
        self.animate(delta_time,self.direction.x,self.direction.y)
        


    def render(self, display):
        display.blit(self.curr_image, self.rect)
    

    def animate(self, delta_time, direction_x, direction_y):
         # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not (self.direction.x or self.direction.y):
            self.curr_image = self.curr_anim_list[0]

            return  
         # If an image was pressed, use the appropriate list of frames according to direction
        if self.direction.x > 0: 
            self.curr_anim_list = self.run_right_sprites
        elif self.direction.x < 0:
            self.curr_anim_list = self.run_left_sprites
        else:
            self.curr_anim_list = self.idle_sprites
           # Playing run animation if enough time has elapsed
        if self.curr_anim_list != self.idle_sprites:
            if self.last_frame_update > .15:
                self.last_frame_update = 0
                self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
                self.curr_image = self.curr_anim_list[self.current_frame]
        else:
            self.curr_image = self.idle_sprites[self.current_frame]


       
    def load_sprites(self): 
        self.sprite_dir = os.path.join(os.getcwd(), "graphics", "sprites","bunny")

        self.idle_sprites, self.run_right_sprites, self.run_left_sprites = [],[],[]

        for i in range(1, 7):
            self.run_right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "run" + str(i) + ".png")))
        for i in range(1, 4):
            self.idle_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "idle" + str(i) + ".png")))
            
        self.run_left_sprites = [pygame.transform.flip(img, True, False) for img in self.run_right_sprites]       
       


        
        self.curr_image = self.idle_sprites[0]
        self.curr_anim_list = self.idle_sprites      
            
