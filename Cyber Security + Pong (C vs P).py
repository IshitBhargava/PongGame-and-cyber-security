import pygame   # Game Processing Library
import sys  # Keyboard input library
import random  # Choosing a random question
import time   # Delay 

name = input("Please enter your name: ")  # name for personilazation of messages
ans = 0                                                         # default values
# Messages
messages = [
    f"Dear {name}, your monthly account statement is now available for viewing. Please log in to your online banking account to access it. If you have any questions, feel free to contact our customer support team.",   # real message
    "Congratulations! You've won a lottery/prize worth $1,000,000! To claim your prize, please reply with your personal information and bank details",   # fraud message 
    "This is the IRS. You have an outstanding tax debt, and legal action will be taken against you if it's not paid immediately. Please call this number to make a payment.",   # fraud message 
    f"Dear {name}, Congratulations! We are pleased to inform you that your loan application has been approved. Please review the terms and conditions provided in the attached document. If you have any questions, our loan specialists are available to assist you.",   # real message
    f"Dear {name}, We have noticed unusual activity on your account. For your security, we have temporarily blocked access to your online banking. Please call our customer service hotline immediately to verify the activity and restore access to your account."   # real message
]
score = 0

print("GENERAL INSTRUCTIONS: Please respond with 'yes' if it is a fraud message and 'no' if it is not a fraud message! If you answer wrong, then the game will end.")
print("   ")

def ask_question():
    global score
    global ans
    message = random.choice(messages)
    print("Received message:", message)
    
    # Define a dictionary to map each message to its correct response
    message_responses = {
        messages[0]: "not",
        messages[1]: "yes",
        messages[2]: "yes",
        messages[3]: "not",
        messages[4]: "not"
    }
    
    correct_response = message_responses[message]
    
    response = input("Fraud or not: ")
    if response == correct_response:
        score += 5
        print("You are correct!")
        ans = 1
    else:
        score -= 3
        ans = 0
        print("You are wrong.")
    print("   ")

a = int(input("enter ball speed: (Default-7): "))
b = int(input("enter paddle speed: (Default-12): "))
c = int(input("red brightness: (0-255): "))
d = int(input("green brightness: (0-255): "))
e = int(input("blue brightness: (0-255): "))
f = input("screen title: ")

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = a
PADDLE_SPEED = b

# Colors
WHITE = (c, d, e)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f)

# Create game objects
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = BALL_SPEED * random.choice([1, -1])
ball_speed_y = BALL_SPEED * random.choice([1, -1])

player_paddle = pygame.Rect(WIDTH - 50 - 20, HEIGHT // 2 - 50, 20, 100)
computer_paddle = pygame.Rect(30, HEIGHT // 2 - 50, 20, 100)

# Game variables
font = pygame.font.Font(None, 36)
player_score = 0
computer_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the player paddle
    keys = pygame.key.get_pressed()
    player_paddle.y -= keys[pygame.K_UP] * PADDLE_SPEED
    player_paddle.y += keys[pygame.K_DOWN] * PADDLE_SPEED

    # Ensure player paddle stays within the valid range
    player_paddle.y = max(0, min(player_paddle.y, HEIGHT - player_paddle.height))

    # Move the computer paddle to track the ball
    if ball.centery < computer_paddle.centery:
        computer_paddle.y -= PADDLE_SPEED
    elif ball.centery > computer_paddle.centery:
        computer_paddle.y += PADDLE_SPEED

    # Ensure computer paddle stays within the valid range
    computer_paddle.y = max(0, min(computer_paddle.y, HEIGHT - computer_paddle.height))

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds
    if ball.left <= 0:
        player_score += 1
        print("Player Score:", player_score)
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = BALL_SPEED * random.choice([1, -1])
        ball_speed_y = BALL_SPEED * random.choice([1, -1])
        ask_question()
        if(ans == 0):
            print("your score is:",score)
            input("press enter to exit!")
            break
        time.sleep(10)  # Pause for 10 seconds
    elif ball.right >= WIDTH:
        computer_score += 1
        print("Computer Score:", computer_score)
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = BALL_SPEED * random.choice([1, -1])
        ball_speed_y = BALL_SPEED * random.choice([1, -1])
        ask_question()
        if(ans == 0):
            print("your score is:",score)
            input("press enter to exit")
            break
        time.sleep(10)  # Pause for 10 seconds

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Update the display
    pygame.display.flip()

    # Control the game's speed
    pygame.time.delay(30)
