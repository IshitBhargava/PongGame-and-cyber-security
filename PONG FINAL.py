import pygame
import sys
import random
import time
rbb = int(input("enter background colour (red): "))
gbb = int(input("enter background colour (green): "))
bbb = int(input("enter background colour (blue): "))
rb = int(input("enter UI colour (red): "))
gb = int(input("enter UI colour (green): "))
bb = int(input("enter UI colour (blue): "))
ballsp = int(input("enter ball speed: "))
paddlesp = int(input("enter paddle speed: "))
name = input("Please enter your name: ")
# Messages
messages = [
    "Dear [Name], your monthly account statement is now available for viewing. Please log in to your online banking account to access it. If you have any questions, feel free to contact our customer support team.",
    "Congratulations! You've won a lottery/prize worth $1,000,000! To claim your prize, please reply with your personal information and bank details",
    "This is the IRS. You have an outstanding tax debt, and legal action will be taken against you if it's not paid immediately. Please call this number to make a payment.",
    "Dear [Name], Congratulations! We are pleased to inform you that your loan application has been approved. Please review the terms and conditions provided in the attached document. If you have any questions, our loan specialists are available to assist you.",
    "Dear [Name], We have noticed unusual activity on your account. For your security, we have temporarily blocked access to your online banking. Please call our customer service hotline immediately to verify the activity and restore access to your account."
]
score = 0
def ask_question(screen, font, name):
    global score
    message = random.choice(messages).replace("[Name]", name)
    print("Received message:", message)

    # Determine the correct response based on the message
    if "lottery" in message.lower() or "prize" in message.lower():
        correct_response = "fake"
    elif "irs" in message.lower() or "tax debt" in message.lower():
        correct_response = "fake"
    else:
        correct_response = "real"

    # Clear the screen
    screen.fill((rbb, gbb, bbb))
    
    # Display the question
    question_text = font.render("Received message:", True, (rb, gb, bb))
    screen.blit(question_text, (50, 50))
    
    # Split message into multiple lines if necessary
    lines = []
    words = message.split()
    current_line = ''
    for word in words:
        if font.size(current_line + word)[0] > 400:  # Check if adding the word exceeds width
            lines.append(current_line)
            current_line = ''
        current_line += word + ' '
    lines.append(current_line)

    y_offset = 100
    for line in lines:
        message_text = font.render(line, True, (rb, gb, bb))
        screen.blit(message_text, (50, y_offset))
        y_offset += 30  # Adjust the vertical spacing

    # Input box for response
    input_box = pygame.Rect(50, y_offset + 20, 400, 32)
    response = ''
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    response = response[:-1]
                else:
                    response += event.unicode

        # Clear the input box
        pygame.draw.rect(screen, (rb, gb, bb), input_box)
        pygame.display.flip()

        # Render and display response text
        response_text = font.render(response, True, (rbb, gbb, bbb))
        screen.blit(response_text, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

    if response.lower() == correct_response:
        score += 5
        print("You are correct!")
    else:
        score -= 3
        print("You are wrong. Game over!")
        pygame.quit()
        sys.exit()

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = ballsp
PADDLE_SPEED = paddlesp

# Colors
WHITE = (rb, gb, bb)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong and Cybersecurity Quiz")

# Create game objects
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = BALL_SPEED * random.choice([1, -1])
ball_speed_y = BALL_SPEED * random.choice([1, -1])

player_paddle = pygame.Rect(WIDTH - 50 - 20, HEIGHT // 2 - 50, 20, 100)
computer_paddle = pygame.Rect(30, HEIGHT // 2 - 50, 20, 100)

# Game variables
font = pygame.font.Font(None, 24)
player_score = 0
computer_score = 0

print("GENERAL INSTRUCTIONS: Please respond with 'yes' if it is a fraud message and 'not' if it is not a fraud message. If you answer wrong, the game will end.")

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

    # Move the computer paddle
    if ball.top < computer_paddle.top:
        computer_paddle.y -= PADDLE_SPEED
    elif ball.bottom > computer_paddle.bottom:
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
    elif ball.right >= WIDTH:
        computer_score += 1
        print("Computer Score:", computer_score)
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = BALL_SPEED * random.choice([1, -1])
        ball_speed_y = BALL_SPEED * random.choice([1, -1])
        ask_question(screen, font, name)

    # Clear the screen
    screen.fill((rbb, gbb, bbb))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw scores
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    computer_text = font.render(f"Computer: {computer_score}", True, WHITE)
    screen.blit(player_text, (WIDTH - 150, 10))
    screen.blit(computer_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the game's speed
    pygame.time.delay(30)
