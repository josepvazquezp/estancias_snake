import pygame
import random

#colores
BACKGROUND_C = (0, 0, 0)        #negro
SNAKE_C = (0, 255, 0)           #verde
FOOD_C = (255, 0, 0)            #rojo
GAME_OVER_C = (102, 0, 153)     #morado
W_COMMAND_C = (255, 255, 255)   #blanco
K_COMMAND_C = (0, 255, 255)     #azul
POINTS_C = (255, 255, 0)    #amarillo
AUTHOR_C = (232, 0, 255)        #rosa
TITLE_C = (0, 255, 0)           #verde

#booleanos
running = True
game_over = False
pause = False
start = False

#dimensione
SCREENSIZE = 500
PIXEL_WIDTH = 10
PIXEL_HEIGHT = 10

#velocidad de movimiento
VEL = 10

#direccion inicial
direction = "RIGHT"

#coordenadas snake inicial
headX = 50
headY = 50

#coordenadas iniciales d ecomida
foodX = random.randrange(0, 49) * 10
foodY = random.randrange(0, 49) * 10

#arreglos
snake = [(headX, headY)]
food = [(foodX, foodY)]


#funciones de logica del juego
def moveSnake(direction, snake, vel):
    newHeadX = snake[0][0]
    newHeadY = snake[0][1]

    snake.pop()

    if direction == "UP":
        newHeadY -= vel
    elif direction == "DOWN":
        newHeadY += vel
    elif direction == "RIGHT":
        newHeadX += vel
    elif direction == "LEFT":
        newHeadX -= vel

    snake.insert(0, (newHeadX, newHeadY))

def growSnake(snake, direction, pixelWidth, pixelHeight):
    #colision serpiente y comida
    queueX = snake[0][0]
    queueY = snake[0][1]

    if direction == "RIGHT":
        queueX -= pixelWidth
    elif direction == "LEFT":
        queueX += pixelWidth
    elif direction == "UP":
        queueY -= pixelHeight
    elif direction == "DOWN":
        queueY += pixelHeight

    snake.append((queueX, queueY))

def teleportFood(food, pixelWidth, pixelHeight):
    #colision de serpiente y comida
    food.pop()

    x = random.randrange(0, 49) * pixelWidth
    y = random.randrange(0, 49) * pixelHeight

    food.append((x, y))

def outOfBounds(snake, screensize):
    (headX, headY) = snake[0]

    if headX < 0 or headX > screensize:
        return True                         #game_over = True
    elif headY < 0 or headY > screensize:
        return True

    return False

def snakeCollision(snake, gameOver):
    count = snake.count(snake[0])

    if count > 1:
        return True             #game_over = True

    return gameOver

def restart(snake, food, headX, headY, pixelWidth, pixelHeight):
    snake.clear()
    snake.append((headX, headY))

    food.clear()
    x = random.randrange(0, 49) * pixelWidth
    y = random.randrange(0, 49) * pixelHeight
    food.append((x, y))



#funciones de interfaz grafica
def drawSnake(win, snake, pixelWidth, pixelHeight, background_c, snake_c):
    win.fill(background_c)

    for pixel in snake:
        pygame.draw.rect(win, snake_c, (pixel[0], pixel[1], pixelWidth, pixelHeight))

    pygame.display.update()

def drawFood(win, food, pixelWidth, pixelHeight, food_c):
    pygame.display.flip()

    for pixel in food:
        pygame.draw.rect(win, food_c, (pixel[0], pixel[1], pixelWidth, pixelHeight))

    pygame.display.update()

def gameOverWindow(win, snake, game_over_c, k_command_c, w_command_c, points_c):
    count = len(snake) - 1

    win.get_rect()

    font = pygame.font.Font(None, 80)
    font2 = pygame.font.Font(None, 30)

    text1 = font.render("Game Over", True, game_over_c)
    text2 = font2.render("R", True, k_command_c)
    text3 = font2.render("Restart", True, w_command_c)
    text4 = font2.render("Q", True, k_command_c)
    text5 = font2.render("Quit", True, w_command_c)
    points = font2.render("Points: " + str(count), True, points_c)

    text1.get_rect()
    text2.get_rect()
    text3.get_rect()
    text4.get_rect()
    text5.get_rect()
    points.get_rect()

    win.blit(text1, (100, 120))
    win.blit(text2, (160, 280))
    win.blit(text3, (190, 280))
    win.blit(text4, (160, 315))
    win.blit(text5, (190, 315))
    win.blit(points, (210, 200))

    pygame.display.flip()

