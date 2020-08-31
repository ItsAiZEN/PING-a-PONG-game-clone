import pygame
import sys
import random

# Constants
rand_i = random.randrange(360, 780)
constant_i = 1
power_up_len = 0

# Sizes
sc_width = 650
sc_height = 900
border = 3
pd_width = 130
pd_height = 18
ball_size = 34
space_bt_pd = 6
power_up_size = 48

# Colors
white = (235, 235, 235)

# Speeds
ai_speed = 4
pd_constant_speed = 6
paddle_speed = 0
ball_speed = -4
ball_sp_x = ball_speed
ball_sp_y = int(ball_speed / 0.5)
init_sp = 60

# Score
score = 0
ai_score = 0

# Boolean values
power_up_status = False
running = True
bg_music_state = True

# Initializing PyGame and Sound modules
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Sounds importing and settings
hit_sound = pygame.mixer.Sound('.\\Sounds\\hit.ogg')
hit_sound.set_volume(0.5)
bg_music = pygame.mixer.Sound('.\\Sounds\\bg_music.ogg')
bg_music.set_volume(0.12)
click_sound = pygame.mixer.Sound('.\\Sounds\\click.ogg')
click_sound.set_volume(0.7)
power_up_sound = pygame.mixer.Sound('.\\Sounds\\powerup.ogg')
power_up_sound.set_volume(0.5)
win_sound = pygame.mixer.Sound('.\\Sounds\\win.ogg')
win_sound.set_volume(0.7)
point_earned = pygame.mixer.Sound('.\\Sounds\\point.ogg')
point_earned.set_volume(0.4)
point_lost = pygame.mixer.Sound('.\\Sounds\\point_lost.ogg')
point_lost.set_volume(0.4)
safety_used = pygame.mixer.Sound('.\\Sounds\\safety.ogg')

# Image importing and setting
icon = pygame.image.load('.\\Sprites\\icon.png')
paddle_image = pygame.image.load('.\\Sprites\\paddle1.png')
long_paddle_image = pygame.image.load('.\\Sprites\\paddle_long1.png')
short_paddle_image = pygame.image.load('.\\Sprites\\paddle_short1.png')
background = pygame.image.load('.\\Sprites\\background6.png')
ball_img = pygame.image.load('.\\Sprites\\ball.png')
power_up_img = pygame.image.load('.\\Sprites\\powerup.png')
large_ball_img = pygame.image.load('.\\Sprites\\ball_big.png')
small_ball_img = pygame.image.load('.\\Sprites\\ball_small.png')
borders_img = pygame.image.load('.\\Sprites\\borders1.png')
safety_net_img = pygame.image.load('.\\Sprites\\safety_net.png')
play_btn = pygame.image.load('.\\Sprites\\play_unpressed.png')
play_btn_pressed = pygame.image.load('.\\Sprites\\play.png')
music_btn = pygame.image.load('.\\Sprites\\music_unpressed.png')
music_btn_pressed = pygame.image.load('.\\Sprites\\music.png')
exit_btn = pygame.image.load('.\\Sprites\\exit_unpressed.png')
exit_btn_pressed = pygame.image.load('.\\Sprites\\exit.png')
menu_bg = pygame.image.load('.\\Sprites\\background3.png')
timer_bg = pygame.image.load('.\\Sprites\\background4.png')
current_paddle_image = paddle_image
current_ai_image = paddle_image
current_ball_image = ball_img

# Playing background music indefinitely
bg_music.play(-1)


# Creating clock object
clock = pygame.time.Clock()

# Screen initializing
screen = pygame.display.set_mode((sc_width, sc_height))

# Window Header
pygame.display.set_caption('PING! by AiZEN')
pygame.display.set_icon(icon)

# Game objects
ai = pygame.Rect(int(sc_width / 2) - int(pd_width / 2), space_bt_pd + border, pd_width, pd_height)
paddle = pygame.Rect(int(sc_width / 2) - int(pd_width / 2), (sc_height - pd_height - border - space_bt_pd), pd_width,
                     pd_height)
