import pygame
import random
pygame.init()

screen = pygame.display.set_mode([600, 600])
surface = pygame.display.get_surface()
w, h = surface.get_width(), surface.get_height()
pygame.display.set_caption('Snake Game')
the_snake = pygame.image.load('the_snake.png')
the_bg = pygame.image.load('the_bg.jpg')
the_fruits = [pygame.image.load('apple.png'), pygame.image.load('banana.png'), pygame.image.load('lemon.png'),
              pygame.image.load('pear.png'), pygame.image.load('watermelon.png')]
music = pygame.mixer.music.load('music.mp3')
eat = pygame.mixer.Sound('BITE.wav')
pygame.mixer.music.play(-1)

class Snake(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 12
        self.dir = 0

    def draw(self, screen):
        screen.blit(the_snake, (self.x, self.y))

class Fruit(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.the_fruit = the_fruits[random.randrange(len(the_fruits))]

    def draw(self, screen):
        screen.blit(self.the_fruit, (self.x, self.y))


class Body(object):
    def __init__(self, x, y, radius, count):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (128, 255, 0)
        self.sec_color = (0, 102, 0)
        self.count = count

    def draw(self, screen):
        if self.count %2 == 0:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(screen, self.sec_color, (self.x, self.y), self.radius)

snake = Snake(250, 250, 40, 40)
fruits = []
bodies = [Body(snake.x + snake.width//2, snake.y + snake.height, 15, 0)]
TailX = []
TailY = []
count = -1
score = 0
running = True
font = pygame.font.SysFont('comicsans', 40, True)
game_over = False

def redrawGameWindow():
    global running, count, score
    screen.blit(the_bg, (0, 0))
    text = font.render('Score: '+ str(score), 1, (51, 153, 255))
    screen.blit(text, (20, 20))
    if snake.dir == 2:
        snake.y -= snake.speed
        bodies[0].x = snake.x + snake.width // 2
        bodies[0].y = snake.y + snake.height

    elif snake.dir == -2:
        snake.y += snake.speed
        bodies[0].x = snake.x + snake.width // 2
        bodies[0].y = snake.y

    elif snake.dir == 1:
        snake.x += snake.speed
        bodies[0].x = snake.x
        bodies[0].y = snake.y + snake.height // 2

    elif snake.dir == -1:
        snake.x -= snake.speed
        bodies[0].x = snake.x + snake.width
        bodies[0].y = snake.y + snake.height // 2

    for fruit in fruits:
        if ((fruit.x <= snake.x + snake.width) and (fruit.x + fruit.width >= snake.x) and (fruit.y >= snake.y - 20) and (fruit.y <= snake.y + snake.height)):
            fruits.pop(fruits.index(fruit))
            count += 1
            score += 1
            if snake.dir == 2 or snake.dir == -2:
                bodies.append(Body(bodies[len(bodies) - 1].x - 15, bodies[len(bodies) - 1].y, 15, count))
            elif snake.dir == 1 or snake.dir == -1:
                bodies.append(Body(bodies[len(bodies) - 1].x, bodies[len(bodies) - 1].y - 15, 15, count))

            if score % 10 == 0:
                snake.speed += 2
            eat.play()
        fruit.draw(screen)

    prevX = bodies[0].x
    prevY = bodies[0].y
    for i in range(1, len(bodies)):
        prev2X = bodies[i].x
        prev2Y = bodies[i].y
        bodies[i].x = prevX
        bodies[i].y = prevY
        prevX = prev2X
        prevY = prev2Y
        bodies[i-1].draw(screen)

    for i in range(4, len(bodies)):
        if ((snake.x + snake.width//2 >= bodies[i].x - 15) and (snake.x + snake.width//2<= bodies[i].x + 15)):
            if ((snake.y + snake.height//2>= bodies[i].y - 15) and (snake.y + snake.height//2 <= bodies[i].y + 15)):
                running = False

    snake.draw(screen)

def main_function():
    global running
    while running:
        pygame.time.delay(50)
        if (len(fruits) == 0):
            fruit_x = random.randrange(5, w - 25, 1)
            fruit_y = random.randrange(5, h - 25, 1)
            fruits.append(Fruit(fruit_x, fruit_y, 30, 30))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snake.dir = 2
        if keys[pygame.K_DOWN]:
            snake.dir = -2
        if keys[pygame.K_LEFT]:
            snake.dir = -1
        if keys[pygame.K_RIGHT]:
            snake.dir = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if((snake.x - 20 <= 0) or (snake.x + snake.width + 10>= w) or (snake.y -20 <= 0) or (snake.y + snake.height + 10 >= h)):
            running = False
        redrawGameWindow()
        pygame.display.update()

def start_game():
    global game_over, score
    run = True
    text = pygame.font.SysFont('comicsans', 30)
    data = text.render("Click space to start the game!", 1,  (51, 152, 255))
    tutorial = text.render("Use arrow keys to move the snake. Eat fruits to grow.", 1,  (51, 152, 255))
    while run and not game_over:
        screen.blit(the_bg, (0, 0))
        screen.blit(data, (w//2 - 200, h // 2 - 20))
        screen.blit(tutorial, (w // 2 - 250, h // 2 + 20))
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_SPACE]):
            main_function()
            game_over = True
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                game_over = True
                run = False
        pygame.display.update()

    game_over = False
    while not game_over:
        if score == 0:
            screen.blit(the_bg, (0, 0))
        go = text.render("Game Over!", 1, (51, 152, 255))
        screen.blit(go, (w // 2 - 200, h // 2 - 20))
        start_again = text.render("Press q to quit", 1, (51, 152, 255))
        score_text = text.render("Score: " + str(score), 1, (51, 152, 255))
        screen.blit(start_again, (w // 2 - 200, h // 2 + 20))
        screen.blit(score_text, (w // 2 - 200, h // 2 + 50))
        keys1 = pygame.key.get_pressed()
        if (keys1[pygame.K_q]):
            game_over = True
        pygame.event.pump()
        pygame.display.update()

if not game_over:
    start_game()
pygame.quit()