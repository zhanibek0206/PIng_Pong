import pygame as pg
import random

pg.init()
pg.font.init()

TITLE = "Half Pong"
WITH = 800
HEIGHT = 480

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 15
PLATFORM_SPEED = 10
platform_rect = pg.rect.Rect(WITH / 2 - PLATFORM_WIDTH / 2,
                             HEIGHT - PLATFORM_HEIGHT * 2,
                             PLATFORM_WIDTH, PLATFORM_HEIGHT)

CIRCLE_RADIUS = 15
CIRCLE_SPEED = 10
circle_first_collide = False
circle_x_speed = 0
circle_y_speed = CIRCLE_SPEED
circle_rect = pg.rect.Rect(WITH / 2 - CIRCLE_RADIUS,
                           HEIGHT / 2 - CIRCLE_RADIUS,
                           CIRCLE_RADIUS * 2,
                           CIRCLE_RADIUS * 2)

score = 0

ARIAL_FONT_PATH = pg.font.match_font('arial')
ARIAL_FONT_48 = pg.font.Font(ARIAL_FONT_PATH, 48)
ARIAL_FONT_36 = pg.font.Font(ARIAL_FONT_PATH, 36)

screen = pg.display.set_mode([WITH, HEIGHT])
pg.display.set_caption(TITLE)

clock = pg.time.Clock()

game_over = False
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            continue
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                continue
            elif event.key == pg.K_r:
                game_over = False

                platform_rect.centerx = WITH / 2
                platform_rect.bottom = HEIGHT - PLATFORM_HEIGHT

                circle_rect.center = [WITH / 2, HEIGHT / 2]

                circle_x_speed = 0
                circle_y_speed = CIRCLE_SPEED
                circle_first_collide = False

                score = 0

    screen.fill(BLACK)

    if not game_over:
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            platform_rect.x -= PLATFORM_SPEED
        elif keys[pg.K_d]:
            platform_rect.x += PLATFORM_SPEED

        if platform_rect.colliderect(circle_rect):
            if not circle_first_collide:
                if random.randint(0, 1) == 0:
                    circle_x_speed = CIRCLE_SPEED
                else:
                    circle_x_speed = -CIRCLE_SPEED

                circle_first_collide = True

            circle_y_speed = -CIRCLE_SPEED
            score += 1

    pg.draw.rect(screen, WHITE, platform_rect)

    circle_rect.x += circle_x_speed
    circle_rect.y += circle_y_speed

    if circle_rect.bottom >= HEIGHT:
        game_over = True
        circle_y_speed = -CIRCLE_SPEED
    elif circle_rect.top <= 0:
        circle_y_speed = CIRCLE_SPEED
    elif circle_rect.left <= 0:
        circle_x_speed = CIRCLE_SPEED
    elif circle_rect.right >= WITH:
        circle_x_speed = -CIRCLE_SPEED

    pg.draw.circle(screen, WHITE, circle_rect.center, CIRCLE_RADIUS)

    score_surface = ARIAL_FONT_48.render(str(score), True, WHITE)
    if not game_over:
        screen.blit(score_surface, [WITH / 2 - score_surface.get_width() / 2, 15])
    else:
        retry_surface = ARIAL_FONT_36.render('press R to restart', True, WHITE)
        screen.blit(score_surface, [WITH / 2 - score_surface.get_width() / 2, HEIGHT / 3])
        screen.blit(retry_surface, [WITH / 2 - score_surface.get_width() / 2,
                                    HEIGHT / 3 + score_surface.get_height()])

    clock.tick(FPS)

    pg.display.flip()

pg.quit()
