from pygame import *
from config_for_muli_shooter import energy_bullet_right

class GameSprite(sprite.Sprite):
    def __init__(self, image_file: str, x: int, y: int, width: int, height: int, speed: int):
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(image_file), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed



class Player(GameSprite):
    def __init__(self, image_file: str, x: int, y: int, width: int, height: int, speed: int, health: int, armor: int, damage: int):
        super().__init__(image_file, x, y, width, height, speed)

        self.max_health = health
        self.health = health
        self.armor = armor
        self.damage = damage
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.is_jumping = False
        self.init_y = y
        self.damage_dealt = 0
        self.bar_filled = False
        self.damage_ratio_divider = 10_000
        self.base_bar_width = 100

    def reset(self, window: Surface):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    def start_jump(self):
        self.velocity_y = self.jump_power
        self.is_jumping = True
    
    def update_jump(self, other_player=None):
        if self.is_jumping:
            self.velocity_y += self.gravity
            old_y = self.rect.y
            self.rect.y += self.velocity_y

            if other_player and self.rect.colliderect(other_player.rect):
                self.rect.y = old_y
                self.velocity_y = 0

            if self.rect.y >= self.init_y:
                self.rect.y = self.init_y
                self.is_jumping = False
                self.velocity_y = 0

    def draw_health_bar(self, bar_width: int, bar_height: int, window: Surface, bar_color: tuple):
        health_ratio = self.health / self.max_health
        current_width = bar_width * health_ratio

        draw.rect(window, (255, 0, 0), (self.rect.x, self.rect.y, bar_width, bar_height))
        draw.rect(window, bar_color, (self.rect.x, self.rect.y, current_width, bar_height))
    
    def draw_xp_bar(self, bar_width: int, bar_height: int, window: Surface, bar_color: tuple = (0, 0, 0)):
        max_bar_width = bar_width
        dmg_ratio = self.damage_dealt / self.damage_ratio_divider
        current_width = bar_width * dmg_ratio if bar_width * dmg_ratio <= max_bar_width else max_bar_width

        if current_width == max_bar_width:
            self.bar_filled = True


        draw.rect(window, (200, 200, 200), (self.rect.x + 70, self.rect.y + 20, bar_width, bar_height))
        draw.rect(window, bar_color, (self.rect.x + 70, self.rect.y + 20, current_width, bar_height))


    def attack(self, other):
        if not isinstance(other, Player):
            raise TypeError("'other' повинен бути гравцем (Player)")
        else:
            other.health -= self.damage
            self.damage_dealt += self.damage
    
    def upgrade(self, max_health_bonus, damage_bonus):
        self.max_health += max_health_bonus
        self.health = self.max_health
        self.damage += damage_bonus
        




class EnergyBlaster(GameSprite):
    def __init__(self, image: str, x: int, y: int, width: int, height: int, speed: int, damage: int, owner: Player = None):
        super().__init__(image, x, y, width, height, speed)
        self.owner = owner
        self.bullet = Bullet(energy_bullet_right, self.rect.x, self.rect.y, 700, 65, 0)
        self.bullet_damage = damage
    
    def reset(self, window: Surface, space_from_owner: int = 0):
        window.blit(self.image, (self.rect.x + space_from_owner, self.rect.y))

    def shoot(self, window: Surface, other: Player, space_from_blaster: int):
        self.bullet.active = True
        if self.bullet.active:
            self.bullet.reset(window, self.rect.x + space_from_blaster, self.rect.y)
            if resolve_collision(self.bullet.rect, other.rect) and other != self.owner:
                if hasattr(self.owner, "damage_dealt"):
                    self.owner.damage_dealt += self.bullet_damage
                other.health -= self.bullet_damage

    def upgrade(self, bullet_damage_bonus, new_picture = None):
        self.image = transform.scale(image.load(new_picture), (self.width, self.height))
        self.bullet_damage += bullet_damage_bonus


    

        


class Bullet(GameSprite):
    def __init__(self, image_file, x, y, width, height, speed):
        super().__init__(image_file, x, y, width, height, speed)
        self.active = False
    def reset(self, window: Surface, x: int, y: int):
        if self.active:
            self.rect.x = x
            self.rect.y = y
            window.blit(self.image, (self.rect.x, self.rect.y))


def resolve_collision(self: Player | Rect, other: Player | Rect) -> bool:
    if isinstance(self, Player) and isinstance(other, Player):
        return self.rect.colliderect(other.rect)
    elif isinstance(self, Rect) and isinstance(other, Rect):
        return self.colliderect(other)
    elif isinstance(self, Player) and isinstance(other, Rect):
        return self.rect.colliderect(other)
    elif isinstance(self, Rect) and isinstance(other, Player):
        return self.colliderect(other.rect)
    
    return False