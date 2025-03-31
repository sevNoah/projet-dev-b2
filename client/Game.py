import pygame
from SpriteSheet import SpriteSheet
from Animation import Animation

class Game:
    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Street Fighter Game")
        self.clock = pygame.time.Clock() 
        self.bg2 = pygame.image.load("../src/background/street_fighter_2.png").convert()
        self.sprite = pygame.image.load("../src/sprites/sprite_1.png").convert_alpha()
        self.sprite_coupDePoint = pygame.image.load("../src/sprites/spritecombat_coupDePoint.png").convert_alpha()

        self.running = True

        # Créer l'objet SpriteSheet
        self.sprite_sheet = SpriteSheet(self.sprite)
        self.punch_sprite_sheet = SpriteSheet(self.sprite_coupDePoint)

        # Créer les objets Animation
        self.idle_animation = Animation(self.sprite_sheet, 4, 0.1, 47)
        self.punch_animation = Animation(self.punch_sprite_sheet, 2, 0.1, 69)

        self.current_animation = self.idle_animation
        self.is_punching = False

        # Position du joueur
        self.player_x = 50
        self.player_y = 350  # Position fixe en Y
        self.speed = 300  # Pixels par seconde

        # Initialiser la manette
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

    def handle_joystick_input(self, delta_time):
        if self.joystick:
            # Obtenir la valeur de l'axe horizontal (X)
            axis_x = self.joystick.get_axis(0)  # Axe gauche-droite

            # Seuil pour éviter les petites variations
            deadzone = 0.2
            if abs(axis_x) > deadzone:
                self.player_x += axis_x * self.speed * delta_time

            # Limiter aux bords de l'\u00e9cran
            self.player_x = max(0, min(self.player_x, 1280 - 150))  # 150 = largeur du sprite

            # Coup de poing avec carr\u00e9 (bouton 2)
            if self.joystick.get_button(2):
                if not self.is_punching or self.current_animation == self.idle_animation:
                    self.current_animation = self.punch_animation
                    self.current_animation.reset()
                    self.is_punching = True

            # Transition fluide vers l'animation idle après le coup de poing
            if self.is_punching:
                if self.current_animation.current_frame >= self.current_animation.animation_steps:
                    if self.current_animation.animation_timer >= 0.2:
                        self.is_punching = False
                else:
                    self.player_x += (axis_x * self.speed * 0.5) * delta_time  # Mouvement réduit pendant le punch

            # Retour à l'animation idle si le coup de poing est terminé
            if not self.is_punching:
                self.current_animation = self.idle_animation


    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000  # Temps écoulé en secondes

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_joystick_input(delta_time)
            
            # Mise à jour de l'animation
            frame = self.current_animation.animate(delta_time)
            self.screen.blit(self.bg2, (0, 0))

            if frame:
                self.screen.blit(frame, (self.player_x, self.player_y))
            else:
                self.current_animation = self.idle_animation
                self.current_animation.reset()
                self.is_punching = False

            pygame.display.flip()

        pygame.quit()
        print("👋 Déconnexion du serveur.")