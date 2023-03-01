from settings import *
#from main import *
import pygame as pg
from pygame import mixer
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, left, right, all_sprites, x, y,
                 player_facing_right, bullets, enemy_bullets, ultimate,
                 enemy_ultimate, shot_direction, image_direction,
                 player_standing_list, player_walking_list, player_shooting_list,
                 player_jumping_list):

        pg.sprite.Sprite.__init__(self)
        self.player_standing_list = player_standing_list
        self.player_walking_list = player_walking_list
        self.player_shooting_list = player_shooting_list
        self.player_jumping_list = player_jumping_list
        self.game = game
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.jump_count = 1
        self.rect.midleft = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.x = x
        self.y = y
        self.key_left = left
        self.key_right = right
        self.all_sprites = all_sprites
        self.player_facing_right = player_facing_right
        self.bullets = bullets
        self.enemy_bullets = enemy_bullets
        self.health = 10
        self.lives = 3
        self.ready_to_ult = False
        self.ultimate = ultimate
        self.enemy_ultimate = enemy_ultimate
        self.shot_direction = shot_direction
        self.image_direction = image_direction

        self.walking = False
        self.jumping = False
        self.standing = True
        self.current_frame = 0
        self.last_update = 0

    def load_images(self):
        self.standing_frames_r = self.player_standing_list
        self.standing_frames_l = []
        for standing_frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(standing_frame, True, False))

        self.walk_frames_r = self.player_walking_list
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame_r = self.player_jumping_list
        self.jump_frame_l = pg.transform.flip(pg.image.load(self.player_jumping_list).convert_alpha(), True, False)

        self.shoot_frame_r = self.player_shooting_list
        self.shoot_frame_l = pg.transform.flip(pg.image.load(self.player_shooting_list).convert_alpha(), True, False)

    def jump(self):
            self.rect.x += 1
            pg.mixer.Sound('sounds/jump.wav').play()
            self.jumping = True
            self.vel.y = -20
            if self.shot_direction == "shot_left.png" and self.vel.x != 0 and self.jumping:
                self.image = pg.transform.flip(pg.image.load(self.player_jumping_list).convert_alpha(), True, False)
            elif self.shot_direction == "shot_left.png" and self.vel.x == 0 and self.jumping:
                self.image = pg.transform.flip(pg.image.load(self.player_jumping_list).convert_alpha(), True, False)
            else:
                self.image = pg.image.load(self.player_jumping_list).convert_alpha()
            self.rect.x -= 1
            self.jump_count += 1

    def double_jump(self):
            self.rect.x += 1
            pg.mixer.Sound('sounds/double_jump.wav').play()
            self.jumping = True
            self.vel.y = -15
            if self.shot_direction == "shot_left.png" and self.vel.x != 0 and self.jumping:
                self.image = pg.transform.flip(pg.image.load(self.player_jumping_list).convert_alpha(), True, False)
            elif self.shot_direction == "shot_left.png" and self.vel.x == 0 and self.jumping:
                self.image = pg.transform.flip(pg.image.load(self.player_jumping_list).convert_alpha(), True, False)
            else:
                self.image = pg.image.load(self.player_jumping_list).convert_alpha()
            self.rect.x -= 1
            self.jump_count = 1


    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

        self.fire_direction = "still"

        keys = pg.key.get_pressed()

        if keys[self.key_left]:
            self.acc.x = -PLAYER_ACC
            self.fire_direction = "left"
            self.image_direction = "ultimate_left.png"
            self.shot_direction = "shot_left.png"
            self.player_facing_right = False

        if keys[self.key_right]:
            self.acc.x = PLAYER_ACC
            self.fire_direction = "right"
            self.image_direction = "ultimate_right.png"
            self.shot_direction = "shot_right.png"
            self.player_facing_right = True

        #Ger friktion o de är equations of motion resten
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.45:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

        collided_ultimate = pg.sprite.spritecollide(self, self.enemy_ultimate, True)
        for ultimate in collided_ultimate:
            self.health -= 5
            for i in range(1, 30):
                self.blood = Blood(self.pos, self.bullets)
                self.all_sprites.add(self.blood)
                self.game.blood_spray.add(self.blood)

        collided_bullets = pg.sprite.spritecollide(self, self.enemy_bullets, True)
        for bullet in collided_bullets:
            self.health -= 1
            for i in range(1, 30):
                self.blood = Blood(self.pos, self.bullets)
                self.all_sprites.add(self.blood)
                self.game.blood_spray.add(self.blood)
        for hit in collided_bullets:
            self.pow_picked_up = True
            if random.random() > 0.93 and self.pow_picked_up == True:
                self.pow_picked_up = False
                self.all_sprites.add(self.game.powerup)
                self.game.powerups.add(self.game.powerup)
        if self.game.player1.ready_to_ult == False:
            if pg.sprite.spritecollide(self.game.player1, self.game.powerups, True):
                pg.mixer.Sound('sounds/obtain_ultimate.wav').play()
                self.game.player1.ready_to_ult = True

        if self.game.player2.ready_to_ult == False:
            if pg.sprite.spritecollide(self.game.player2, self.game.powerups, True):
                pg.mixer.Sound('sounds/obtain_ultimate.wav').play()
                self.game.player2.ready_to_ult = True



        if self.health <= 0 and self.lives > 0:
            self.lives -= 1
            self.health = 10

            pg.mixer.Sound('sounds/respawn.wav').play()
            self.pos = vec(self.x, self.y)
            self.rect.midleft = (WIDTH / 2, HEIGHT / 2)

        elif self.lives == 0:
            self.health = 0
            pg.display.flip()



    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking and not self.jumping:
            if now - self.last_update > 10:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking and self.standing and self.shot_direction == "shot_right.png":
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_r)
                self.image = self.standing_frames_r[self.current_frame]

        if not self.jumping and not self.walking and self.standing and self.shot_direction == "shot_left.png":
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_l)
                self.image = self.standing_frames_l[self.current_frame]


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.center, self.fire_direction,
                        self.player_facing_right, self.pos, self.shot_direction)
        pg.mixer.Sound('sounds/bullet.wav').play()
        if self.shot_direction == "shot_left.png":
            self.image = pg.transform.flip(pg.image.load(self.player_shooting_list).convert_alpha(), True, False)
        else:
            self.image = pg.image.load(self.player_shooting_list).convert_alpha()
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def shoot_ultimate(self):
        ultimate = Ultimate(self.rect.centerx, self.rect.center, self.fire_direction,
                            self.player_facing_right, self.image_direction)
        pg.mixer.Sound('sounds/ultimate.wav').play()
        if self.image_direction == "ultimate_left.png":
            self.image = pg.transform.flip(pg.image.load("pictures/ez_shooting.png").convert_alpha(), True, False)
        else:
            self.image = pg.image.load("pictures/ez_shooting.png").convert_alpha()
        self.pow_picked_up = True
        self.ready_to_ult = False
        self.all_sprites.add(ultimate)
        self.ultimate.add(ultimate)






