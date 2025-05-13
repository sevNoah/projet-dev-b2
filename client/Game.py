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
        self.sprite_coup_ken = pygame.image.load("../src/sprites/ken/coup.png").convert_alpha()
        self.sprite_coupDePied_ken = pygame.image.load("../src/sprites/ken/sprite_coup_de_pied_ken.png").convert_alpha()

        self.running = True
        self.fireballs = []  # 🔥 boules de feu de Ryu
        self.fireballs_ken = []  # 🔥 boules de feu de Ken

        # Création des sprite sheets
        self.sprite_sheet = SpriteSheet(self.sprite_person1_img)
        self.punch_sprite_sheet = SpriteSheet(self.sprite_coupDePoint_img)
        self.coup_de_pied_sprite_sheet = SpriteSheet(self.sprite_coup_de_pied_img)
        self.cameamea_sprite_sheet = SpriteSheet(self.sprite_cameamea_img)
        self.boule_de_feu_sprite_sheet = SpriteSheet(self.sprite_boule_de_feu_img)

        self.sprite_sheet_ken = SpriteSheet(self.sprite_person2)
        self.sprite_sheet_coup = SpriteSheet(self.sprite_coup_ken)
        self.sprite_sheet_coupDePied = SpriteSheet(self.sprite_coupDePied_ken)

        # Animations
        self.idle_animation = Animation(self.sprite_sheet, 4, 0.15, 50, loop=True)  # Ryu idle
        self.punch_animation = Animation(self.punch_sprite_sheet, 2, 0.15, 65, loop=False)
        self.coup_de_pied_animation = Animation(self.coup_de_pied_sprite_sheet, 3, 0.15, 65, loop=False)
        self.cameamea_animation = Animation(self.cameamea_sprite_sheet, 2, 0.15, 70, loop=False)

        self.idle_animation_ken = Animation(self.sprite_sheet_ken, 4, 0.15, 60, loop=True)
        self.coup_ken_animation = Animation(self.sprite_sheet_coup, 3, 0.15, 83, loop = False)
        self.coupDePied_ken_animation = Animation(self.sprite_sheet_coupDePied, 3, 0.15, 83, loop= False)

        # Joueurs
        self.player1 = {
            "x": 50,
            "y": 350,
            "current_animation": self.idle_animation,
            "is_punching": False,
            "is_cameamea": False,
            "is_coupDePied": False
        }

        self.player2 = {
            "x": 900,
            "y": 300,
            "current_animation": self.idle_animation_ken,
            "is_punching": False,
            "is_cameamea": False,
            "is_coupDePied": False
        }

        self.speed = 300

        # Touches configurées
        self.kick_button = 1
        self.punch_button = 2
        self.hadouken_button = 3

        # Initialiser les manettes
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def handle_joystick_input(self, delta_time):
        for idx, joystick in enumerate(self.joysticks):
            if idx == 0:
            # 🎮 Manette 0 -> contrôle Ryu
                player = self.player1
            else:
            # 🎮 Manette 1 -> contrôle Ken
                player = self.player2

        # Déplacement
            axis_x = joystick.get_axis(0)
            deadzone = 0.2
            if abs(axis_x) > deadzone:
                player["x"] += axis_x * self.speed * delta_time
                player["x"] = max(0, min(player["x"], 1280 - 150))

        # Attaques (seulement pour Ryu pour l'instant)
            if idx == 0:
                if joystick.get_button(self.kick_button) and not player["is_coupDePied"] and not player["is_punching"] and not player["is_cameamea"]:
                    player["current_animation"] = self.coup_de_pied_animation
                    player["current_animation"].reset()
                    player["is_coupDePied"] = True

                if joystick.get_button(self.punch_button) and not player["is_punching"] and not player["is_coupDePied"] and not player["is_cameamea"]:
                    player["current_animation"] = self.punch_animation
                    player["current_animation"].reset()
                    player["is_punching"] = True

                if joystick.get_button(self.hadouken_button) and not player["is_cameamea"] and not player["is_punching"] and not player["is_coupDePied"]:
                    player["current_animation"] = self.cameamea_animation
                    player["current_animation"].reset()
                    player["is_cameamea"] = True

                if player["is_cameamea"] and player["current_animation"].current_frame >= player["current_animation"].animation_steps - 1:
                    self.fireballs.append({
                        "x": player["x"] + 100,
                        "y": player["y"] + 20,
                        "animation": Animation(self.boule_de_feu_sprite_sheet, 11, 0.1, 45)
                    })
                    player["is_cameamea"] = False
                    player["current_animation"] = self.idle_animation

            if idx == 1:
                if joystick.get_button(self.kick_button) and not player["is_coupDePied"] and not player["is_punching"]:
                    player["current_animation"] = self.coupDePied_ken_animation
                    player["current_animation"].reset()
                    player["is_coupDePied"] = True
                if joystick.get_button(self.punch_button) and not player["is_punching"] and not player["is_coupDePied"]:
                    player["current_animation"] = self.coup_ken_animation
                    player["current_animation"].reset()
                    player["is_punching"] = True

    def update_player(self, player, delta_time):
        frame = player["current_animation"].animate(delta_time)
        if frame:
            self.screen.blit(frame, (player["x"], player["y"]))

        if player["current_animation"].finished and not player["current_animation"].loop:
            if player == self.player1:
                player["current_animation"] = self.idle_animation
            else:
                player["current_animation"] = self.idle_animation_ken
            player["current_animation"].reset()
            player["is_punching"] = False
            player["is_coupDePied"] = False
            player["is_cameamea"] = False

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_joystick_input(delta_time)

            self.screen.blit(self.bg2, (0, 0))

            # Boules de feu
            for fireball in self.fireballs + self.fireballs_ken:
                fireball["x"] += 8
                frame = fireball["animation"].animate(delta_time)
                if frame:
                    self.screen.blit(frame, (fireball["x"], fireball["y"]))
            self.fireballs = [f for f in self.fireballs if f["x"] < 1480]
            self.fireballs_ken = [f for f in self.fireballs_ken if f["x"] < 1480]

            # Joueurs
            self.update_player(self.player1, delta_time)
            self.update_player(self.player2, delta_time)

            pygame.display.flip()

        pygame.quit()
        print("👋 Déconnexion du serveur.")
