import pygame
import os
from Button import Button

class GameOverScreen:
    def __init__(self, screen, winner):
        self.screen = screen
        self.winner = winner  # Nom du gagnant (par exemple, "Ryu" ou "Ken")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 72)  # Police pour "Game Over" et gagnant
        self.button_font = pygame.font.SysFont(None, 48)  # Police pour boutons
        self.running = True

        # Initialisation du joystick
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("⚠️ Aucune manette détectée.")
            pygame.quit()
            exit()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Chargement sécurisé des images des boutons
        def load_image(path, default_size=(100, 50)):
            try:
                return pygame.image.load(path).convert_alpha()
            except pygame.error:
                print(f"❌ Image introuvable : {path}")
                return pygame.Surface(default_size)

        # Boutons (réutilisation des images de clien.py si disponibles)
        self.replay_button = Button(image=load_image("../src/button/start_btn.png"), pos=(640, 400))
        self.quit_button = Button(image=load_image("../src/button/button_quit.png"), pos=(640, 500))
        self.button_list = [self.replay_button, self.quit_button]
        self.selected_index = 0
        self.joystick_moved = False
        self.last_move_time = 0
        self.move_delay = 0.5  # Délai entre les mouvements

        # Cache pour les images redimensionnées
        self.resized_images = {}

    def get_scaled_image(self, button, scale_factor=1.2):
        if button not in self.resized_images:
            width = int(button.rect.width * scale_factor)
            height = int(button.rect.height * scale_factor)
            self.resized_images[button] = pygame.transform.scale(button.image, (width, height))
        return self.resized_images[button]

    def animate_buttons(self):
        for i, button in enumerate(self.button_list):
            if i == self.selected_index:
                scaled_image = self.get_scaled_image(button)
                rect = scaled_image.get_rect(center=button.rect.center)
                self.screen.blit(scaled_image, rect)
            else:
                self.screen.blit(button.image, button.rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"

                # Gestion du joystick
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 1 and abs(event.value) > 0.5 and not self.joystick_moved:
                        current_time = time.time()
                        if current_time - self.last_move_time > self.move_delay:
                            self.selected_index = (self.selected_index + 1) % len(self.button_list) if event.value > 0 else (self.selected_index - 1) % len(self.button_list)
                            print(f"🎮 Bouton sélectionné : {self.selected_index}")
                            self.last_move_time = current_time
                            self.joystick_moved = True

                    if abs(event.value) < 0.1:
                        self.joystick_moved = False

                # Sélection avec le bouton X
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    print(f"✅ Bouton {self.selected_index} activé !")
                    if self.button_list[self.selected_index] == self.replay_button:
                        self.running = False
                        return "replay"
                    elif self.button_list[self.selected_index] == self.quit_button:
                        # Supprimer settings.json avant de quitter
                        if os.path.exists("settings.json"):
                            os.remove("settings.json")
                        self.running = False
                        return "quit"

            # Affichage
            self.screen.fill((0, 0, 0))  # Fond noir
            game_over_text = self.font.render("Game Over", True, (255, 255, 255))
            winner_text = self.font.render(f"Winner: {self.winner}", True, (255, 255, 255))
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 100))
            self.screen.blit(winner_text, (self.screen.get_width() // 2 - winner_text.get_width() // 2, 200))

            # Animation des boutons
            self.animate_buttons()

            pygame.display.flip()
            self.clock.tick(60)

        return "quit"  # Par défaut, quitter si la boucle se termine 