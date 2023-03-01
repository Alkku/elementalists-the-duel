#League of Ezreal platformer

import pygame as pg
from pygame import mixer
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        self.SplashBackground = Splash("pictures/background_splash.jpg", [0, 0])
        self.MainMenuFrame = Splash("pictures/main_menu_frame.png", [600, 440])
        self.GameOver = Splash("pictures/game over.png", [640, 150])
        self.Player1Jump = Splash("pictures/ez_jumping.png", [930, 480])
        self.Player2Jump = Splash("pictures/ez_jumping_r.png", [930, 480])

        self.ReadyToUlt1 = Splash("pictures/ultimate_ready.png", [230, 35])
        self.ReadyToUlt2 = Splash("pictures/ultimate_ready.png", [1630, 35])

        self.life_hearts1 = Splash("pictures/lives.png", [330, 32])
        self.life_hearts2 = Splash("pictures/lives.png", [370, 32])
        self.life_hearts3 = Splash("pictures/lives.png", [410, 32])

        self.life_hearts4 = Splash("pictures/lives.png", [1730, 32])
        self.life_hearts5 = Splash("pictures/lives.png", [1770, 32])
        self.life_hearts6 = Splash("pictures/lives.png", [1810, 32])


        pg.mouse.set_visible(False)
        pg.display.set_caption("League of Ezreal")
        self.clock = pg.time.Clock()
        self.previous_time1 = pg.time.get_ticks()
        self.previous_time2 = pg.time.get_ticks()
        self.running = True
        self.start_screen = True
        self.font_name = pg.font.match_font(FONT_NAME)
        pg.mixer.music.load('sounds/Game Music.wav')
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.13)

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)

        self.draw_text("PLAYER 1", 20, WHITE, WIDTH * 0.092, HEIGHT * 0.04)
        self.draw_text("PLAYER 2", 20, WHITE, WIDTH * 0.82, HEIGHT * 0.04)
        if self.player1.ready_to_ult == True:
            self.screen.blit(self.ReadyToUlt1.image, self.ReadyToUlt1.rect)
        elif self.player2.ready_to_ult == True:
            self.screen.blit(self.ReadyToUlt2.image, self.ReadyToUlt2.rect)

        #player1 lives graphics
        if self.player1.lives == 3:
            self.screen.blit(self.life_hearts1.image, self.life_hearts1.rect)
            self.screen.blit(self.life_hearts2.image, self.life_hearts2.rect)
            self.screen.blit(self.life_hearts3.image, self.life_hearts3.rect)
        if self.player1.lives == 2:
            self.screen.blit(self.life_hearts1.image, self.life_hearts1.rect)
            self.screen.blit(self.life_hearts2.image, self.life_hearts2.rect)
        if self.player1.lives == 1:
            self.screen.blit(self.life_hearts1.image, self.life_hearts1.rect)

        #2 lives graphics
        if self.player2.lives == 3:
            self.screen.blit(self.life_hearts4.image, self.life_hearts4.rect)
            self.screen.blit(self.life_hearts5.image, self.life_hearts5.rect)
            self.screen.blit(self.life_hearts6.image, self.life_hearts6.rect)
        if self.player2.lives == 2:
            self.screen.blit(self.life_hearts4.image, self.life_hearts4.rect)
            self.screen.blit(self.life_hearts5.image, self.life_hearts5.rect)
        if self.player2.lives == 1:
            self.screen.blit(self.life_hearts4.image, self.life_hearts4.rect)

        pg.draw.rect(self.screen, RED, (100, 70, 340, 35))
        pg.draw.rect(self.screen, RED, (1500, 70, 340, 35))
        pg.draw.rect(self.screen, GREEN, (100, 70, 34 * self.player1.health, 35)) # Health of player 1
        pg.draw.rect(self.screen, GREEN, (1500, 70, 34 * self.player2.health, 35)) # Health of player 2

        self.all_sprites.draw(self.screen)
        if self.paused:
            pg.mixer.music.pause()
            self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
            self.dim_screen.fill((0, 0, 0, 140))
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("PAUSED", 90, WHITE, WIDTH / 2, HEIGHT * 0.4)
            self.draw_text("Press Q to quit to main menu", 30, WHITE, WIDTH / 2, HEIGHT * 0.5)
        pg.display.flip()


    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.both_healthbars = pg.sprite.Group()
        self.p1_bullets = pg.sprite.Group()
        self.p2_bullets = pg.sprite.Group()
        self.p1_ultimate = pg.sprite.Group()
        self.p2_ultimate = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.blood_spray = pg.sprite.Group()

        p1 = Platform(-20, HEIGHT * 0.92, "still", False, "platform2.png")
        p2 = Platform(WIDTH * 0.15, HEIGHT * 0.25, "moving", False, "platform_moving.png") #Vänster moving
        p3 = Platform(WIDTH * 0.72, HEIGHT * 0.55, "moving", True, "platform_moving.png") #Höger moving
        p4 = Platform(-50, HEIGHT * 0.45, "still", False, "main_platforms.png") #Vänster spawn bottom
        p5 = Platform(WIDTH - WIDTH * 0.1, HEIGHT * 0.45, "still", False, "main_platforms.png") #Höger spawn bottom
        p6 = Platform(WIDTH * 0.425, HEIGHT * 0.6, "still", False, "main_platforms.png") #Mitten högre
        p7 = Platform(WIDTH * 0.335, HEIGHT * 0.21, "still", False, "platform_small.png") #Övre liten höger
        p8 = Platform(WIDTH * 0.595, HEIGHT * 0.21, "still", False, "platform_small.png") #Övre liten vänster
        p9 = Platform(WIDTH * 0.29, HEIGHT * 0.75, "still", False, "platform_small.png") #Höger nere liten
        p10 = Platform(WIDTH / 2 - (WIDTH * 0.0375), HEIGHT * 0.16, "still", False, "platform_small.png") #Hösta ult plat
        p11 = Platform(WIDTH * 0.63, HEIGHT * 0.75, "still", False, "platform_small.png") #Vänster nere liten
        p12 = Platform(-35, HEIGHT * 0.2, "still", False, "platform_small.png")
        p13 = Platform(WIDTH - 75, HEIGHT * 0.2, "still", False, "platform_small.png")

        self.all_sprites.add(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13)
        self.platforms.add(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13)

        self.healthbar_frame_p1 = Splash('pictures/health_bar.png', [50, 50])
        self.healthbar_frame_p2 = Splash('pictures/health_bar.png', [1450, 50])
        self.all_sprites.add(self.healthbar_frame_p1, self.healthbar_frame_p2)
        self.both_healthbars.add(self.healthbar_frame_p1, self.healthbar_frame_p2)

        self.player1 = Player(self, pg.K_a, pg.K_d, self.all_sprites, WIDTH * 0.21, HEIGHT * 0.2,
                              True, self.p1_bullets, self.p2_bullets, self.p1_ultimate, self.p2_ultimate,
                              "shot_right.png", "ultimate_right.png",
                              [pg.image.load("pictures/ez_standing1.png").convert_alpha(),
                         pg.image.load("pictures/ez_standing2.png").convert_alpha()],
                              [pg.image.load("pictures/ez_walking1.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking2.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking3.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking4.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking5.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking6.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking7.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking8.png").convert_alpha(),
                        pg.image.load("pictures/ez_walking9.png").convert_alpha()],
                              "pictures/ez_shooting.png", "pictures/ez_jumping.png")

        self.player2 = Player(self, pg.K_LEFT, pg.K_RIGHT, self.all_sprites, WIDTH * 0.78, HEIGHT * 0.2,
                              False, self.p2_bullets, self.p1_bullets, self.p2_ultimate, self.p1_ultimate,
                              "shot_left.png", "ultimate_left.png",
                              [pg.image.load("pictures/ez_standing1_r.png").convert_alpha(),
                        pg.image.load("pictures/ez_standing2_r.png").convert_alpha()],
                              [pg.image.load("pictures/ez_walking1_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking2_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking3_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking4_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking5_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking6_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking7_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking8_r.png").convert_alpha(),
                       pg.image.load("pictures/ez_walking9_r.png").convert_alpha()],
                              "pictures/ez_shooting_r.png", "pictures/ez_jumping_r.png")

        self.all_sprites.add(self.player1, self.player2)
        self.players = pg.sprite.Group(self.player1, self.player2)
        self.powerup = Powerup(self)
        self.paused = False
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.screen.fill([255, 255, 255])
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
                pg.mixer.music.unpause()
            self.draw()


    def update(self):
        self.all_sprites.update()
        #Player 1 position
        if self.player1.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player1.pos.x < lowest.rect.right and self.player1.pos.x > lowest.rect.left:
                     if self.player1.pos.y < lowest.rect.centery:
                        self.player1.pos.y = lowest.rect.top
                        self.player1.vel.y = 5
                        self.player1.jumping = False

        if self.player2.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player2, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player2.pos.x < lowest.rect.right and self.player2.pos.x > lowest.rect.left:
                     if self.player2.pos.y < lowest.rect.centery:
                        self.player2.pos.y = lowest.rect.top
                        self.player2.vel.y = 5
                        self.player2.jumping = False


        if self.player1.health <= 0 and self.player1.lives <= 0:
            self.winner = "PLAYER 2"
            #Bild av ezreal me pokal
            self.playing = False

        if self.player2.health <= 0 and self.player2.lives <= 0:
            self.winner = "PLAYER 1"
            self.playing = False




    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused


