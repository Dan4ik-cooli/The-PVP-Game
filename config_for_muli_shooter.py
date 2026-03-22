from pygame import *
win_width = 1500
win_height = 900
background = transform.scale(
    image.load("assets/mul_shooter_city_back.jpg"), (win_width, win_height)
)

player1_img_right = "assets/player1_right.png"
player1_img_left = "assets/player1_left.png"
player2_img_1_left = "assets/player2opt1_left.png"
player2_img_1_right = "assets/player2opt1_right.png"

player2_img_2 = "assets/player2opt2.png"
player2_img_3 = "assets/player2opt3.png"
player2_img_4 = "assets/player2opt4.png"
player2_img_5 = "assets/player2opt5.png"
player2_img_6 = "assets/player2opt6.png"
player2_img_7 = "assets/player2opt7.png"
player2_img_8 = "assets/player2opt8.png"
player2_img_9 = "assets/player2opt9.png"
player2_img_10 = "assets/player2opt10.png"
player2_img_11 = "assets/player2opt11.png"
player2_img_12 = "assets/player2opt12.png"

blaster_image_right = "assets/energy_blaster.png"
energy_bullet_right = "assets/en_bullet.png"
blaster_image_left = "assets/energy_blaster_mirror.png"
energy_bullet_left = "assets/en_bullet_mirror.png"
static_bullet = "assets/stat_bullet.png"

blaster_collected_p1 = 0
blaster_collected_p2 = 0
blaster_shot = False
static_bullet_direction = 0
#paused = False
#MES_LEN = 3000
BLASTER_HIDEN_DURATION = 60_000