import pygame
from SpriteSheet import SpriteSheet
from Animation import Animation
from option import OptionsMenu  # Importation du module option
from gameOver import GameOverScreen  # Importation du module game over
import json
import os
import time

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
        self.winner = None  # Suivi du gagnant

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
        self.coup_ken_animation = Animation(self.sprite_sheet_coup, 3, 0.15, 83, loop=False)
        self.coupDePied_ken_animation = Animation(self.sprite_sheet_coupDePied, 3, 0.15, 83, loop=False)

        # Joueurs avec points de vie
        self.player1 = {
            "x": 50,
            "y": 350,
            "hp": 100,  # Points de vie initiaux pour Ryu
            "current_animation": self.idle_animation,
            "is_punching": False,
            "is_cameamea": False,
            "is_coupDePied": False
        }

        self.player2 = {
            "x": 900,
            "y": 300,
            "hp": 100,  # Points de vie initiaux pour Ken
            "current_animation": self.idle_animation_ken,
            "is_punching": False,
            "is_cameamea": False,
            "is_coupDePied": False
        }

        self.speed = 300

        # Touches configurées (valeurs par défaut)
        self.kick_button = 1
        self.punch_button = 2
        self.hadouken_button = 3
        self.options_button = 9  # Bouton Options sur la manette PS5

        # Charger les paramètres depuis settings.json si disponible
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    self.kick_button = settings.get("kick_button", self.kick_button)
                    self.punch_button = settings.get("punch_button", self.punch_button)
                    self.hadouken_button = settings.get("hadouken_button", self.hadouken_button)
                    self.speed = settings.get("axis_sensitivity", self.speed) * 1500  # Ajuster la vitesse selon la sensibilité
            except Exception as e:
                print(f"❌ Erreur de chargement des paramètres : {e}")

        # Initialiser les manettes
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

        # Délai pour le bouton Options
        self.last_options_press = 0
        self.options_delay = 0.5  # 500ms entre chaque activation

    def handle_joystick_input(self, delta_time):
        for idx, joystick in enumerate(self.joysticks):
            if idx == 0:
                # 🎮 Manette 0 -> contrôle Ryu
                player = self.player1
                opponent = self.player2
            else:
                # 🎮 Manette 1 -> contrôle Ken
                player = self.player2
                opponent = self.player1

            # Déplacement
            axis_x = joystick.get_axis(0)
            deadzone = 0.2
            if abs(axis_x) > deadzone:
                player["x"] += axis_x * self.speed * delta_time
                player["x"] = max(0, min(player["x"], 1280 - 150))

            # Attaques (Ryu)
            if idx == 0:
                if joystick.get_button(self.kick_button) and not player["is_coupDePied"] and not player["is_punching"] and not player["is_cameamea"]:
                    player["current_animation"] = self.coup_de_pied_animation
                    player["current_animation"].reset()
                    player["is_coupDePied"] = True
                    # Vérifier collision pour coup de pied
                    if self.check_collision(player, opponent, attack_type="kick"):
                        opponent["hp"] = max(0, opponent["hp"] - 15)  # 15 dégâts pour coup de pied
                        print(f"💥 Ryu touche Ken ! Vie de Ken : {opponent['hp']}")

                if joystick.get_button(self.punch_button) and not player["is_punching"] and not player["is_coupDePied"] and not player["is_cameamea"]:
                    player["current_animation"] = self.punch_animation
                    player["current_animation"].reset()
                    player["is_punching"] = True
                    # Vérifier collision pour coup de poing
                    if self.check_collision(player, opponent, attack_type="punch"):
                        opponent["hp"] = max(0, opponent["hp"] - 10)  # 10 dégâts pour coup de poing
                        print(f"💥 Ryu touche Ken ! Vie de Ken : {opponent['hp']}")

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

            # Attaques (Ken)
            if idx == 1:
                if joystick.get_button(self.kick_button) and not player["is_coupDePied"] and not player["is_punching"]:
                    player["current_animation"] = self.coupDePied_ken_animation
                    player["current_animation"].reset()
                    player["is_coupDePied"] = True
                    # Vérifier collision pour coup de pied
                    if self.check_collision(player, opponent, attack_type="kick"):
                        opponent["hp"] = max(0, opponent["hp"] - 15)  # 15 dégâts pour coup de pied
                        print(f"💥 Ken touche Ryu ! Vie de Ryu : {opponent['hp']}")

                if joystick.get_button(self.punch_button) and not player["is_punching"] and not player["is_coupDePied"]:
                    player["current_animation"] = self.coup_ken_animation
                    player["current_animation"].reset()
                    player["is_punching"] = True
                    # Vérifier collision pour coup de poing
                    if self.check_collision(player, opponent, attack_type="punch"):
                        opponent["hp"] = max(0, opponent["hp"] - 10)  # 10 dégâts pour coup de poing
                        print(f"💥 Ken touche Ryu ! Vie de Ryu : {opponent['hp']}")

    def check_collision(self, attacker, target, attack_type):
        # Définir les hitboxes
        attacker_rect = pygame.Rect(attacker["x"], attacker["y"], 100, 200)  # Hitbox du joueur attaquant
        target_rect = pygame.Rect(target["x"], target["y"], 100, 200)  # Hitbox du joueur cible

        # Ajuster la hitbox pour les attaques de mêlée
        if attack_type in ["punch", "kick"]:
            if attacker == self.player1:  # Ryu attaque vers la droite
                attack_rect = pygame.Rect(attacker["x"] + 80, attacker["y"], 50, 100)
            else:  # Ken attaque vers la gauche
                attack_rect = pygame.Rect(attacker["x"] - 30, attacker["y"], 50, 100)
            return attack_rect.colliderect(target_rect)
        return False

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

    def draw_health_bars(self):
        # Barre de vie de Ryu (gauche)
        pygame.draw.rect(self.screen, (255, 0, 0), (50, 50, 200, 20))  # Fond rouge
        health_width = (self.player1["hp"] / 100) * 200
        pygame.draw.rect(self.screen, (0, 255, 0), (50, 50, health_width, 20))  # Vie verte

        # Barre de vie de Ken (droite)
        pygame.draw.rect(self.screen, (255, 0, 0), (1030, 50, 200, 20))  # Fond rouge
        health_width = (self.player2["hp"] / 100) * 200
        pygame.draw.rect(self.screen, (0, 255, 0), (1030, 50, health_width, 20))  # Vie verte

    def check_victory(self):
        # Vérifier si un joueur est mort
        if self.player1["hp"] <= 0 and self.player2["hp"] > 0:
            self.winner = "Ken"
        elif self.player2["hp"] <= 0 and self.player1["hp"] > 0:
            self.winner = "Ryu"
        elif self.player1["hp"] <= 0 and self.player2["hp"] <= 0:
            self.winner = "Match nul"  # Cas rare de double KO

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None

            # Vérifier si le bouton d'options est pressé avec un délai
            current_time = time.time()
            for joystick in self.joysticks:
                if joystick.get_button(self.options_button) and current_time - self.last_options_press > self.options_delay:
                    self.last_options_press = current_time
                    options_menu = OptionsMenu(self.screen, self)
                    result = options_menu.run()
                    if result == "return_to_menu":
                        self.running = False
                        return "return_to_menu"  # Retourner au menu principal

            self.handle_joystick_input(delta_time)

            # Vérifier collisions pour les boules de feu (Ryu)
            for fireball in self.fireballs[:]:
                fireball_rect = pygame.Rect(fireball["x"], fireball["y"], 45, 45)
                target_rect = pygame.Rect(self.player2["x"], self.player2["y"], 100, 200)
                if fireball_rect.colliderect(target_rect):
                    self.player2["hp"] = max(0, self.player2["hp"] - 20)  # 20 dégâts pour hadouken
                    print(f"💥 Hadouken touche Ken ! Vie de Ken : {self.player2['hp']}")
                    self.fireballs.remove(fireball)

            # Vérifier collisions pour les boules de feu (Ken, si implémenté)
            for fireball in self.fireballs_ken[:]:
                fireball_rect = pygame.Rect(fireball["x"], fireball["y"], 45, 45)
                target_rect = pygame.Rect(self.player1["x"], self.player1["y"], 100, 200)
                if fireball_rect.colliderect(target_rect):
                    self.player1["hp"] = max(0, self.player1["hp"] - 20)  # 20 dégâts pour hadouken
                    print(f"💥 Hadouken touche Ryu ! Vie de Ryu : {self.player1['hp']}")
                    self.fireballs_ken.remove(fireball)

            # Vérifier si un joueur est mort
            self.check_victory()
            if self.winner:
                # Afficher la page Game Over
                game_over_screen = GameOverScreen(self.screen, self.winner)
                result = game_over_screen.run()
                self.running = False
                return result  # Retourner "replay" ou "quit"

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

            # Afficher les barres de vie
            self.draw_health_bars()

            pygame.display.flip()

        return None  # Retour par défaut si le jeu se termine autrement