import pgzrun
import random

# --- Game Setup ---
WIDTH = 800
HEIGHT = 500
TITLE = "Awesome Platformer"

# --- Player Variables ---
player = Rect(100, 400, 40, 40)
velocity_y = 0
gravity = 1.2
on_ground = False
jump_strength = -18
player_speed = 6

# --- Game State Variables ---
score = 0
lives = 3
game_over = False
win_condition_met = False
level = 1

# --- Collectible Variables ---
coins = []
gems = []

# --- Hazard Variables ---
moving_platform_hazard = None
moving_platform_hazard_speed = 2
moving_platform_hazard_direction = 1

# --- Enemy Variables ---
enemies = []
enemy_speed = 2
enemy_direction = [] # Will be populated per level

# --- Platform Variables ---
platforms = []

# --- Goal Variable ---
# This MUST be initialized to a value that signifies "no goal yet" or a default.
# A placeholder Rect is good, or None if you handle None checks carefully everywhere.
# Let's initialize it to None.
goal = None

# --- Level Data ---
levels = [
    { # Level 1
        "platforms": [
            Rect(0, HEIGHT - 30, WIDTH, 30), Rect(200, 380, 150, 20), Rect(450, 300, 150, 20),
            Rect(650, 220, 100, 20), Rect(300, 250, 80, 15), Rect(500, 180, 120, 15)
        ],
        "coins": [
            Rect(250, 340, 20, 20), Rect(500, 260, 20, 20), Rect(690, 180, 20, 20),
            Rect(330, 220, 20, 20), Rect(550, 150, 20, 20)
        ],
        "gems": [
            Rect(470, 270, 18, 18)
        ],
        "hazards": [
            Rect(350, HEIGHT - 30, 100, 20), # Lava on ground
            Rect(600, 350, 80, 15) # Moving platform hazard
        ],
        "enemies": [
            Rect(220, HEIGHT - 50, 30, 30), Rect(500, 270, 30, 30),
        ],
        "goal": Rect(WIDTH - 50, HEIGHT - 50, 30, 30)
    },
    { # Level 2
        "platforms": [
            Rect(0, HEIGHT - 30, WIDTH, 30), Rect(150, 400, 120, 20), Rect(300, 350, 120, 20),
            Rect(450, 300, 120, 20), Rect(600, 250, 120, 20), Rect(750, 200, 100, 20)
        ],
        "coins": [
            Rect(180, 370, 20, 20), Rect(330, 320, 20, 20), Rect(480, 270, 20, 20),
            Rect(630, 220, 20, 20), Rect(780, 170, 20, 20)
        ],
        "gems": [
            Rect(310, 320, 18, 18), Rect(580, 220, 18, 18)
        ],
        "hazards": [
            Rect(370, HEIGHT - 30, 80, 20), # Lava
            Rect(200, 370, 50, 15),       # Small, deadly platform
            Rect(550, 270, 50, 15)        # Small, deadly platform
        ],
        "enemies": [
            Rect(250, 370, 30, 30), Rect(400, 320, 30, 30),
            Rect(500, 270, 30, 30), Rect(700, 170, 30, 30)
        ],
        "goal": Rect(WIDTH - 50, 170, 30, 30)
    }
]

# --- Global variables that will be set by load_level ---
current_moving_hazard_rect = None

def load_level(level_index):
    """Loads data for a specific level. Returns the goal Rect or None if game finished."""
    global platforms, coins, gems, hazards, enemies, player, goal
    global current_moving_hazard_rect, moving_platform_hazard_speed, moving_platform_hazard_direction
    global enemy_direction

    if level_index >= len(levels):
        return None # Indicates game completion

    level_data = levels[level_index]

    platforms = level_data["platforms"]
    coins = level_data["coins"]
    gems = level_data["gems"]
    hazards = level_data["hazards"]
    enemies = level_data["enemies"]
    
    # Crucially, assign to the global 'goal' variable here
    goal = level_data["goal"]

    # Reset player position for the new level
    player.x = 100
    safe_y = HEIGHT - 100
    for plat in platforms:
        if player.colliderect(plat):
            safe_y = min(safe_y, plat.top - player.height)
    player.y = max(safe_y, 0)
    velocity_y = 0
    on_ground = False

    # Initialize enemy directions
    enemy_direction = [1] * len(enemies)

    # Handle the moving platform hazard
    current_moving_hazard_rect = None
    moving_platform_hazard_speed = 2
    moving_platform_hazard_direction = 1
    
    for hazard in hazards:
        # Simple identifier for the moving hazard (adjust if needed)
        if hazard.x == 600 and hazard.y == 350 and hazard.width == 80:
            current_moving_hazard_rect = hazard
            break

    return goal # Return the goal for the current level