class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, movement, direction_up, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("pictures/" + str(image)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.speedy = 2
        self.rect.y = y
        self.movement = movement
        self.direction_up = direction_up

    def update(self):
        if self.movement == "moving":
            if self.rect.y <= HEIGHT * 0.55 and self.direction_up == False:
                 self.rect.y += self.speedy

            elif self.rect.y >= HEIGHT * 0.25 and self.direction_up == True:
                 self.rect.y -= self.speedy

            if self.rect.y == HEIGHT * 0.55:
                self.direction_up = True
            elif self.rect.y == HEIGHT * 0.25:
                self.direction_up = False

        elif self.movement == "still":
            self.rect.x = self.rect.x




class Splash(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location




class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, fire_direction, player_facing_right, player_pos, shot_direction):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("pictures/" + str(shot_direction)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = y
        self.rect.centerx = x
        self.speedx = BULLET_SPEED
        self.fire_direction = fire_direction
        self.player_facing_right = player_facing_right
        self.pos = player_pos

    def update(self):
        if self.fire_direction == "left":
            self.rect.x += self.speedx
        elif self.fire_direction == "right":
            self.rect.x -= self.speedx

        elif self.fire_direction == "still" and self.player_facing_right == False:
            self.rect.x += self.speedx
        elif  self.fire_direction == "still" and self.player_facing_right == True:
            self.rect.x -= self.speedx


        if self.rect.x - self.pos.x >= 400:
            self.kill()

        elif self.rect.x - self.pos.x <= -400:
            self.kill()

        elif self.rect.x < 0:
            self.kill()
        elif self.rect.right > WIDTH:
            self.kill()


class Ultimate(pg.sprite.Sprite):
    def __init__(self, x, y, fire_direction, player_facing_right, image_direction):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("pictures/" + str(image_direction)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = y
        self.rect.centerx = x
        self.speedx = ULTIMATE_SPEED
        self.fire_direction = fire_direction
        self.player_facing_right = player_facing_right

    def update(self):
        if self.fire_direction == "left":
            self.rect.x += self.speedx
        elif self.fire_direction == "right":
            self.rect.x -= self.speedx
        elif self.fire_direction == "still" and self.player_facing_right == False:
            self.rect.x += self.speedx
        elif self.fire_direction == "still" and self.player_facing_right == True:
            self.rect.x -= self.speedx

        if self.rect.x < 0:
            self.kill()
        elif self.rect.x > WIDTH:
            self.kill()


class Powerup(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("pictures/powerup.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midleft = (916, 132)

class Blood(pg.sprite.Sprite):
    def __init__(self, hit_player_pos, bullets):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5, 5))
        self.image.fill(TURQUOISE)
        self.rect = self.image.get_rect()
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.hit_player_pos = hit_player_pos
        self.rect.midtop = hit_player_pos
        self.bullets = bullets
        self.speedx = random.randrange(-20, 20)
        self.speedy = random.randrange(5, 20)

    def update(self):
        self.acc = vec(0, 10)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.rect.x -= self.speedx
        self.rect.y -= self.speedy

        if self.rect.x - self.hit_player_pos.x >= random.randrange(100, 200):
            self.kill()
        elif self.rect.x - self.hit_player_pos.x <= random.randrange(-200, -100):
            self.kill()
        if self.rect.y - self.hit_player_pos.y > random.randrange(100, 200):
            self.kill()
        elif self.rect.y - self.hit_player_pos.y < random.randrange(-200, -100):
            self.kill()