ball = pygame.Rect(sc_width - 50, sc_height - 50, ball_size, ball_size)
power_up = pygame.Rect(sc_width + 50, sc_height + 50, power_up_size, power_up_size)
safety_net = pygame.Rect(sc_width + 50, sc_height + 50, 620, 18)
button1 = pygame.Rect(205, 330, 240, 90)
button2 = pygame.Rect(205, 445, 240, 90)
button3 = pygame.Rect(205, 560, 240, 90)


# Initializes text font and location for the timer function
def start_timer(message):
    font_style = pygame.font.Font('Fonts/font1.otf', 80)
    time_os = font_style.render(str(message), True, white)
    screen.blit(time_os, (int(sc_width / 2 - 120), int(sc_height / 2 - 50)))
    pygame.display.flip()
    pygame.time.delay(160)


# Counts down before tossing a new ball
def st_timer():
    pygame.time.delay(230)
    screen.blit(timer_bg, (0, 0))
    start_timer('3')
    screen.blit(timer_bg, (0, 0))
    start_timer('3.')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..2')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..2.')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..2..')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..2..1')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..2..1.')
    screen.blit(timer_bg, (0, 0))
    start_timer('3..2..1..')
    pygame.time.delay(200)


# Counts and displays the score
def score_counter():
    font_style = pygame.font.Font('Fonts/font1.otf', 32)
    score_os = font_style.render(str(ai_score), True, white)
    screen.blit(score_os, [int(sc_width / 2 - 2), int(sc_height / 2 - 45)])
    score_os = font_style.render(str(score), True, white)
    screen.blit(score_os, [int(sc_width / 2 - 2), int(sc_height / 2 + 10)])


# Ball movement including colliding with walls paddles and losing
def ball_movement():
    global ball_sp_x, ball_sp_y, score, paddle_speed, running, ai_score, constant_i, power_up_len, power_up_status, \
        current_paddle_image, current_ai_image, current_ball_image
    # Moves the ball X and Y by the "speed" of them
    ball.x += ball_sp_x
    ball.y += ball_sp_y
    # If ball hits left wall change directions
    if ball.left <= 0 + border and ball_sp_x < 0:
        ball_sp_x *= -1
        pygame.mixer.Sound.play(hit_sound)
    # If ball hits right wall change directions
    if ball.right >= sc_width - border and ball_sp_x > 0:
        ball_sp_x *= -1
        pygame.mixer.Sound.play(hit_sound)
    # If ball hits the paddle change direction and degree by place on paddle, make a sound
    if ball.colliderect(paddle) and ball_sp_y > 0:
        ball_sp_x = int(((paddle.centerx - ball.centerx) * ball_speed) / 50)
        ball_sp_y *= -1
        pygame.mixer.Sound.play(hit_sound)
    # If ball hits the paddle change direction and degree by place on paddle, make a sound
    if ball.colliderect(ai) and ball_sp_y < 0:
        ball_sp_x = int(((ai.centerx - ball.centerx) * ball_speed) / 50)
        ball_sp_y *= -1
        pygame.mixer.Sound.play(hit_sound)
    # If lost by player
    if ball.bottom >= sc_height - border - space_bt_pd:
        if ball.colliderect(safety_net):
            ball_sp_y *= -1
            pygame.mixer.Sound.play(safety_used)
            safety_net.x = sc_width + 50
            safety_net.y = sc_height + 50
        else:
            # Reset all variables that might have changed by power-ups
            pygame.mixer.Sound.play(point_lost)
            constant_i = 1
            ai_score += 1
            power_up_len = 0
            power_up_status = False
            paddle.width = 130
            ai.width = 130
            safety_net.x = sc_width + 50
            safety_net.y = sc_height + 50
            ball.height = ball_size
            ball.width = ball_size
            current_paddle_image = paddle_image
            current_ai_image = paddle_image
            current_ball_image = ball_img
            # If game is not ended, toss the ball again
            if ai_score < 5:
                paddle.centerx = int(sc_width / 2)
                ai.centerx = int(sc_width / 2)
                ball.center = (sc_width - 50, sc_height - 50)
                pygame.display.flip()
                st_timer()
                ball_sp_y = 2 * ball_speed  # random.choice((-1, 1))
                ball_sp_x = ball_speed
        # If game is ended, display loss screen, ask for rematch or quit, place ball and paddles at beginning's stage
            if ai_score == 5:
                running = False
                screen.blit(background, (0, 0))
                score_style = pygame.font.Font('Fonts/font1.otf', 75)
                score_os = score_style.render('You Lost!', True, white)
                screen.blit(score_os, (int(sc_width / 2 - 155), int(sc_height / 2 - 245)))
                record_os = score_style.render('Score: ' + str(score) + ':' + str(ai_score), True, white)
                screen.blit(record_os, (int(sc_width / 2 - 165), int(sc_height / 2 - 360)))
                again_style = pygame.font.Font('Fonts/font1.otf', 50)
                replay_os = again_style.render('press Enter to replay', True, white)
                quit_os = again_style.render('press Esc to quit', True, white)
                screen.blit(replay_os, (int(sc_width / 6 - 25), int(sc_height / 4 + 145)))
                screen.blit(quit_os, (int(sc_width / 6 + 30), int(sc_height / 3 + 195)))
                score = 0
                loop = True
                while loop:
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_RETURN:
                                ball.center = (sc_width - 50, sc_height - 50)
                                ball_sp_y = 2 * ball_speed
                                ball_sp_x = ball_speed
                                paddle.centerx = int(sc_width / 2)
                                ai.centerx = int(sc_width / 2)
                                score = 0
                                ai_score = 0
                                loop = False
                                running = True
                            # The lines below fix a bug where if keys are held down while replaying the speed remains
                                pressed = pygame.key.get_pressed()
                                if pressed[pygame.K_LEFT]:
                                    paddle_speed = -pd_constant_speed
                                elif pressed[pygame.K_RIGHT]:
                                    paddle_speed = pd_constant_speed
                                else:
                                    paddle_speed = 0
                                st_timer()
                                game_loop()
                            elif events.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                    pygame.display.flip()
                    clock.tick(60)