def draw():
    """This function draws things on the screen."""
    screen.clear()
    screen.fill("skyblue")

    for platform in platforms:
        screen.draw.filled_rect(platform, (34, 139, 34))

    for coin in coins:
        screen.draw.filled_rect(coin, "yellow")
    for gem in gems:
        screen.draw.filled_rect(gem, "purple")

    for hazard in hazards:
        if hazard != current_moving_hazard_rect:
            screen.draw.filled_rect(hazard, "red")

    if current_moving_hazard_rect:
        screen.draw.filled_rect(current_moving_hazard_rect, "darkred")

    for enemy in enemies:
        screen.draw.filled_rect(enemy, "black")

    # Draw the goal ONLY if it's been assigned a value (i.e., not None)
    if goal:
        screen.draw.filled_rect(goal, "gold")

    screen.draw.filled_rect(player, "blue")

    screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Lives: {lives}", (WIDTH - 100, 10), fontsize=30, color="white")
    screen.draw.text(f"Level: {level}", (WIDTH // 2 - 40, 10), fontsize=30, color="white")

    if win_condition_met:
        screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="gold")
        screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")
    elif game_over:
        screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")

def update():
    """This function updates the game over and over."""
    global velocity_y, on_ground, score, lives, game_over, win_condition_met, level
    global current_moving_hazard_rect, moving_platform_hazard_speed, moving_platform_hazard_direction
    global enemy_direction, goal # Ensure goal is declared global here too for modification

    if game_over or win_condition_met:
        if keyboard.r:
            reset_game()
        return

    # --- Player Movement ---
    if keyboard.left: player.x -= player_speed
    if keyboard.right: player.x += player_speed

    if player.left < 0: player.left = 0
    if player.right > WIDTH: player.right = WIDTH

    # --- Gravity and Vertical Movement ---
    velocity_y += gravity
    player.y += velocity_y

    # --- Ground and Platform Collision ---
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform):
            if velocity_y > 0:
                player.bottom = platform.top
                velocity_y = 0
                on_ground = True
            elif velocity_y < 0:
                player.top = platform.bottom
                velocity_y = 0

    # --- Jumping ---
    if keyboard.space and on_ground:
        velocity_y = jump_strength
        on_ground = False

    # --- Falling off screen ---
    if player.bottom > HEIGHT:
        lose_life()
        return

    # --- Collectibles Collision ---
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 5

    for gem in gems[:]:
        if player.colliderect(gem):
            gems.remove(gem)
            score += 20

    # --- Hazard Collision ---
    for hazard in hazards:
        if hazard != current_moving_hazard_rect:
            if player.colliderect(hazard):
                lose_life()
                return

    # --- Moving Platform Hazard Logic ---
    if current_moving_hazard_rect:
        current_moving_hazard_rect.x += moving_platform_hazard_speed * moving_platform_hazard_direction
        if current_moving_hazard_rect.left < 550 or current_moving_hazard_rect.right > 750:
            moving_platform_hazard_direction *= -1
            current_moving_hazard_rect.x += moving_platform_hazard_speed * moving_platform_hazard_direction

        if player.colliderect(current_moving_hazard_rect):
            lose_life()
            return

    # --- Enemy Logic ---
    for i, enemy in enumerate(enemies):
        enemy.x += enemy_speed * enemy_direction[i]
        
        collided_with_platform_edge = False
        on_platform = False
        for platform in platforms:
            if enemy.colliderect(platform):
                if enemy.bottom - enemy_speed < platform.top < enemy.bottom: # Falling onto platform
                    enemy.bottom = platform.top
                    on_platform = True
                    break
                elif (enemy.right > platform.left and enemy.right - enemy_speed < platform.left) or \
                     (enemy.left < platform.right and enemy.left + enemy_speed > platform.right):
                    collided_with_platform_edge = True
                    break

        if collided_with_platform_edge or enemy.left < 0 or enemy.right > WIDTH:
            enemy_direction[i] *= -1
            enemy.x += enemy_speed * enemy_direction[i]
            
        # Enemy Collision with Player
        if player.colliderect(enemy):
            if velocity_y > 0 and player.bottom - velocity_y < enemy.top: # Player stomping
                del enemies[i]
                del enemy_direction[i]
                score += 50
                velocity_y = -10
                on_ground = False
                break # Exit enemy loop, list modified
            else: # Player hit from side/below
                lose_life()
                return

    # --- Goal Collision ---
    # CRITICAL: This line relies on 'goal' being defined.
    # The global 'goal' in update() is needed because load_level assigns to it.
    if goal and player.colliderect(goal):
        if not coins and not gems:
            level += 1
            new_goal = load_level(level - 1)
            if new_goal is None: # All levels completed
                win_condition_met = True
            else:
                goal = new_goal # Re-assign goal for the new level
        else:
            screen.draw.text("Collect all items first!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=40, color="orange")


def lose_life():
    """Handles player losing a life."""
    global lives, game_over, player, velocity_y, on_ground, goal # Ensure goal is global here too
    
    lives -= 1
    if lives <= 0:
        game_over = True
    else:
        # Reload the current level
        goal = load_level(level - 1) # Important: reload level and reassign goal
        # Player reset happens inside load_level

def reset_game():
    """Resets all game variables to their initial state."""
    global player, velocity_y, on_ground, score, lives, game_over, win_condition_met, level
    global coins, gems, hazards, enemies, platforms, goal, enemy_direction, current_moving_hazard_rect

    player = Rect(100, 400, 40, 40)
    velocity_y = 0
    on_ground = False
    score = 0
    lives = 3
    game_over = False
    win_condition_met = False
    level = 1

    enemy_direction = []
    current_moving_hazard_rect = None

    # Load the first level
    goal = load_level(level - 1)


# --- Initialization ---
goal = load_level(level - 1) # Initial load of the first level

pgzrun.go()