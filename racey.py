import pygame
import random
import time

pygame.init()

# display definitions
display_width = 800
display_height = 600

car_width = 99
car_height = 115

# global definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 200, 0)
FONT = 'freesansbold.ttf'

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Zoom!")
clock = pygame.time.Clock()

carImg = pygame.image.load('car.png')


# methods
def draw_car(a, b):
    gameDisplay.blit(carImg, (a, b))

def create_thing(name, color):
    box = random.randrange(25, 100)
    name = {'w' : box,
            'h' : box,
            'x' : random.randrange(50, (display_width - box - 50)),
            'y' : 0 - box,
            's' : random.randrange(3, 10),
            'c' : color}
    return name

def draw_thing(dict):
    pygame.draw.rect(gameDisplay, dict['c'], [dict['x'], dict['y'], dict['w'], dict['h']])

def draw_road(a):
    pygame.draw.rect(gameDisplay, YELLOW, [(display_width*.5)+10, 0, 10, 600])
    pygame.draw.rect(gameDisplay, YELLOW, [(display_width*.5)-10, 0, 10, 600])

    for i in range(0, 14):
        if i % 2 == 0:
            pygame.draw.rect(gameDisplay, RED, [0, -100+a+(i*50), 50, 50])
            pygame.draw.rect(gameDisplay, RED, [display_width-50, -100+a+(i*50), 50, 50])
        else:
            pygame.draw.rect(gameDisplay, WHITE, [0, -100+a+(i*50), 50, 50])
            pygame.draw.rect(gameDisplay, WHITE, [display_width-50, -100+a+(i*50), 50, 50])

    for i in range(0, 14):
        if i % 2 == 0:
            pygame.draw.rect(gameDisplay, WHITE, [(display_width)*.25+20, -100+a+(i*50), 10, 50])
            pygame.draw.rect(gameDisplay, WHITE, [(display_width)*.75-20, -100+a+(i*50), 10, 50])


def new(dict):
    new = create_thing(dict, dict['c'])
    return new

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text, size, color):
    largeText = pygame.font.Font(FONT, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def message_box(x, y, w, h):
    dx = (x*display_width) - int(w/2)
    dy = (y*display_height) - int(h/2)

    pygame.draw.rect(gameDisplay, BLACK, [dx, dy, w, h])
    pygame.draw.rect(gameDisplay, WHITE, [dx+1, dy+1, w-2, h-2])
    pygame.draw.rect(gameDisplay, GRAY, [dx+3, dy+3, w-6, h-6])
    pygame.draw.rect(gameDisplay, WHITE, [dx+5, dy+5, w-10, h-10])
    pygame.draw.rect(gameDisplay, BLACK, [dx+7, dy+7, w-14, h-14])

def crash(score):
    message_box(.5, .5, 400, 300)
    message_display("CRASH!", 100, RED)
    time.sleep(1)

    message_box()
    message_display( "Score: " + str(score), 100, GREEN)
    time.sleep(1)

    game_loop()

def game_loop():

    STATE = 'DRIVING'
    score = 0

    # car start pos coords
    x = (display_width * .425)
    y = (display_height * .75)
    x_change = 0
    y_change = 0
    car_vx = 0
    car_vy = 0
    PLAYER_SPEED = 5
    speed = 5
    road = 0

    rock = create_thing('rock',  RED)
    cookie = create_thing('cookie', GREEN)
    #line = create_thing(line)

    gameExit = False

    while not gameExit:
        STATE == 'DRIVING'

        if STATE == 'DRIVING':
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key ==pygame.K_a:
                        x_change = -(PLAYER_SPEED)

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        x_change = PLAYER_SPEED

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        y_change = -(PLAYER_SPEED)

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        y_change = PLAYER_SPEED

                    if car_vx != 0 and car_vy != 0:
                        car_vx *= .7071
                        car_vy *= .7071

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or \
                        event.key == pygame.K_RIGHT:
                            x_change = 0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN:
                            y_change = 0

            x += x_change
            y += y_change

            # draw objects
            gameDisplay.fill(GRAY)

            draw_road(road)
            if road < 100:
                road += speed
            else:
                road = 0

            draw_thing(rock)
            draw_thing(cookie)
            draw_car(x, y)

            rock['y'] += rock['s']
            cookie['y'] += cookie['s']

            if x > display_width - car_width - 50 or x < 50:
                STATE = 'CRASH'

            if y >= display_height - car_height:
                y -= 5

            if y <= 0:
                y += 5

            if y < (rock['y']+rock['h']) and (y + car_height) > (rock['y']+rock['h']) or \
                    y < rock['y'] and (y+car_height) > (rock['y']):
                if x > rock['x'] and x < (rock['x']+rock['w']) or \
                        (x+car_width) > rock['x'] and (x+car_width) < (rock['x']+rock['w']) or \
                        x < rock['x'] and (x+car_width) > (rock['x']+rock['w']):

                    STATE = 'CRASH'

            if rock['y'] > display_height:
                rock = new(rock)
                draw_thing(rock)

            if y < (cookie['y']+cookie['h']) and (y + car_height) > (cookie['y']+cookie['h']) or \
                    y < cookie['y'] and (y+car_height) > (cookie['y']):
                if x > cookie['x'] and x < (cookie['x']+cookie['w']) or \
                        (x+car_width) > cookie['x'] and (x+car_width) < (cookie['x']+cookie['w']) or \
                        x <cookie['x'] and (x+car_width) > (cookie['x']+cookie['w']):

                    cookie = new(cookie)
                    draw_thing(cookie)
                    score += 1

            if cookie['y'] > display_height:
                cookie = new(cookie)
                draw_thing(cookie)

            pygame.display.update()

        elif STATE == 'CRASH':
            crash(score)
            pygame.display.update()

        #elif STATE == MENU
            #menu()

        clock.tick(60)

game_loop()
pygame.quit()
quit()