# AI movement and logic, includes delay and random speed
def ai_movement():
    global ball_sp_x, ball_sp_y, ball_speed, score, paddle_speed, running, ai_score, constant_i, power_up_len, \
        power_up_status, ai_speed, current_paddle_image, current_ai_image, current_ball_image
    # This gives the AI random speeds, and makes the game more random and less predictable
    ai_speed = random.randrange(3, 6)
    # This moves the AI paddle by the "speed" of it
    ai.x += ai_speed
    # If the left side of the paddle is more to the right than the center of the ball, move left
    if ai.left > ball.centerx:
        ai.left -= ai_speed
    # If the right side of the paddle is more to the left than the center of the ball, move right
    if ai.right > ball.centerx:
        ai.right -= ai_speed
    # Keeps the AI paddle within the borders
    if ai.left <= border:
        ai.left = border
    # Keeps the AI paddle within the borders
    if ai.right >= sc_width - border:
        ai.right = sc_width - border
    # If AI loses a point
    if ball.top <= border + space_bt_pd:
        if ball.colliderect(safety_net):
            ball_sp_y *= -1
            pygame.mixer.Sound.play(safety_used)
            safety_net.x = sc_width + 50
            safety_net.y = sc_height + 50
        else:
            # Reset all variables that might have changed by power-ups
            if score < 4:
                pygame.mixer.Sound.play(point_earned)
            constant_i = 1
            score += 1
            power_up_len = 0
            power_up_status = False
            paddle.width = 130
            ai.width = 130
            safety_net.x = sc_width + 50
            safety_net.y = sc_height + 50
            ball.height = ball_size
            ball.width = ball_size
            current_paddle_image = paddle_image
            current_ai_image = paddle_image
            current_ball_image = ball_img
            # If game is not ended, toss the ball again
            if score < 5:
                paddle.centerx = int(sc_width / 2)
                ai.centerx = int(sc_width / 2)
                ball.center = (sc_width - 50, sc_height - 50)
                pygame.display.flip()
                st_timer()
                ball_sp_y = 2 * ball_speed
                ball_sp_x = ball_speed
            # If game is ended, display win screen, ask for rematch or quit, place ball and paddles at beginning's stage
            if score == 5:
                pygame.mixer.Sound.play(win_sound)
                running = False
                ball.center = (sc_width - 50, sc_height - 50)
                ball_sp_y = 2 * ball_speed
                ball_sp_x = ball_speed
                screen.blit(background, (0, 0))
                score_style = pygame.font.Font('Fonts/font1.otf', 75)
                score_os = score_style.render('You Won!', True, white)
                screen.blit(score_os, (int(sc_width / 2 - 165), int(sc_height / 2 - 245)))
                record_os = score_style.render('Score: ' + str(score) + ':' + str(ai_score), True, white)
                screen.blit(record_os, (int(sc_width / 2 - 165), int(sc_height / 2 - 360)))
                again_style = pygame.font.Font('Fonts/font1.otf', 50)
                replay_os = again_style.render('press Enter to replay', True, white)
                quit_os = again_style.render('press Esc to quit', True, white)
                screen.blit(replay_os, (int(sc_width / 6 - 35), int(sc_height / 4 + 145)))
                screen.blit(quit_os, (int(sc_width / 6 + 40), int(sc_height / 3 + 195)))
                score = 0
                loop = True
                while loop:
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_RETURN:
                                paddle.centerx = int(sc_width / 2)
                                score = 0
                                ai_score = 0
                                loop = False
                                running = True
                            # The lines below fix a bug where if keys are held down while replaying the speed remains
                                pressed = pygame.key.get_pressed()
                                if pressed[pygame.K_LEFT]:
                                    paddle_speed = -pd_constant_speed
                                elif pressed[pygame.K_RIGHT]:
                                    paddle_speed = pd_constant_speed
                                else:
                                    paddle_speed = 0
                                st_timer()
                                game_loop()
                            elif events.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                    pygame.display.flip()
                    clock.tick(60)


