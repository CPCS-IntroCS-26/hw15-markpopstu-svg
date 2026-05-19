[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vXTjOAz_)
# Python Platformer Project

## Project Overview

In this project, you will build a simple 2D platformer game in Python using **Pygame Zero**.

A platformer is a game where the player moves left and right, jumps, lands on platforms, avoids hazards, collects items, and tries to reach a goal.

You will start with a basic player and gradually add more game features. By the end, your game should feel like a small but complete platformer level.

---

## What You Will Learn

By completing this project, you will practice:

- Creating a game window
- Drawing game objects on the screen
- Moving a player with the keyboard
- Using variables to track position and speed
- Adding gravity
- Making a player jump
- Creating platforms
- Detecting collisions
- Adding collectibles and score
- Adding hazards
- Creating a goal or win condition
- Organizing code so it is easier to understand

---

## Before You Begin

This project uses **Pygame Zero**.

Please run
```python

pip install pgzero

```

A Pygame Zero program usually has two important functions:

```python

def draw():
    # This function draws things on the screen
    pass


def update():
    # This function updates the game over and over
    pass
```

The `draw()` function controls what the player sees.

The `update()` function controls what changes while the game is running.

---

# Step 1: Create the Game Window

The first thing every game needs is a window.

Create two variables for the size of your game screen:

```python
WIDTH = 800
HEIGHT = 500
```

These numbers tell Python how wide and tall the game window should be.

Next, create a simple `draw()` function:

```python
def draw():
    screen.clear()
```

At this point, your game may not look very exciting yet. That is normal. You are setting up the space where your game will happen.

### Think About It

- What does `WIDTH` control?
- What does `HEIGHT` control?
- Why do games need to redraw the screen many times?

---

# Step 2: Create the Player

Your player needs to appear on the screen.

For now, your player can be a rectangle. Later, you may replace it with an image or sprite.

Create a player rectangle:

```python
player = Rect((100, 400), (40, 40))
```

This creates a rectangle at position `(100, 400)` with a width of `40` and a height of `40`.

Now draw the player:

```python
def draw():
    screen.clear()
    screen.draw.filled_rect(player, "blue")
```

You should now see a blue square on the screen.

### Explanation

The player has an `x` position and a `y` position.

- `x` controls left and right movement.
- `y` controls up and down movement.

In many 2D games, the top-left corner of the screen is close to `(0, 0)`.

As `x` gets larger, the object moves right.

As `y` gets larger, the object moves down.

### Try It

Change the player's starting position.

Try changing:

```python
player = Rect((100, 400), (40, 40))
```

What happens if you change `100`?

What happens if you change `400`?

What happens if you change the size from `(40, 40)` to `(60, 60)`?

---

# Step 3: Move the Player Left and Right

A platformer needs movement.

Inside the `update()` function, check if the player is pressing the left or right arrow keys:

```python
def update():
    if keyboard.left:
        player.x -= 5

    if keyboard.right:
        player.x += 5
```

### Explanation

The player moves because the code changes the player's `x` position.

```python
player.x -= 5
```

This moves the player left.

```python
player.x += 5
```

This moves the player right.

The number `5` is the player's movement speed.

### Try It

Change the speed from `5` to another number.

Try:

```python
player.x -= 2
player.x += 2
```

Then try:

```python
player.x -= 10
player.x += 10
```

Which one feels better for your game?

---

# Step 4: Keep the Player on the Screen

Right now, your player might move off the screen. That can cause problems.

Add boundaries so the player cannot leave the window:

```python
def update():
    if keyboard.left:
        player.x -= 5

    if keyboard.right:
        player.x += 5

    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH
```

### Explanation

This code checks whether the player has moved too far left or right.

If the player goes past the left side of the screen, the code moves the player back.

If the player goes past the right side of the screen, the code moves the player back.

### Think About It

- Why do we use `player.left` instead of only `player.x`?
- What does `player.right` mean?
- What would happen if the player could leave the screen?

---

# Step 5: Add Gravity

Platformers need gravity.

Gravity pulls the player down.

Create two variables near the top of your code:

```python
velocity_y = 0
gravity = 1
```

Then update the player's vertical movement:

```python
def update():
    global velocity_y

    velocity_y += gravity
    player.y += velocity_y
```

### Explanation

`velocity_y` is the player's vertical speed.

`gravity` increases the player's vertical speed over time.

That means the player falls faster the longer they are in the air.

This is similar to how gravity feels in real life, but simplified for a game.

### Important

If your player falls off the screen forever, that is expected for now. You have added gravity, but you have not added the ground yet.

---

# Step 6: Add the Ground

The player needs something to land on.

Add this code to stop the player at the bottom of the screen:

