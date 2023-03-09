import pygame

class Map():
    def __init__(self, game, file_name):
        self.game = game
        self.tile_size = 16
        self.collidable_rects = []
        self.file_name = file_name
        
        # Load map data from file
        with open(file_name) as f:
            self.data = [line.split() for line in f]

        # Load tile images
        self.grassblk_image = pygame.image.load('graphics/tiles/Day-Platformer/PNG/dp_tiles/grss_blk.png').convert_alpha()
        self.drtblk1_image = pygame.image.load('graphics/tiles/Day-Platformer/PNG/dp_tiles/drt_blk1.png').convert_alpha()
        self.drtblk2_image = pygame.image.load('graphics/tiles/Day-Platformer/PNG/dp_tiles/drt_blk2.png').convert_alpha()
        self.background_image = pygame.image.load('graphics/tiles/Day-Platformer/PNG/background/sky.png').convert_alpha()

    def get_collidable_rects(self):
        # Create rect objects for each collidable tile
        collisions = []
        for row_index, row in enumerate(self.data):
            for col_index, col in enumerate(row):
                if col != '0':
                    rect = pygame.Rect(col_index * self.tile_size, row_index * self.tile_size, self.tile_size, self.tile_size)
                    collisions.append(rect)
        return collisions

    def vertical_collisions(self, Player_rect):
        # Check for collisions in the vertical direction
        collisions = []
        for obj in self.get_collidable_rects():
            if Player_rect.colliderect(obj):
                collisions.append(obj)

        # Adjust player position to resolve collisions
        for collision in collisions:
            # Moving down (hitting the top of the object)
            if Player_rect.bottom > collision.top and Player_rect.top < collision.top:
                Player_rect.bottom = collision.top
            # Moving up (hitting the bottom of the object)
            elif Player_rect.top < collision.bottom and Player_rect.bottom > collision.bottom:
                Player_rect.top = collision.bottom

    def horizontal_collisions(self, Player_rect):
        # Check for collisions in the horizontal direction
        collisions = []
        for obj in self.get_collidable_rects():
            if Player_rect.colliderect(obj):
                collisions.append(obj)

        # Adjust player position to resolve collisions
        for collision in collisions:
            # Moving right (hitting the left side of the object)
            if Player_rect.right > collision.left and Player_rect.left < collision.left:
                Player_rect.right = collision.left
            # Moving left (hitting the right side of the object)
            elif Player_rect.left < collision.right and Player_rect.right > collision.right:
                Player_rect.left = collision.right
                
    def update(self, delta_time, Player_rect):
        self.vertical_collisions(Player_rect) 
        self.horizontal_collisions(Player_rect) 
        self.render(self.game.display_surface)
        return Player_rect

    def render(self, display):
        # Draw the tiles according to map data
        for row_index, row in enumerate(self.data):
            for col_index, col in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if col == '1':
                    display.blit(self.grassblk_image, (x, y))
                elif col == '2':
                    display.blit(self.drtblk1_image, (x, y))
                elif col == '3':
                    display.blit(self.drtblk2_image, (x, y))