# Blocks the paddle from moving off screen and also lets the paddle move in screen
def paddle_movement():
    paddle.x += paddle_speed
    if paddle.left <= border:
        paddle.left = border
    if paddle.right >= sc_width - border:
        paddle.right = sc_width - border


# Places the power-up object in the X and Y the function is given
def locate_power_up(x, y):
    global rand_i
    rand_i = random.randrange(360, 780)
    power_up.x = x
    power_up.y = y


# Moves the power-up down until it is off screen
def move_power_up():
    global power_up_len
    if power_up.y < sc_height:
        power_up.y += 4


# Makes the power-ups objects give the power-up ability
def use_power_up():
    global paddle_speed, power_up_status, power_up_len, score, ai_score, current_paddle_image, current_ai_image, \
        current_ball_image
    if power_up.colliderect(paddle):
        pygame.mixer.Sound.play(power_up_sound)
        power_up.x = 1000
        power_up.y = 1000
        power_up_status = True
        i = random.randrange(1, 8)
        if i == 1:  # Shorter paddle
            paddle.width = int(paddle.width * 0.5)
            current_paddle_image = short_paddle_image
        if i == 2:  # Shorter AI paddle
            ai.width = int(ai.width * 0.5)
            current_ai_image = short_paddle_image
        if i == 3:  # Longer paddle
            paddle.width = int(paddle.width * 1.6)
            current_paddle_image = long_paddle_image
        if i == 4:  # Longer AI paddle
            ai.width = int(ai.width * 1.6)
            current_ai_image = long_paddle_image
        if i == 5:  # Smaller ball
            ball.width = int(ball.width * 0.5)
            ball.height = int(ball.height * 0.5)
            current_ball_image = small_ball_img
        if i == 6:  # Larger ball
            ball.width *= 2
            ball.height *= 2
            current_ball_image = large_ball_img
        if i == 7:  # Safety net for AI
            safety_net.x = border
            safety_net.y = border + space_bt_pd
        if i == 8:  # Safety net for Player
            safety_net.x = border
            safety_net.y = sc_height - border - space_bt_pd - pd_height


# Draws the game objects on screen
def draw_objects():
    screen.blit(safety_net_img, safety_net)
    screen.blit(current_ball_image, ball)
    screen.blit(current_paddle_image, paddle)
    screen.blit(current_ai_image, ai)
    screen.blit(power_up_img, power_up)
    screen.blit(borders_img, (0, 0))


