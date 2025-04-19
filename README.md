# Brick-Breaker
A classic 80's game made using pygame

## Project Overview
-This is the first game I've ever made with Pygame. 

-When the code is executed a display is outputted with a "START NEW GAME" window and the game waits for the end user to press space to start the game
- Then a rectangular paddle is used to collide a sprite to hit the "bricks" whilst the score is updated after every collision with the bricks
- Whilst this happens the time taken is outputted
- For each collision there is a sound effect for a more streamlined gameplay experience
- Whilst the game is running music is played
  
##Project Pros:
-Interactive Gameplay: The user can control a paddle to interact with the ball and break bricks.

-Sound Effects: Incorporates sound effects for collisions and background music to enhance the gaming experience.

-Graphics: Simple yet effective 2D graphics, including sprites for the ball and images for start and game over screens.

-Game Mechanics: Features dynamic ball reflection and different colors for the bricks to add variety to the visual appeal.

##Project Cons:
-Limited Difficulty Scaling: The game could benefit from increasing difficulty levels as the player progresses (e.g., faster ball speed or more complex brick layouts).

-Minimalistic UI: The game could have additional menus for settings or difficulty selection.

-No Save System: The game doesn't store the player's score across sessions.

- Score is not saved which could be improved with high scores too

- Score is not outputted after every game

##Features:
Paddle Movement: The player moves a paddle left or right to keep the ball in play.

Brick Destruction: Bricks are destroyed when the ball collides with them.

Sound Effects: Includes sound for paddle hits, brick destruction, and background music.

Score and Time Tracking: Displays the score and the time played during the game.

Collision Detection: The game uses Axis-Aligned Bounding Box (AABB) for detecting collisions between the ball and bricks or the paddle.

##How it works:
- The relevant modules are imported: 
- To draw a shape there is a fucntion called "draw_rectangle" with parameters for its dimensions, including the pygame.Surface object and it is needed to render the shapes such as the blocks
-The ball, brick and paddle are defined as classes with multiple functions. Each have attributes for their particular functions. For example, the "Player()" class a consrtructor, with parameters
for its dimensions which uses the "draw_rectangle" function to draw the paddle. The update function allows the end user to move the paddle left and right.
- is_AAB_colliding is used to check if the ball hits the blocks.
- The Axis Enum class defines the X and Y axes, which are used for reflecting the ball's velocity when it collides with the paddle or a brick.
- Purpose: The Ball class represents the ball in the game and has the following attributes:
-   x, y: The initial position of the ball. height, width: The size of the ball.
-   velocity_x, velocity_y: The velocity (speed) of the ball in both X and Y directions.
-   position: The current position of the ball, represented as a Vector2 object (to handle 2D movement).
-   surface: The ball's image surface, loaded and scaled to the ball's dimensions.
-   This is used to control the speed of the ball etc
-   The reflect function is used to do just that when the ball collides with the bricks
-   The render function draws the ball on the screen
-   The same thing is done to draw the bricks on screen, more or less
-   Show_image loads the start screen and I used a while loop so the screen is shown until the player presses space
-   Finally the main() function is the core of the game. It initializes the game objects, handles user input, updates game elements (like the ball and player), checks for collisions, and renders everything to the screen.
-   The game uses a loop to repeatedly update and render the screen until the game is over or the user quits.


Technologies Used:
Python: The programming language used to develop the game.

Pygame: A set of Python modules designed for creating video games. It handles graphics, sound, and input.

Sound: The game uses pygame.mixer to handle sound effects and background music.

How to Use:
Install Pygame:
Run pip install pygame to install the necessary dependencies.

Clone the project:
Download the Python script and necessary image and sound files.

Run the game:
Execute the script, and it will open a game window where you can play.

Controls:

Arrow keys to move the paddle left and right.

Spacebar to start the game.

Game Over:
After either losing or completing all levels, the game will show a "Game Over" screen and you can restart.

Contributing:
If you'd like to contribute, feel free to fork the repository and submit a pull request with improvements or bug fixes.

Contact:
Email: kallamsamad@gmail.com

GitHub: KallamSamad GitHub
