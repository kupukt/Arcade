from os import remove
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "FireFall"
SCALING = 1.0
GRAVITY = 5

class FireFall(arcade.Window):
    
    # Class to handle the game
    

    def __init__(self, width, height, title):
        """Initialize the game
        """
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.fire_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        # Get the game ready to play
        

        # Set the background color
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Set up the player
        self.player = arcade.Sprite("images/firefighter.png")
        self.player.center_y = 90
        self.player.left = 400
        self.all_sprites.append(self.player)

        platform = arcade.Sprite("images/ice_platform.png")

        platform.center_y = self.height - (self.height)
        platform.left = 200
        platform.velocity = (0,0)
        self.all_sprites.append(platform)
        self.platform_list.append(platform)

        arcade.schedule(self.add_fire, 1.0)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY
        )

        self.paused = False
    
    def add_fire(self, delta_time: float):
       

        # Create the new fire sprite
        fire = MovingSprites("images/fireball.png")

        # Set its position to a random location off the top of the screen.
        fire.left = random.randint(0, self.width)
        fire.top = random.randint(self.height, self.height + 30)

        fire.velocity = ((random.randint(-100,100)) , (random.randint(-200, -50 )))

        self.fire_list.append(fire)
        self.all_sprites.append(fire)

    def add_platform(self, delta_time: float):

        platform = arcade.Sprite("images/ice_platform.png", SCALING)

        platform.center_y = self.height / 2
        platform.left = 10
        platform.velocity = (0,0)
        self.all_sprites.append(platform)
        self.platform_list.append(platform)
      

    def on_key_press(self, key: int, modifiers: int):
        
        if key == arcade.key.Q:
          
            arcade.close_window()

        if key == arcade.key.P:
            self.paused = not self.paused

        if key == arcade.key.W or key == arcade.key.UP:
            self.player.change_y = 350
            

        if key == arcade.key.S or key == arcade.key.DOWN:
            self.player.change_y = -350
            

        if key == arcade.key.A or key == arcade.key.LEFT:
            self.player.change_x = -350

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.change_x = 350

    def on_key_release(self, key: int, modifiers: int):
        
        if (
            key == arcade.key.W
            or key == arcade.key.S
            or key == arcade.key.UP
            or key == arcade.key.DOWN

        ):
            self.player.change_y = GRAVITY

        if (
            key == arcade.key.A
            or key == arcade.key.D
            or key == arcade.key.LEFT
            or key == arcade.key.RIGHT
        ):
            self.player.change_x = 0
    
    def on_update(self, delta_time: float):
     
        # Check if player collides with fire, if so, remove the fire.
        check_fire_collision = arcade.check_for_collision_with_list(self.player, self.fire_list)
        for fire in check_fire_collision:
            fire.remove_from_sprite_lists()
        
        
        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        

        # Keep player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
       
        arcade.start_render()
        self.all_sprites.draw()

    

class MovingSprites(arcade.Sprite):

    def update(self):
        

        # Move the sprite
        super().update()

        # Remove us if we're off screen
        if self.top > self.height + 50:
            self.remove_from_sprite_lists()
        elif self.right > self.width + 50:
            self.remove_from_sprite_lists()
        elif self.left < 0:
            self.remove_from_sprite_lists()
        elif self.bottom < 0:
            self.remove_from_sprite_lists()


if __name__ == "__main__":
    
    game = FireFall(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    
    game.setup()
   
    arcade.run()