#Player 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w and pg.sprite.spritecollide(self.player1, self.platforms, False) and self.player1.jump_count == 1:
                    self.player1.jump()

                elif event.key == pg.K_w and pg.sprite.spritecollide(self.player1, self.platforms, False) and self.player1.jump_count == 2:
                    self.player1.jump()
                    self.player1.jump_count = 2
                elif event.key == pg.K_w and self.player1.jump_count == 2:
                    self.player1.double_jump()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    current_time = pg.time.get_ticks()
                    if current_time - self.previous_time1 > 500:
                        self.previous_time1 = current_time
                        self.player1.shoot()

                if event.key == pg.K_h and self.player1.ready_to_ult == True:
                    self.player1.shoot_ultimate()
                    self.player1.ready_to_ult = False



# Player 2
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and pg.sprite.spritecollide(self.player2, self.platforms, False) and self.player2.jump_count == 1:
                    self.player2.jump()
                elif event.key == pg.K_UP and pg.sprite.spritecollide(self.player2, self.platforms, False) and self.player2.jump_count == 2:
                    self.player2.jump()
                    self.player2.jump_count = 2
                elif event.key == pg.K_UP and self.player2.jump_count == 2:
                    self.player2.double_jump()


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP1:
                    current_time = pg.time.get_ticks()
                    if current_time - self.previous_time2 > 500:
                        self.previous_time2 = current_time
                        self.player2.shoot()

                if event.key == pg.K_KP2 and self.player2.ready_to_ult == True:
                    self.player2.shoot_ultimate()
                    self.player2.ready_to_ult = False



    def show_controls_screen(self):
        pass


    def show_end_screen(self):
        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
        self.screen.blit(self.GameOver.image, self.GameOver.rect)
        if self.winner == "PLAYER 1":
            self.screen.blit(self.Player1Jump.image, self.Player1Jump.rect)
        else:
            self.screen.blit(self.Player2Jump.image, self.Player2Jump.rect)
        self.draw_text(str(self.winner) + " WINS!", 60, LIGHT_RED, WIDTH / 2, HEIGHT * 0.275)

        self.draw_text("« PLAY AGAIN »", 50, LIGHT_RED, WIDTH / 2, HEIGHT * 0.6)
        self.draw_text("QUIT TO MAIN MENU", 50, WHITE, WIDTH / 2, HEIGHT * 0.7)
        pg.display.flip()
        end_menu = 1
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and end_menu == 1:
                        waiting = False
                        pg.display.flip()
                    elif event.key == pg.K_RETURN and end_menu == 2:
                        waiting = False
                        self.running = False
                    # New Game -> Controls

                    elif event.key == pg.K_DOWN and end_menu == 1 or event.key == pg.K_UP and end_menu == 1:
                        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
                        self.screen.blit(self.GameOver.image, self.GameOver.rect)
                        if self.winner == "PLAYER 1":
                            self.screen.blit(self.Player1Jump.image, self.Player1Jump.rect)
                        else:
                            self.screen.blit(self.Player2Jump.image, self.Player2Jump.rect)
                        self.draw_text(str(self.winner) + " WINS!", 60, LIGHT_RED, WIDTH / 2, HEIGHT * 0.275)
                        self.draw_text("PLAY AGAIN", 50, WHITE, WIDTH / 2, HEIGHT * 0.6)
                        self.draw_text("« QUIT TO MAIN MENU »", 50, LIGHT_RED, WIDTH / 2, HEIGHT * 0.7)
                        end_menu = 2
                        waiting = True
                        pg.display.flip()
                    elif event.key == pg.K_UP and end_menu == 2 or event.key == pg.K_DOWN and end_menu == 2:
                        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
                        self.screen.blit(self.GameOver.image, self.GameOver.rect)
                        if self.winner == "PLAYER 1":
                            self.screen.blit(self.Player1Jump.image, self.Player1Jump.rect)
                        else:
                            self.screen.blit(self.Player2Jump.image, self.Player2Jump.rect)
                        self.draw_text(str(self.winner) + " WINS!", 60, LIGHT_RED, WIDTH / 2, HEIGHT * 0.275)
                        self.draw_text("« PLAY AGAIN »", 50, LIGHT_RED, WIDTH / 2, HEIGHT * 0.6)
                        self.draw_text("QUIT TO MAIN MENU", 50, WHITE, WIDTH / 2, HEIGHT * 0.7)
                        end_menu = 1
                        waiting = True
                        pg.display.flip()


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def show_start_screen(self):
        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
        self.screen.blit(self.MainMenuFrame.image, self.MainMenuFrame.rect)
        self.draw_text("ELEMENTALISTS", 90, LIGHT_RED, WIDTH / 2, HEIGHT * 0.15)
        self.draw_text("- THE DUEL -", 70, BLACK, WIDTH / 2, HEIGHT * 0.25)
        self.draw_text("« NEW GAME »", 50, GREEN, WIDTH / 2, HEIGHT * 0.53)
        self.draw_text("CONTROLS", 50, BLACK, WIDTH / 2, HEIGHT * 0.6)
        self.draw_text("QUIT", 50, BLACK, WIDTH / 2, HEIGHT * 0.68)
        self.draw_text("A game made by Alkku", 16, WHITE, WIDTH / 2, HEIGHT * 0.97)
        pg.display.flip()

        main_menu = 1
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and main_menu == 1:
                        waiting = False
                        pg.display.flip()
                   # elif event.key == pg.K_RETURN and main_menu == 2:

                    elif event.key == pg.K_RETURN and main_menu == 3:
                        waiting = False
                        self.running = False
                        self.start_screen = False

                    elif event.key == pg.K_DOWN and main_menu == 1 or event.key == pg.K_UP and main_menu == 3:
                        self.screen.fill(BLUE)
                        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
                        self.screen.blit(self.MainMenuFrame.image, self.MainMenuFrame.rect)
                        self.draw_text("ELEMENTALISTS", 90, LIGHT_RED, WIDTH / 2, HEIGHT * 0.15)
                        self.draw_text("- THE DUEL -", 70, BLACK, WIDTH / 2, HEIGHT * 0.25)
                        self.draw_text("NEW GAME", 50, BLACK, WIDTH / 2, HEIGHT * 0.53)
                        self.draw_text("« CONTROLS »", 50, GREEN, WIDTH / 2, HEIGHT * 0.6)
                        self.draw_text("QUIT", 50, BLACK, WIDTH / 2, HEIGHT * 0.68)
                        self.draw_text("A game made by Alkku", 16, WHITE, WIDTH / 2, HEIGHT * 0.97)
                        main_menu = 2
                        waiting = True
                        pg.display.flip()
                    elif event.key == pg.K_DOWN and main_menu == 2 or event.key == pg.K_UP and main_menu == 1:
                        self.screen.fill(BLUE)
                        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
                        self.screen.blit(self.MainMenuFrame.image, self.MainMenuFrame.rect)
                        self.draw_text("ELEMENTALISTS", 90, LIGHT_RED, WIDTH / 2, HEIGHT * 0.15)
                        self.draw_text("- THE DUEL -", 70, BLACK, WIDTH / 2, HEIGHT * 0.25)
                        self.draw_text("NEW GAME", 50, BLACK, WIDTH / 2, HEIGHT * 0.53)
                        self.draw_text("CONTROLS", 50, BLACK, WIDTH / 2, HEIGHT * 0.6)
                        self.draw_text("« QUIT »", 50, GREEN, WIDTH / 2, HEIGHT * 0.68)
                        self.draw_text("A game made by Alkku", 16, WHITE, WIDTH / 2, HEIGHT * 0.97)
                        main_menu = 3
                        waiting = True
                        pg.display.flip()
                    elif event.key == pg.K_UP and main_menu == 2 or event.key == pg.K_DOWN and main_menu == 3:
                        self.screen.fill(BLUE)
                        self.screen.blit(self.SplashBackground.image, self.SplashBackground.rect)
                        self.screen.blit(self.MainMenuFrame.image, self.MainMenuFrame.rect)
                        self.draw_text("ELEMENTALISTS", 90, LIGHT_RED, WIDTH / 2, HEIGHT * 0.15)
                        self.draw_text("- THE DUEL -", 70, BLACK, WIDTH / 2, HEIGHT * 0.25)
                        self.draw_text("« NEW GAME »", 50, GREEN, WIDTH / 2, HEIGHT * 0.53)
                        self.draw_text("CONTROLS", 50, BLACK, WIDTH / 2, HEIGHT * 0.6)
                        self.draw_text("QUIT", 50, BLACK, WIDTH / 2, HEIGHT * 0.68)
                        self.draw_text("A game made by Alkku", 16, WHITE, WIDTH / 2, HEIGHT * 0.97)
                        main_menu = 1
                        waiting = True
                        pg.display.flip()


g = Game()
g.show_start_screen()

while g.start_screen:
    while g.running:
        g.new()
        g.run()
        g.show_end_screen()
    g.show_start_screen()
    g.running = True
pg.quit()


# Additional updates
# 1. Pause quit to main menu
# 2. Assign keys in settings


