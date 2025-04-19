import pygame
import math
import random
from enum import Enum

# Function to draw a rectangle on the screen
def draw_rectangle(screen: pygame.Surface, topleft_x: int, topleft_y: int, width: int, height: int, colour: tuple[int, int, int]):
    surface = pygame.Surface((width, height))
    surface.fill(colour)
    screen.blit(surface, (topleft_x, topleft_y))

# Player class representing the paddle
class Player():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour

    def render(self, screen):
        draw_rectangle(screen, self.x, self.y, self.width, self.height, self.colour)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    # Update method for player movement left and right
    def update(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.x -= 5  # adjust movement speed as desired
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if self.x < 0:
            self.x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

# Function to check if two rectangles are colliding (Axis-Aligned Bounding Box collision detection)
def is_AABB_colliding(rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
    return rect_a.colliderect(rect_b)

# Function to determine the angle between the center points of two rectangles
def get_angle_between_centre_points(rect_a: pygame.Rect, rect_b: pygame.Rect):
    centre_a = pygame.math.Vector2(rect_a.center)
    centre_b = pygame.math.Vector2(rect_b.center)
    diff = centre_b - centre_a
    return math.degrees(math.atan2(diff.y, diff.x))

class Axis(Enum):
    X = 1
    Y = 2

# Ball class representing the bouncing ball
class Ball():
    def __init__(self, x, y, height, width, velocity_x, velocity_y, image_path):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y)
        # Load the ball's image
        original_surface = pygame.image.load(image_path).convert_alpha()
        self.surface = pygame.transform.scale(original_surface, (self.width, self.height))   

    # Function to update ball position and handle wall collisions
    def update(self, elapsed_seconds):
        self.position += self.velocity * elapsed_seconds
        
        # Wall collisions
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x = -self.velocity.x
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y = -self.velocity.y
        if self.position.x + self.width > 400:
            self.position.x = 400 - self.width
            self.velocity.x = -self.velocity.x

    # Function to reflect the ball's velocity along a given axis
    def reflect(self, axis: Axis):
        if axis == Axis.X:
            self.velocity.x *= -1
        elif axis == Axis.Y:
            self.velocity.y *= -1

    def render(self, screen):
        screen.blit(self.surface, (self.position.x, self.position.y))
    
    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

# Brick class representing the breakable blocks
class Brick():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.is_active = True

    def render(self, screen):
        if self.is_active:
            draw_rectangle(screen, self.x, self.y, self.width, self.height, self.colour)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Display full-screen image
def show_image(screen, image_path):
    image = pygame.image.load(image_path).convert()
    screen.blit(pygame.transform.scale(image, (400, 400)), (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def main():
    # INIT
    player_width = 80
    player_height = 20
    player = Player(160, 380, player_width, player_height, (0, 255, 0))  # Center player horizontally at bottom

    bricks = []
    brick_width = 63
    brick_height = 5
    brick_spacing = 5
    colour_list = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue  
    ]

    for column_index in range(6):
        for row in range(4):  
            a = column_index * (brick_width + brick_spacing)  # Adds a brick for every value of column_index with a gap space of 5 
            b = row * (brick_height + brick_spacing)  # Adds a brick for to every row with a height of 5 and gap space of 5
            colour_index = (row + column_index) % len(colour_list)  # Finds the remainder of 6*3/10 so colours can alternate eg red green blue
            brick_colour = colour_list[colour_index]  # Uses the colours from colour list by finding the index of colour_index from the modulus
            bricks.append(Brick(a, b, brick_width, brick_height, brick_colour))  # Appends the bricks

    pygame.init()
    pygame.mixer.init()  # Initialize sound mixer

    # Load sounds
    collision_sound = pygame.mixer.Sound("sfx_a.wav")
    brick_hit_sound = pygame.mixer.Sound("sfx_b.wav")
    pygame.mixer.music.load("music_a.wav")
    pygame.mixer.music.play(-1)  # Loop background music indefinitely

    # Create window and set caption
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Brick Breaker")  # Set window title

    # Font and timer setup
    font = pygame.font.SysFont("DS-Digital", 26, bold=True)
    neon_green = (57, 255, 20)  # Neon green text color
    clock = pygame.time.Clock()

    # Start screen (shows an image on game start)
    show_image(screen, "start.png")

    running = True
    while running:
        # Reset player, ball at the start of each new game
        player = Player(160, 380, player_width, player_height, (0, 255, 0))
        ball = Ball(195, 350, 25, 25, 100, -100, "swan.png")
        for brick in bricks:
            brick.is_active = True
        score = 0
        game_started = False
        start_ticks = pygame.time.get_ticks()

        keep_playing = True
        while keep_playing:
            elapsed_seconds = clock.tick(60) / 1000  # Time passed in seconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit event
                    keep_playing = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Start the game when space is pressed
                        game_started = True

            keys = pygame.key.get_pressed()
            player.update(keys, 400)

            # Update game elements
            if game_started:
                ball.update(elapsed_seconds)

            # Ball and paddle collision detection
            if is_AABB_colliding(ball.get_rect(), player.get_rect()):
                collision_sound.play()  # Play paddle hit sound
                hit_pos = (ball.position.x + ball.width / 2) - (player.x + player.width / 2)
                normalized_hit_pos = hit_pos / (player.width / 2)
                ball.velocity.x = normalized_hit_pos * 50 + random.uniform(-10, 10)  # Adjust ball angle based on paddle hit position
                ball.velocity.y = -abs(ball.velocity.y)  # Ensure ball bounces upwards

            # Ball and brick collision detection
            for brick in bricks:
                if brick.is_active and is_AABB_colliding(ball.get_rect(), brick.get_rect()):
                    brick.is_active = False  # Brick is no longer active
                    brick_hit_sound.play()  # Play brick hit sound
                    ball.reflect(Axis.Y)  # Ball reflects vertically after hitting the brick
                    score += 1  # Increase score when brick is destroyed

            # Check for game over (ball falls below the screen or all bricks destroyed)
            if ball.position.y > 400 or all(not brick.is_active for brick in bricks):
                keep_playing = False

            # RENDER
            screen.fill((0, 0, 0))  # Clears screen with black
            player.render(screen)
            ball.render(screen)
            for brick in bricks:
                brick.render(screen)

            # Display score and time in neon green, centered
            time_played = int((pygame.time.get_ticks() - start_ticks) / 1000)  # Time played in seconds
            string_score = font.render(f"Score: {score}", True, neon_green)  # Score text
            string_time= font.render(f"Time: {time_played}s", True, neon_green)  # Time text
            # Positioning score and time in the center of the screen
            screen.blit(string_score, ((400 - string_score.get_width()) // 2, 200 - string_score.get_height()))  # Center score vertically and horizontally
            screen.blit(string_time, ((400 - string_time.get_width()) // 2, 200))  # Center time vertically and horizontally

            pygame.display.flip()  # Update the display

        # Game over screen (shows an image after game over)
        show_image(screen, "gameover.png")

    pygame.quit()  # Quit pygame when loop ends

if __name__ == "__main__":
    main()  # Run the main game loop
