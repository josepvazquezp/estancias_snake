import pygame
import random

#CONSTANTES MAYUSCULAS
#colores
BACKGROUND_C = (0, 0, 0)        #negro
SNAKE_C = (0, 255, 0)           #verde
TITLE_C = (0, 255, 0)           #verde
FOOD_C = (255, 0, 0)            #rojo
GAME_OVER_C = (102, 0, 153)     #morado
W_COMMAND_C = (255, 255, 255)   #blanco
K_COMMAND_C = (0, 255, 255)     #azul bajito
POINTS_C = (255, 255, 0)        #amarillo
AUTHOR_C = (232, 0, 255)        #morado 2.0

#booleanos
running = True
game_over = False
pause = False
start = False

#dimensiones
SCREENSIZE = 500
PIXEL_WIDTH = 10
PIXEL_HEIGTH = 10

#coordenadas de cabeza de sepiente (iniciales)
headX = 50
headY = 50

#velocidad de movimiento
VEL = 10

#direccion inicial
direction = "RIGHT"

#logica de coordenadas y ancho de pixel
foodX = random.randrange(0, 49) * 10
foodY = random.randrange(0, 49) * 10

#arreglos
snake = [(headX, headY)]
food = [(foodX, foodY)]


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


def drawSnake(win, snake, pixelWidth, pixelHeight):
    win.fill(BACKGROUND_C)

    for pixel in snake:
        pygame.draw.rect(win, (SNAKE_C), (pixel[0], pixel[1], pixelWidth, pixelHeight))

    pygame.display.update()


def drawFood(win, food, pixelWidth, pixelHeight):
    pygame.display.flip()

    for pixel in food:
        pygame.draw.rect(win, (FOOD_C), (pixel[0], pixel[1], pixelWidth, pixelHeight))

    pygame.display.update()


def growSnake(snake, pixelWidth, pixelHeight):
    #colision serpiente y comida
    queueX = headX
    queueY = headY

    if direction == "RIGHT":
        queueX = headX - pixelWidth
    elif direction == "LEFT":
        queueX = headX + pixelWidth
    elif direction == "UP":
        queueY = headY - pixelHeight
    elif direction == "DOWN":
        queueY= headY + pixelHeight

    snake.append((queueX, queueY))


def teleportFood(food, pixelWidth, pixelHeight):
    # colision serpiente y comida
    food.pop()

    x = random.randrange(0, 49) * pixelWidth
    y = random.randrange(0, 49) * pixelHeight

    food.append((x, y))

def outOfBounds(snake, screensize):
    (headX, headY) = snake[0]

    if headX < 0 or headX > screensize:
        return True                     #game_over = True
    elif headY < 0 or headY > screensize:
        return True                     #game_over = True

    return False                        #game_over = False

def colisionSerpiente(snake):
    global game_over
    cuenta = snake.count(snake[0])

    if cuenta > 1:
        game_over = True


def gameOver(win):
    global game_over
    if game_over == True:
        win.get_rect()
        font = pygame.font.Font(None, 80)
        fuente = pygame.font.Font(None, 30)
        text1 = font.render("Game Over", True, GAME_OVER_C)
        text2 = fuente.render("R", True, K_COMMAND_C)
        text3 = fuente.render("Restart", True, W_COMMAND_C)
        text4 = fuente.render("Q", True, K_COMMAND_C)
        text5 = fuente.render("Quit", True, W_COMMAND_C)
        text1.get_rect()
        text2.get_rect()
        text3.get_rect()
        text4.get_rect()
        text5.get_rect()
        win.blit(text1, (100, 120))
        win.blit(text2, (160, 280))
        win.blit(text3, (190, 280))
        win.blit(text4, (160, 315))
        win.blit(text5, (190, 315))

    pygame.display.flip()


def pausar(win, keys):
    global pause
    if keys[pygame.K_p]:
        pause = True

    if pause == True:
        win_rect = win.get_rect()
        font = pygame.font.Font(None, 30)
        texto = font.render("C", True, K_COMMAND_C)
        text_surface = font.render("Continue", True, W_COMMAND_C)
        text_rect = text_surface.get_rect()
        texto.get_rect()
        text_rect.center = win_rect.center
        win.blit(texto, (160, 240))
        win.blit(text_surface, text_rect)

        if keys[pygame.K_c]:
            pause = False

    pygame.display.flip()


def reiniciar(keys):
    global game_over
    global direction
    if game_over == True and keys[pygame.K_r]:
        snake.clear()
        snake.append((headX, headY))
        food.clear()
        x = random.randrange(0, 49) * 10
        y = random.randrange(0, 49) * 10
        food.append((x, y))
        game_over = False

        direction = "RIGHT"

        pygame.display.update()


def salir(keys):
    global game_over
    global running
    if game_over == True and keys[pygame.K_q]:
        running = False


def puntos(snake, win):
    global game_over
    cuenta = len(snake)

    if game_over == True:
        win.get_rect()
        font = pygame.font.Font(None, 30)
        puntuacion = font.render("Points: " + str(cuenta), True, POINTS_C)
        puntuacion.get_rect()
        win.blit(puntuacion, (210, 200))


def pantallaStart(win, keys):
    global start
    global game_over
    global pause
    if start == False:
        win.get_rect()
        f = pygame.font.Font(None, 120)
        s = pygame.font.Font(None, 30)
        snake = f.render("SNAKE", True, TITLE_C)
        st = s.render("S", True, K_COMMAND_C)
        pres = s.render("Start", True, W_COMMAND_C)
        by = s.render("By: JPVP", True, AUTHOR_C)
        snake.get_rect()
        pres.get_rect()
        st.get_rect()
        win.blit(snake, (100, 100))
        win.blit(st, (220, 220))
        win.blit(pres, (240, 220))
        win.blit(by, (210, 370))

        if keys[pygame.K_s]:
            start = True


    pygame.display.update()

def main():
    global direction
    global running
    global snake
    global food
    global VEL
    global PIXEL_WIDTH
    global PIXEL_HEIGTH
    global SCREENSIZE
    global game_over

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

        if keys[pygame.K_RIGHT]:
            if direction != "LEFT":
                direction = "RIGHT"
        elif keys[pygame.K_LEFT]:
            if direction != "RIGHT":
                direction = "LEFT"
        elif keys[pygame.K_UP]:
            if direction != "DOWN":
                direction = "UP"
        elif keys[pygame.K_DOWN]:
            if direction != "UP":
                direction = "DOWN"

        if(start == False):
            pantallaStart(win, keys)

        if start == True and game_over == False and pause == False:
            moveSnake(direction, snake, VEL)

            drawSnake(win, snake, PIXEL_WIDTH, PIXEL_HEIGTH)

            drawFood(win, food, PIXEL_WIDTH, PIXEL_HEIGTH)

            if snake[0] == food[0]:
                growSnake(snake, PIXEL_WIDTH, PIXEL_HEIGTH)

                teleportFood(food, PIXEL_WIDTH, PIXEL_HEIGTH)

            game_over = outOfBounds(snake, SCREENSIZE)

            colisionSerpiente(snake)

        gameOver(win)

        pausar(win, keys)

        reiniciar(keys)

        salir(keys)

        puntos(snake, win)

    pygame.quit()


main()