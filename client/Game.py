import pygame
from SpriteSheet import SpriteSheet

class Game:
    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Street Fighter Game")
        self.clock = pygame.time.Clock() 
        self.bg2 = pygame.image.load("../src/background/street_fighter_2.png").convert()
        self.sprite = pygame.image.load("../src/sprites/sprite_1.png").convert_alpha()
        
        self.running = True

        # Créer l'objet SpriteSheet
        self.sprite_sheet = SpriteSheet(self.sprite)

        # Créer la liste d'animation
        self.animation_list = []
        self.animation_steps = 4  # Nombre de frames dans l'animation

        # Découper les frames de l'animation et les ajouter à la liste
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, 46, 120, 3))

        self.current_frame = 0  # Frame actuelle pour l'animation

        # Contrôler la vitesse de l'animation
        self.frame_delay = 90 
        self.last_frame_time = pygame.time.get_ticks() 

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Si le délai entre les frames est écoulé
        if current_time - self.last_frame_time >= self.frame_delay:
            # Positionner le sprite joueur 1
            self.screen.blit(self.animation_list[self.current_frame], (50, 350))  # Centrer l'animation

            # Passer à la frame suivante
            self.current_frame = (self.current_frame + 1) % self.animation_steps  # Passer à la frame suivante, revenir à 0 si nécessaire

            self.last_frame_time = current_time  # Mettre à jour l'heure du dernier changement de frame

    def run(self):
        while self.running:
            self.clock.tick(10)  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.bg2, (0, 0))

            self.animate()

            pygame.display.flip()

        pygame.quit()
        print("👋 Déconnexion du serveur.")