def pauseWindow(win, k_command_c, w_command_c):
    win_rect = win.get_rect()

    font = pygame.font.Font(None, 30)

    text = font.render("C", True, k_command_c)
    text_surface = font.render("Continue", True, w_command_c)

    text_rect = text_surface.get_rect()
    text.get_rect()

    text_rect.center = win_rect.center

    win.blit(text, (160, 240))
    win.blit(text_surface, text_rect)

    pygame.display.flip()

def startWindow(win, title_c, k_command_c, w_commnad_c, author_c):
    win.get_rect()

    f = pygame.font.Font(None, 120)
    s = pygame.font.Font(None, 30)

    snake = f.render("SNAKE", True, title_c)
    st = s.render("S", True, k_command_c)
    pres = s.render("Start", True, w_commnad_c)
    by = s.render("By: JPVP", True, author_c)

    snake.get_rect()
    pres.get_rect()
    st.get_rect()
    by.get_rect()

    win.blit(snake, (100, 100))
    win.blit(st, (220, 220))
    win.blit(pres, (240, 220))
    win.blit(by, (210, 370))

    pygame.display.update()

#funcion principal
def main(running, game_over, pause, start,
         SCREENSIZE, PIXEL_WIDTH, PIXEL_HEIGHT, headX, headY,
         snake, food,
         BACKGROUND_C, SNAKE_C, FOOD_C, GAME_OVER_C, W_COMMAND_C, K_COMMAND_C, POINTS_C, AUTHOR_C, TITLE_C,
         VEL, direction):
    pygame.init()
    win = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
    pygame.display.set_caption("SnakeGame")

    while running:
        clock = pygame.time.Clock()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"
        elif keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        elif keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        elif keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"

        if start == False:
            startWindow(win, TITLE_C, K_COMMAND_C, W_COMMAND_C, AUTHOR_C)

            if keys[pygame.K_s]:
                start = True

        elif keys[pygame.K_p]:
            pause = True

        if start == True and game_over == False and pause == False:
            moveSnake(direction, snake, VEL)

            drawSnake(win, snake, PIXEL_WIDTH, PIXEL_HEIGHT, BACKGROUND_C, SNAKE_C)

            drawFood(win, food, PIXEL_WIDTH, PIXEL_HEIGHT, FOOD_C)

            if snake[0] == food[0]:
                growSnake(snake, direction, PIXEL_WIDTH, PIXEL_HEIGHT)

                teleportFood(food, PIXEL_WIDTH, PIXEL_HEIGHT)

            game_over = outOfBounds(snake, SCREENSIZE)

            game_over = snakeCollision(snake, game_over)

        if game_over == True:
            gameOverWindow(win, snake, GAME_OVER_C, K_COMMAND_C, W_COMMAND_C, POINTS_C)

            if keys[pygame.K_q]:
                running = False

            if keys[pygame.K_r]:
                restart(snake, food, headX, headY, PIXEL_WIDTH, PIXEL_HEIGHT)
                game_over = False
                direction = "RIGHT"
                pygame.display.update()

        if pause == True:
            pauseWindow(win, K_COMMAND_C, W_COMMAND_C)

            if keys[pygame.K_c]:
                pause = False

    pygame.quit()

main(running, game_over, pause, start,
     SCREENSIZE, PIXEL_WIDTH, PIXEL_HEIGHT, headX, headY,
     snake, food,
     BACKGROUND_C, SNAKE_C, FOOD_C, GAME_OVER_C, W_COMMAND_C, K_COMMAND_C, POINTS_C, AUTHOR_C, TITLE_C,
     VEL, direction)