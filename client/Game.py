import pygame
from SpriteSheet import SpriteSheet
from Animation import Animation

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Street Fighter Game")
        self.clock = pygame.time.Clock()

        # Chargement du fond
        self.bg2 = pygame.image.load("../src/background/street_fighter_2.png").convert()

        # Chargement des sprites pour Ryu
        self.sprite_person1_img = pygame.image.load("../src/sprites/ryu/sprite_1.png").convert_alpha()
        self.sprite_coupDePoint_img = pygame.image.load("../src/sprites/ryu/spritecombat_coupDePoint.png").convert_alpha()
        self.sprite_coup_de_pied_img = pygame.image.load("../src/sprites/ryu/sprite_coup_de_pied.png").convert_alpha()
        self.sprite_cameamea_img = pygame.image.load("../src/sprites/ryu/sprite_caméaméa.png").convert_alpha()
        self.sprite_boule_de_feu_img = pygame.image.load("../src/sprites/ryu/sprite_boule_de_feu.png").convert_alpha()

        # Chargement du sprite pour Ken
        self.sprite_person2 = pygame.image.load("../src/sprites/ken/sprite_idl.png").convert_alpha()

        self.running = True
        self.fireballs = []

        # Création des sprite sheets
        self.sprite_sheet = SpriteSheet(self.sprite_person1_img)
        self.punch_sprite_sheet = SpriteSheet(self.sprite_coupDePoint_img)
        self.coup_de_pied_sprite_sheet = SpriteSheet(self.sprite_coup_de_pied_img)
        self.cameamea_sprite_sheet = SpriteSheet(self.sprite_cameamea_img)
        self.boule_de_feu_sprite_sheet = SpriteSheet(self.sprite_boule_de_feu_img)

        self.sprite_sheet_ken = SpriteSheet(self.sprite_person2)

        # Animations
        self.idle_animation = Animation(self.sprite_sheet, 4, 0.15, 50, loop=True)  # ✅ idle boucle
        self.punch_animation = Animation(self.punch_sprite_sheet, 2, 0.1, 65, loop=False)  # ❌ coup de poing 1 fois
        self.coup_de_pied_animation = Animation(self.coup_de_pied_sprite_sheet, 3, 0.1, 65, loop=False)  # ❌ 1 fois
        self.cameamea_animation = Animation(self.cameamea_sprite_sheet, 2, 0.15, 70, loop=False)  # ❌ 1 fois


        self.idle_animation_ken = Animation(self.sprite_sheet_ken, 3, 0.15, 50, loop=True) 

        self.current_animation = self.idle_animation
        self.is_punching = False
        self.is_cameamea = False
        self.is_coupDePied = False

        self.player_x = 50
        self.player_y = 350
        self.ken_x= 900
        self.ken_y= 350
        self.speed = 300

        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

    def handle_joystick_input(self, delta_time):
        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            deadzone = 0.2
            if abs(axis_x) > deadzone:
                self.player_x += axis_x * self.speed * delta_time
            self.player_x = max(0, min(self.player_x, 1280 - 150))

            # Attaques
            if self.joystick.get_button(1) and not self.is_coupDePied and not self.is_punching and not self.is_cameamea:
                self.current_animation = self.coup_de_pied_animation
                self.current_animation.reset()
                self.is_coupDePied = True

            if self.joystick.get_button(2) and not self.is_punching and not self.is_coupDePied and not self.is_cameamea:
                self.current_animation = self.punch_animation
                self.current_animation.reset()
                self.is_punching = True

            if self.joystick.get_button(3) and not self.is_cameamea and not self.is_punching and not self.is_coupDePied:
                self.current_animation = self.cameamea_animation
                self.current_animation.reset()
                self.is_cameamea = True

            # Gestion de la fin de caméaméa -> tir d'une boule de feu
            if self.is_cameamea and self.current_animation.current_frame >= self.current_animation.animation_steps - 1:
                self.fireballs.append({
                    "x": self.player_x + 100,
                    "y": self.player_y + 20,
                    "animation": Animation(self.boule_de_feu_sprite_sheet, 11, 0.1, 45)  # Nouvelle animation pour chaque boule
                })
                self.is_cameamea = False
                self.current_animation = self.idle_animation

    def run(self):
     while self.running:
        delta_time = self.clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.handle_joystick_input(delta_time)

        self.screen.blit(self.bg2, (0, 0))

        ken_frame = self.idle_animation_ken.animate(delta_time)
        if ken_frame:
            self.screen.blit(ken_frame, (self.ken_x, self.ken_y))


        # Affichage des boules de feu
        for fireball in self.fireballs:
            fireball["x"] += 8
            fireball_frame = fireball["animation"].animate(delta_time)
            if fireball_frame:
                self.screen.blit(fireball_frame, (fireball["x"], fireball["y"]))

        self.fireballs = [f for f in self.fireballs if f["x"] < 1480]

        player_frame = self.current_animation.animate(delta_time)
        if player_frame:
            self.screen.blit(player_frame, (self.player_x, self.player_y))

        # 🔥 Quand l'animation est terminée (et pas idle), on revient à idle + on reset les flags
        if self.current_animation.finished and not self.current_animation.loop:
            self.current_animation = self.idle_animation
            self.current_animation.reset()
            self.is_punching = False
            self.is_coupDePied = False
            self.is_cameamea = False



        pygame.display.flip()

    pygame.quit()
    print("👋 Déconnexion du serveur.")

        