# Loop in which all game happens, infinite loop until lost, gets keyboard input for movement
def game_loop():
    global running, paddle_speed, rand_i, constant_i, power_up_len, power_up_status, current_paddle_image,\
        current_ai_image, current_ball_image
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            # If the event was key pressed
            if event.type == pygame.KEYDOWN:
                # This will pause the game
                if event.key == pygame.K_SPACE:
                    score_style = pygame.font.Font('Fonts/font1.otf', 80)
                    score_os = score_style.render('Paused', True, white)
                    screen.blit(score_os, (int(sc_width / 2 - 130), int(sc_height / 2 - 150)))
                    pygame.display.flip()
                    pygame.mixer.Sound.play(click_sound)
                    pygame.time.delay(100)
                    # The lines below fix a bug where if keys are held down while resuming the speed remains
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_LEFT]:
                        if paddle_speed == 0:
                            paddle_speed = pd_constant_speed
                        else:
                            paddle_speed = 0
                    elif pressed[pygame.K_RIGHT]:
                        if paddle_speed == 0:
                            paddle_speed = -pd_constant_speed
                        else:
                            paddle_speed = 0
                    else:
                        paddle_speed = 0
                    pause = True
                    while pause:
                        for happening in pygame.event.get():
                            if happening.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if happening.type == pygame.KEYDOWN:
                                # This will unpause the game
                                if happening.key == pygame.K_SPACE:
                                    pygame.mixer.Sound.play(click_sound)
                                    pause = False
                                    # The lines below fix a bug where speed remains after resuming
                                    pressed = pygame.key.get_pressed()
                                    if pressed[pygame.K_LEFT]:
                                        paddle_speed -= pd_constant_speed
                                    elif pressed[pygame.K_RIGHT]:
                                        paddle_speed += pd_constant_speed
                                elif happening.key == pygame.K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # The lines before raises or lowers the speed of the paddle if up or down keys are pressed
                pressed4 = pygame.key.get_pressed()
                if paddle_speed == int(2 * pd_constant_speed):
                    if pressed4[pygame.K_UP] and pressed4[pygame.K_RIGHT]:
                        continue
                    elif pressed4[pygame.K_RIGHT]:
                        paddle_speed = pd_constant_speed
                    else:
                        paddle_speed = 0
                if paddle_speed == int(2 * -pd_constant_speed):
                    if pressed4[pygame.K_UP] and pressed4[pygame.K_LEFT]:
                        continue
                    elif pressed4[pygame.K_LEFT]:
                        paddle_speed = -pd_constant_speed
                    else:
                        paddle_speed = 0
                if paddle_speed == int(0.5 * pd_constant_speed):
                    if pressed4[pygame.K_DOWN] and pressed4[pygame.K_RIGHT]:
                        continue
                    elif pressed4[pygame.K_RIGHT]:
                        paddle_speed = pd_constant_speed
                    else:
                        paddle_speed = 0
                if paddle_speed == int(0.5 * -pd_constant_speed):
                    if pressed4[pygame.K_DOWN] and pressed4[pygame.K_LEFT]:
                        continue
                    elif pressed4[pygame.K_LEFT]:
                        paddle_speed = -pd_constant_speed
                    else:
                        paddle_speed = 0
                pressed1 = pygame.key.get_pressed()
                if event.key == pygame.K_RIGHT:
                    paddle_speed = 0
                    if pressed1[pygame.K_UP]:
                        paddle_speed += int(2 * pd_constant_speed)
                    elif pressed1[pygame.K_DOWN]:
                        paddle_speed += int(0.5 * pd_constant_speed)
                    else:
                        paddle_speed += pd_constant_speed
                if event.key == pygame.K_LEFT:
                    paddle_speed = 0
                    if pressed1[pygame.K_UP]:
                        paddle_speed -= int(2 * pd_constant_speed)
                    elif pressed1[pygame.K_DOWN]:
                        paddle_speed -= int(0.5 * pd_constant_speed)
                    else:
                        paddle_speed -= pd_constant_speed
            pressed2 = pygame.key.get_pressed()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if not pressed2[pygame.K_LEFT]:
                        paddle_speed = 0
                    else:
                        paddle_speed = -pd_constant_speed
                if event.key == pygame.K_LEFT:
                    if not pressed2[pygame.K_RIGHT]:
                        paddle_speed = 0
                    else:
                        paddle_speed = pd_constant_speed
            pressed3 = pygame.key.get_pressed()
            if pressed3[pygame.K_UP] and paddle_speed == pd_constant_speed:
                paddle_speed = int(2 * pd_constant_speed)
            elif pressed3[pygame.K_DOWN] and paddle_speed == pd_constant_speed:
                paddle_speed = int(0.5 * pd_constant_speed)
            elif pressed3[pygame.K_UP] and paddle_speed == -pd_constant_speed:
                paddle_speed = -int(2 * pd_constant_speed)
            elif pressed3[pygame.K_DOWN] and paddle_speed == -pd_constant_speed:
                paddle_speed = -int(0.5 * pd_constant_speed)
        # If there is no power-up active if the random number finally reached activate power-up
        if not power_up_status:
            if constant_i == rand_i:
                constant_i = 0
                rand_i = random.randrange(360, 780)
                x = random.randrange(border, sc_width - border - power_up_size)
                y = random.randrange(int(sc_height / 5), int(sc_height / 3))
                locate_power_up(x, y)
        move_power_up()
        use_power_up()
        ball_movement()
        paddle_movement()
        # When power-up is not activated the counter for the random timing keeps on going
        if not power_up_status:
            constant_i += 1
        # This will counts the time for the power-up and ends it after certain amount of loops
        if power_up_status:
            power_up_len += 1
            if power_up_len > 720:
                power_up_len = 0
                power_up_status = False
                # This resets the paddles sizes after the power-up is over
                paddle.width = 130
                ai.width = 130
                safety_net.x = sc_width + 50
                safety_net.y = sc_height + 50
                ball.height = ball_size
                ball.width = ball_size
                current_paddle_image = paddle_image
                current_ai_image = paddle_image
                current_ball_image = ball_img
        # This creates a "delay" for the AI before it starts moving
        if ball.top - ai.bottom < 655:
            ai_movement()
        screen.blit(background, (0, 0))
        score_counter()
        draw_objects()
        # updates the screen
        pygame.display.flip()
        # If player has an advantage over the AI the game will be faster and therefore harder
        if (score - ai_score) > 0:
            clock.tick(init_sp + (int((score - ai_score) * 8)))  # amount of "FPS"
        else:
            clock.tick(init_sp)  # amount of "FPS"