```python
def update():
    global velocity_y

    velocity_y += gravity
    player.y += velocity_y

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
        velocity_y = 0
```

### Explanation

This code checks if the bottom of the player has gone below the bottom of the game window.

If it has, the player is moved back onto the screen.

Then `velocity_y` is set back to `0`, which stops the player from continuing to fall.

### Try It

Change the value of `gravity`.

Try:

```python
gravity = 0.5
```

Then try:

```python
gravity = 2
```

How does the game feel different?

---

# Step 7: Add Jumping

A platformer is not really a platformer until the player can jump.

Create a variable to track whether the player is on the ground:

```python
on_ground = False
```

Then add jumping code:

```python
def update():
    global velocity_y, on_ground

    velocity_y += gravity
    player.y += velocity_y

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
        velocity_y = 0
        on_ground = True

    if keyboard.space and on_ground:
        velocity_y = -15
        on_ground = False
```

### Explanation

When the player presses the spacebar, the player jumps.

The jump works by setting `velocity_y` to a negative number.

```python
velocity_y = -15
```

A negative `y` speed moves the player upward.

Gravity will then pull the player back down.

### Why Use `on_ground`?

The `on_ground` variable prevents the player from jumping forever in the air.

Without it, the player could fly by holding the spacebar.

### Try It

Change the jump strength.

Try:

```python
velocity_y = -10
```

Then try:

```python
velocity_y = -20
```

Which jump height feels best?

---

# Step 8: Create Platforms

Now it is time to add actual platforms.

Create a list of platform rectangles:

```python
platforms = [
    Rect((0, 470), (800, 30)),
    Rect((200, 380), (150, 20)),
    Rect((450, 300), (150, 20)),
    Rect((650, 220), (100, 20))
]
```

The first platform is the ground.

The others are floating platforms.

Update your `draw()` function so it draws every platform:

```python
def draw():
    screen.clear()
    screen.draw.filled_rect(player, "blue")

    for platform in platforms:
        screen.draw.filled_rect(platform, "green")
```

### Explanation

A list lets you store multiple platforms in one variable.

The `for` loop draws each platform one at a time.

This is much better than writing separate drawing code for every single platform.

### Try It

Add your own platform to the list.

Example:

```python
Rect((100, 250), (120, 20))
```

Change the position and size to design your own level.

---

# Step 9: Land on Platforms

Right now, the platforms may appear on the screen, but the player may not actually land on them correctly.

You need collision detection.

Add this inside your `update()` function after gravity moves the player:

```python
on_ground = False

for platform in platforms:
    if player.colliderect(platform) and velocity_y > 0:
        player.bottom = platform.top
        velocity_y = 0
        on_ground = True
```

Because this changes `on_ground`, your function should include it as a global variable:

```python
global velocity_y, on_ground
```

### Explanation

Collision means two objects are touching or overlapping.

```python
player.colliderect(platform)
```

This checks whether the player rectangle is touching a platform rectangle.

The code also checks:

```python
velocity_y > 0
```

This means the player is falling downward.

If the player is falling and touches a platform, the code places the player's feet on top of the platform.

### Think About It

- Why should the player only land when falling down?
- What might happen if the player hits the side of a platform?
- Why do we set `velocity_y` back to `0`?

---

# Step 10: Add Collectibles

Most platformers have something to collect, such as coins, gems, stars, footballs, or energy cells.

Create a list of collectibles:

```python
coins = [
    Rect((250, 340), (20, 20)),
    Rect((500, 260), (20, 20)),
    Rect((690, 180), (20, 20))
]

score = 0
```

Draw the collectibles:

```python
for coin in coins:
    screen.draw.filled_rect(coin, "yellow")
```

Add collision code so the player can collect them:

```python
global score

for coin in coins[:]:
    if player.colliderect(coin):
        coins.remove(coin)
        score += 1
```

Draw the score:

```python
screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
```

### Explanation

The collectibles are stored in a list.

When the player touches a coin, the coin is removed from the list.

The score goes up by 1.

The reason we use `coins[:]` is because we are making a copy of the list while looping. This helps avoid problems when removing items.

### Customize It

Your collectibles do not have to be coins.

You could collect:

- stars
- gems
- keys
- footballs
- pizza slices
- batteries
- magic crystals
- trophies

---

# Step 11: Add Hazards

A game needs challenge.

Hazards are things the player should avoid.

Examples include lava, spikes, enemies, lasers, water, or traps.

Create a hazard:

```python
lava = Rect((350, 450), (100, 20))
```

Draw the hazard:

```python
screen.draw.filled_rect(lava, "red")
```

Add collision code:

