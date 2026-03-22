from pygame import *
from enteties_for_multi_shooter import *
from config_for_muli_shooter import *

init()

blaster_start_ticks = time.get_ticks()

window = display.set_mode((win_width, win_height))
player1 = Player(player1_img_right, 100, 690, 65, 130, 3, 125_000, 55, 20)
player2 = Player(player2_img_1_left, 600, 690, 65, 130, 3, 125_000, 55, 20)
blaster = EnergyBlaster(blaster_image_right, 800, 750, 65, 65, 0, 500)
mixer.init()
font.init()

big_font = font.Font(None, 200)
small_font = font.Font(None, 100)

game = True
game_over = False
clock = time.Clock()

while game:
    window.blit(background, (0, 0))
    player1.reset(window)
    player2.reset(window)
    blaster_reset = True if time.get_ticks() - blaster_start_ticks >= BLASTER_HIDEN_DURATION else False
    p1_margin = player1.rect.inflate(40, 40)
    p2_margin = player2.rect.inflate(40, 40)

    player1.draw_health_bar(100, 5, window, (0, 255, 0))
    player2.draw_health_bar(100, 5, window, (255, 255, 0))

    player1.draw_xp_bar(200, 20, window, (255, 200, 0))
    player2.draw_xp_bar(200, 20, window, (0, 0, 255))
    for ev in event.get():
        if ev.type == QUIT:
            game = False

    if not game_over:
        keys = key.get_pressed()
        if blaster_reset:
            blaster.reset(window)
        if resolve_collision(player1, blaster.rect) and blaster.owner is None and blaster_reset:
            blaster_collected_p1 = 1

        elif resolve_collision(player2, blaster.rect) and blaster.owner is None and blaster_reset:
            blaster_collected_p2 = 1

        if keys[K_d] and player1.rect.x <= (win_width - 85):
            player1.image = transform.scale(image.load(player1_img_right), (player1.width, player1.height))
            old_x = player1.rect.x
            player1.rect.x += player1.speed
            if blaster_collected_p1 == 1:
                blaster.rect.x = player1.rect.x + 60
                blaster.owner = player1
                blaster.image = transform.scale(image.load(blaster_image_right), (blaster.width, blaster.height))
                blaster.bullet.image = transform.scale(image.load(energy_bullet_right), (blaster.bullet.width, blaster.bullet.height))
            if resolve_collision(player1, player2):
                player1.rect.x = old_x

        if keys[K_a] and player1.rect.x >= 0:
            player1.image = transform.scale(image.load(player1_img_left), (player1.width, player1.height))
            old_x = player1.rect.x
            player1.rect.x -= player1.speed
            if blaster_collected_p1 == 1:
                blaster.rect.x = player1.rect.x - 60
                blaster.owner = player1
                blaster.image = transform.scale(image.load(blaster_image_left), (blaster.width, blaster.height))
                blaster.bullet.image = transform.scale(image.load(energy_bullet_left), (blaster.bullet.width, blaster.bullet.height))
            if resolve_collision(player1, player2):
                player1.rect.x = old_x

        if keys[K_x]:
            player1.start_jump()
        
        if keys[K_e]:
            if resolve_collision(p1_margin, p2_margin):
                player1.attack(player2)

        if keys[K_RIGHT] and player2.rect.x <= (win_width - 100):
            player2.image = transform.scale(image.load(player2_img_1_right), (player2.width, player2.height))
            old_x = player2.rect.x
            player2.rect.x += player2.speed
            if blaster_collected_p2 == 1:
                blaster.rect.x = player2.rect.x + 60
                blaster.owner = player2
                blaster.image = transform.scale(image.load(blaster_image_right), (blaster.width, blaster.height))
                blaster.bullet.image = transform.scale(image.load(energy_bullet_right), (blaster.bullet.width, blaster.bullet.height))
            if resolve_collision(player2, player1):
                player2.rect.x = old_x


        if keys[K_LEFT] and player2.rect.x >= 0:
            player2.image = transform.scale(image.load(player2_img_1_left), (player2.width, player2.height))
            old_x = player2.rect.x
            player2.rect.x -= player2.speed
            if blaster_collected_p2 == 1:
                blaster.rect.x = player2.rect.x - 60
                blaster.owner = player2
                blaster.image = transform.scale(image.load(blaster_image_left), (blaster.width, blaster.height))
                blaster.bullet.image = transform.scale(image.load(energy_bullet_left), (blaster.bullet.width, blaster.bullet.height))
            if resolve_collision(player2, player1):
                player2.rect.x = old_x


        if keys[K_SPACE]:
            player2.start_jump()
        
        if keys[K_RSHIFT]:
            if resolve_collision(p2_margin, p1_margin):
                player2.attack(player1)

        if keys[K_q] and blaster_collected_p1 == 1:
            if keys[K_a]:
                blaster.shoot(window, player2, -690)
                static_bullet_direction = 0
            if keys[K_d]:
                static_bullet_direction = 38
                blaster.shoot(window, player2, 60)
            else:
                blaster.bullet.image = transform.scale(image.load(static_bullet), (30, 20))
                window.blit(blaster.bullet.image, (blaster.rect.x + static_bullet_direction, blaster.rect.y + 20))
            blaster.bullet.update()
        else:
            blaster.bullet.active = False
        
        if keys[K_u] and player1.bar_filled:
            player1.upgrade(1000, 50)
            player1.bar_filled = False
            player1.damage_dealt = 0
            player1.damage_ratio_divider += 50_000
        
        if keys[K_UP] and player2.bar_filled:
            player2.upgrade(1000, 50)
            player2.bar_filled = False
            player2.damage_dealt = 0
            player2.damage_ratio_divider += 50_000

        
        if keys[K_RETURN] and blaster_collected_p2 == 1:
            if keys[K_LEFT]:
                blaster.shoot(window, player1, -690)
                static_bullet_direction = 0
            if keys[K_RIGHT]:
                blaster.shoot(window, player1, 60)
                static_bullet_direction = 38
            else:
                blaster.bullet.image = transform.scale(image.load(static_bullet), (30, 20))
                window.blit(blaster.bullet.image, (blaster.rect.x + static_bullet_direction, blaster.rect.y + 20))
            blaster.bullet.update()
        else:
            blaster.bullet.active = False

        if blaster_collected_p1 == 1:
            blaster.rect.y = player1.rect.y
        
        if blaster_collected_p2 == 1:
            blaster.rect.y = player2.rect.y



    if player1.health <= 0:
        p2_win = big_font.render("Player2 WON!", True, (255, 255, 0))
        window.blit(p2_win, (300, 350))
        game_over = True

    if player2.health <= 0:
        p1_win = big_font.render("Player1 WON!", True, (0, 255, 0))
        window.blit(p1_win, (300, 350))
        game_over = True
            

    player1.update_jump(player2)
    player2.update_jump(player1)
            

    clock.tick(60)
    display.update()