import pygame
from SpriteSheet import SpriteSheet
from Animation import Animation
from gameOver import GameOverScreen  

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Street Fighter Game")
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 99_000  # 99 secondes en millisecondes
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
        self.fireballs = [] 
        self.fireballs_ken = [] 

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
            "health": 500,
            "last_attack_time": 0,
            "attack_cooldown": 650,
            "cameamea_cooldown": 1500,  
            "current_animation": self.idle_animation,
            "is_punching": False,
            "is_cameamea": False,
            "is_coupDePied": False
        }

        self.player2 = {
            "x": 900,
            "y": 300,
            "health": 500,
            "last_attack_time": 0,
            "attack_cooldown": 2800,
            "current_animation": self.idle_animation_ken,
            "is_punching": False,
            "is_cameamea": False,
            "is_coupDePied": False
        }

        self.speed = 250

        # Initialiser les manettes
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def handle_joystick_input(self, delta_time):
        now = pygame.time.get_ticks()
        for idx, joystick in enumerate(self.joysticks):
        # Associer le joueur à sa manette
            if idx == 0:
                player = self.player1
                other_player = self.player2
            else:
                player = self.player2
                other_player = self.player1

            # --- MOUVEMENT ---
            axis_x = joystick.get_axis(0)
            deadzone = 0.2
            if abs(axis_x) > deadzone:
                new_x = player["x"] + axis_x * self.speed * delta_time
                new_x = max(0, min(new_x, 1280 - 150))

                new_hitbox = pygame.Rect(new_x, player["y"], 100, 230)
                other_hitbox = pygame.Rect(other_player["x"], other_player["y"], 100, 230)

                if not new_hitbox.colliderect(other_hitbox):
                    player["x"] = new_x

        # --- ATTAQUES ---

            if idx == 0:
                # RYU
                if joystick.get_button(1) and not player["is_coupDePied"] and not player["is_punching"] and not player["is_cameamea"]:
                    if now - player["last_attack_time"] >= player["attack_cooldown"]:
                        player["current_animation"] = self.coup_de_pied_animation
                        player["current_animation"].reset()
                        player["is_coupDePied"] = True
                        player["last_attack_time"] = now

                if joystick.get_button(2) and not player["is_punching"] and not player["is_coupDePied"] and not player["is_cameamea"]:
                    if now - player["last_attack_time"] >= player["attack_cooldown"]:
                        player["current_animation"] = self.punch_animation
                        player["current_animation"].reset()
                        player["is_punching"] = True
                        player["last_attack_time"] = now

                if joystick.get_button(3) and not player["is_cameamea"] and not player["is_punching"] and not player["is_coupDePied"]:
                    if now - player["last_attack_time"] >= player["cameamea_cooldown"]:
                        player["current_animation"] = self.cameamea_animation
                        player["current_animation"].reset()
                        player["is_cameamea"] = True
                        player["last_attack_time"] = now

                if player["is_cameamea"] and player["current_animation"].current_frame >= player["current_animation"].animation_steps - 1:
                    self.fireballs.append({
                        "x": player["x"] + 100,
                        "y": player["y"] + 20,
                        "animation": Animation(self.boule_de_feu_sprite_sheet, 20, 0.1, 45)
                    })
                    player["is_cameamea"] = False
                    player["current_animation"] = self.idle_animation

            else:
                # KEN
                if joystick.get_button(1) and not player["is_coupDePied"] and not player["is_punching"]:
                    if now - player["last_attack_time"] >= player["attack_cooldown"]:
                        player["current_animation"] = self.coupDePied_ken_animation
                        player["current_animation"].reset()
                        player["is_coupDePied"] = True
                        player["last_attack_time"] = now

                if joystick.get_button(2) and not player["is_punching"] and not player["is_coupDePied"]:
                    if now - player["last_attack_time"] >= player["attack_cooldown"]:
                        player["current_animation"] = self.coup_ken_animation
                        player["current_animation"].reset()
                        player["is_punching"] = True
                        player["last_attack_time"] = now


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

    def draw_health_bar(self, x, y, health, max_health=500, bar_width=400, bar_height=20):
        ratio = max(health, 0) / max_health  # Évite les valeurs négatives
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_width, bar_height))  # fond rouge
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, bar_width * ratio, bar_height))  # vert dynamique
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, bar_width, bar_height), 2)  # contour noir

    def run(self):
        while self.running:
            self.screen.blit(self.bg2, (0, 0))
            now = pygame.time.get_ticks()
            elapsed_time = now - self.start_time
            remaining_time = max(0, (self.game_duration - elapsed_time) // 1000)  # en secondes

            # Affichage du compteur
            font = pygame.font.SysFont("Arial", 40)
            timer_surface = font.render(f"{remaining_time:02}", True, (255, 255, 255))  # blanc
            self.screen.blit(timer_surface, (self.screen.get_width() // 2 - 20, 20))  # au centre haut

            delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_joystick_input(delta_time)


            # Boules de feu
            for fireball in self.fireballs + self.fireballs_ken:
                fireball["x"] += 50
                frame = fireball["animation"].animate(delta_time)
                if frame:
                    self.screen.blit(frame, (fireball["x"], fireball["y"]))
            self.fireballs = [f for f in self.fireballs if f["x"] < 1480]
            self.fireballs_ken = [f for f in self.fireballs_ken if f["x"] < 1480]

            # Joueurs
            self.update_player(self.player1, delta_time)
            self.update_player(self.player2, delta_time)

            self.draw_health_bar(50, 50, self.player1["health"])
            self.draw_health_bar(830, 50, self.player2["health"])

            # Gestion des collisions de coups
            player1_hitbox = pygame.Rect(self.player1["x"] + 30, self.player1["y"], 90, 230)
            player2_hitbox = pygame.Rect(self.player2["x"] + 30, self.player2["y"] + 70, 100, 230)
            # Dessiner les hitboxs pour le debug
            #pygame.draw.rect(self.screen, (255, 0, 0), player1_hitbox, 2)
            #pygame.draw.rect(self.screen, (0, 0, 255), player2_hitbox, 2)


            # Coup de poing Ryu → Ken
            if self.player1["is_punching"]:
                punch_hitbox = pygame.Rect(self.player1["x"] + 150, self.player1["y"] + 40, 40, 20)
                if punch_hitbox.colliderect(player2_hitbox):
                    self.player2["health"] -= 7
                    self.player1["is_punching"] = False
                #pygame.draw.rect(self.screen, (255, 255, 0), punch_hitbox, 2)  # debug 

            if self.player1["is_coupDePied"]:
                punch_hitbox = pygame.Rect(self.player1["x"] + 150, self.player1["y"] + 40, 40, 20)
                if punch_hitbox.colliderect(player2_hitbox):
                    self.player2["health"] -= 5
                    self.player1["is_coupDePied"] = False
                #pygame.draw.rect(self.screen, (255, 255, 0), punch_hitbox, 2)  # debug 
            
            # Collision des boules de feu de Ryu sur Ken
            for fireball in self.fireballs:
                fireball_hitbox = pygame.Rect(fireball["x"], fireball["y"], 40, 20)
                #pygame.draw.rect(self.screen, (255, 255, 0), fireball_hitbox, 2)  # debug 

                if fireball_hitbox.colliderect(player2_hitbox):
                    self.player2["health"] -= 100
                    self.fireballs.remove(fireball)


            # Coup de poing Ken → Ryu
            if self.player2["is_punching"]:
                punch_hitbox_ken = pygame.Rect(self.player2["x"] - 40, self.player2["y"] + 40, 40, 20)
                if punch_hitbox_ken.colliderect(player1_hitbox):
                    self.player1["health"] -= 7
                    self.player2["is_punching"] = False
                #pygame.draw.rect(self.screen, (255, 255, 0), punch_hitbox_ken, 2)  # debug 

            if self.player2["is_coupDePied"]:
                punch_hitbox_ken = pygame.Rect(self.player2["x"] - 40, self.player2["y"] + 40, 40, 20)
                if punch_hitbox_ken.colliderect(player1_hitbox):
                    self.player1["health"] -= 5
                    self.player2["is_coupDePied"] = False
                #pygame.draw.rect(self.screen, (255, 255, 0), punch_hitbox_ken, 2)  # debug 



            # Fin du combat si un joueur a 0 PV
            if self.player1["health"] <= 0:
                self.winner = "ken"
                game_over_screen = GameOverScreen(self.screen, self.winner)
                result = game_over_screen.run()
                self.running = False
            elif self.player2["health"] <= 0:
                self.winner = "Ryu"
                game_over_screen = GameOverScreen(self.screen, self.winner)
                result = game_over_screen.run()
                self.running = False
                print("💥 Ryu gagne !")

            pygame.display.flip()

        pygame.quit()
        print("👋 Déconnexion du serveur.")