```python
if player.colliderect(lava):
    player.x = 100
    player.y = 400
    velocity_y = 0
```

### Explanation

If the player touches the hazard, the player is sent back to the starting position.

This creates a consequence without ending the entire game.

### Challenge Options

Instead of only resetting the player, you could add:

- lives
- a health bar
- a game over screen
- a sound effect
- a checkpoint
- a timer penalty

---

# Step 12: Add a Goal

The player needs a way to win.

Create a goal rectangle:

```python
goal = Rect((730, 420), (40, 50))
game_won = False
```

Draw the goal:

```python
screen.draw.filled_rect(goal, "purple")
```

Check if the player reached the goal:

```python
global game_won

if player.colliderect(goal):
    game_won = True
```

Show a win message:

```python
if game_won:
    screen.draw.text("You Win!", center=(400, 250), fontsize=60, color="yellow")
```

### Explanation

The `game_won` variable tracks whether the player has won.

It starts as `False`.

When the player touches the goal, it changes to `True`.

The draw function can then display a winning message.

### Customize It

Your goal could be:

- a treasure chest
- a portal
- a spaceship
- a trophy
- a castle door
- an end zone
- an escape door

---

# Step 13: Organize Your Code

As your game gets bigger, your code can become messy.

Try organizing your code into sections.

Example:

```python
# Window settings
WIDTH = 800
HEIGHT = 500

# Player variables
player = Rect((100, 400), (40, 40))
velocity_y = 0
gravity = 1
on_ground = False

# Platforms
platforms = [
    Rect((0, 470), (800, 30)),
    Rect((200, 380), (150, 20))
]

# Collectibles
coins = []
score = 0

# Hazards and goal
lava = Rect((350, 450), (100, 20))
goal = Rect((730, 420), (40, 50))
game_won = False
```

You can also create helper functions.

Example:

```python
def reset_player():
    player.x = 100
    player.y = 400
```

Then instead of writing the reset code again and again, you can call:

```python
reset_player()
```

### Explanation

Good programmers organize their code so it is easier to read, fix, and improve.

Functions help you avoid repeating the same code many times.

---

# Step 14: Customize Your Game

Once the basic game works, make it your own.

You may customize:

- the title
- the theme
- the player
- platform layout
- collectibles
- hazards
- goal
- colors
- difficulty
- story

### Theme Ideas

- Jungle Gem Quest
- Football Training Obstacle Course
- Space Explorer
- Robot Factory Escape
- Ninja Rooftop Runner
- Haunted Castle
- Pizza Delivery Dash
- Underwater Adventure

---

# Required Final Game Features

Your finished platformer must include:

- A player character
- Left and right movement
- Jumping
- Gravity
- At least 4 platforms
- At least 3 collectibles
- A score display
- At least 1 hazard
- A goal
- A win condition
- A custom theme

---

# Bonus Features

You may add bonus features after your required features work.

Possible bonus features:

- Moving enemy
- Multiple hazards
- Lives system
- Timer
- Multiple levels
- Sound effects
- Background image
- Custom player sprite
- Start screen
- Game over screen
- Double jump
- Power-up
- Secret area
- Checkpoint

---

# Debugging Tips

If something does not work, do not panic. Debugging is part of programming.

Try these steps:

1. Read the error message carefully.
2. Check spelling and capitalization.
3. Make sure your indentation is correct.
4. Check that variables are created before you use them.
5. Make sure global variables are listed inside functions when needed.
6. Test one feature at a time.
7. Use `print()` to check values.
8. Ask a classmate to look at your code.
9. Compare your code to the example, but do not blindly copy.
10. Explain out loud what you think the code is doing.

---

# Common Problems

## My player falls through the floor.

Check your ground or platform collision code.

Make sure you are checking `player.bottom` and setting it correctly.

## My player cannot jump.

Check that `on_ground` becomes `True` when the player lands.

Also check that the jump code uses the correct key.

## My player jumps forever.

Make sure the player can only jump when `on_ground` is `True`.

## My coin disappears but the score does not change.

Make sure you included:

```python
global score
```

inside the function where the score changes.

## My player resets when touching lava, but then keeps falling strangely.

Make sure you reset `velocity_y` to `0` when the player touches the hazard.

---

# Final Reflection Questions

Answer these when your project is complete.

1. What is the title of your platformer game?
2. What is the theme of your game?
3. What was the hardest feature to add?
4. What bug did you have to fix?
5. What is one thing you customized?
6. What is one feature you would add if you had more time?
7. What did this project teach you about how games work?

---

# Final Reminder

Your goal is not to make the biggest game possible.

Your goal is to make a small game that works.

Start simple. Test often. Add one feature at a time.

A working simple game is better than a huge broken game.