# Menu in which the game loop will be called upon starting a new game
def main():
    global bg_music_state
    menu = True
    while menu:
        click = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu_event.type == pygame.KEYDOWN:
                if menu_event.key == pygame.K_RETURN:
                    menu = False
                    st_timer()
                    game_loop()
                if menu_event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if menu_event.type == pygame.MOUSEBUTTONDOWN:
                if menu_event.button == 1:
                    click = True
        screen.blit(menu_bg, (0, 0))
        if button1.collidepoint(mouse_x, mouse_y):
            screen.blit(play_btn_pressed, button1)
            if click:
                pygame.mixer.Sound.play(click_sound)
                st_timer()
                game_loop()
        else:
            screen.blit(play_btn, button1)
        if button2.collidepoint(mouse_x, mouse_y):
            screen.blit(music_btn_pressed, button2)
            if click:
                pygame.mixer.Sound.play(click_sound)
                if bg_music_state:
                    bg_music_state = False
                    bg_music.stop()
                else:
                    bg_music_state = True
                    bg_music.play(-1)
        else:
            screen.blit(music_btn, button2)
        if button3.collidepoint(mouse_x, mouse_y):
            screen.blit(exit_btn_pressed, button3)
            if click:
                pygame.mixer.Sound.play(click_sound)
                pygame.time.wait(210)
                pygame.quit()
                sys.exit()
        else:
            screen.blit(exit_btn, button3)
        menu_style = pygame.font.Font('Fonts/font1.otf', 18)
        play_os = menu_style.render('MOVE FASTER/SLOWER USING UP/DOWN KEYS!', True, white)
        menu_pause_os = menu_style.render('PAUSE/RESUME WITH SPACE KEY!', True, white)
        screen.blit(play_os, (95, 745))
        screen.blit(menu_pause_os, (165, 810))
        pygame.display.flip()  # Update the screen
        clock.tick(60)


# Calling the main function if the program is run instead of imported
if __name__ == "__main__":
    main()
