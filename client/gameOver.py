import pygame
import os
import time
from Button import Button

class Animation:
    def __init__(self, from_images, image_paths=None, sprite_sheet=None, animation_steps=0, animation_speed=150, position=(0,0), scale=1, y_offset=0, loop=True):
        self.frames = []
        self.position = position
        self.animation_speed = animation_speed  # en millisecondes
        self.loop = loop
        self.current_frame = 0
        self.animation_timer = 0
        self.finished = False
        self.scale = scale

        if from_images:
            # Charger chaque image individuelle
            for path in image_paths:
                image = pygame.image.load(path).convert_alpha()
                width, height = image.get_size()
                image = pygame.transform.scale(image, (width * scale, height * scale))
                self.frames.append(image)
        else:
            # Chargement depuis une sprite sheet (non utilisé ici mais prévu)
            self.animation_steps = animation_steps
            self.sprite_sheet = sprite_sheet
            for x in range(animation_steps):
                frame = self.sprite_sheet.get_image(x, y_offset, 150, scale)
                self.frames.append(frame)

    def animate(self, delta_time):
        if self.finished:
            return self.frames[-1]

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
        return self.frames[self.current_frame]

    def draw(self, screen):
        if self.frames:
            screen.blit(self.frames[self.current_frame], self.position)

    def reset(self):
        self.current_frame = 0
        self.animation_timer = 0
        self.finished = False

class GameOverScreen:
    def __init__(self, screen, winner):
        self.screen = screen
        self.winner = winner
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 48)
        self.running = True
        self.bg = pygame.image.load("../src/background/street_fighter_2.png").convert()

        # 🔁 Animation de KO Ken
        ken_paths = [
            "../src/sprites/ken/ko/frame1.png",
            "../src/sprites/ken/ko/frame2.png",
            "../src/sprites/ken/ko/frame3.png",
            "../src/sprites/ken/ko/frame4.png"
        ]
        self.ken_animation = Animation(
            from_images=True,
            image_paths=ken_paths,
            animation_speed=150,
            position=(900, 450),
            scale=3,
            loop=False
        )

        # 🔁 Animation de KO Ryu
        ryu_paths = [
            "../src/sprites/ryu/ko/frameR1.png",
            "../src/sprites/ryu/ko/frameR2.png",
            "../src/sprites/ryu/ko/frameR3.png",
            "../src/sprites/ryu/ko/frameR4.png",
            "../src/sprites/ryu/ko/frameR5.png",
            "../src/sprites/ryu/ko/frameR6.png",
            "../src/sprites/ryu/ko/frameR7.png"
        ]
        self.ryu_animation = Animation(
            from_images=True,
            image_paths=ryu_paths,
            animation_speed=300,
            position=(50, 450),
            scale=3,
            loop=False
        )

        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("⚠️ Aucune manette détectée.")
            pygame.quit()
            exit()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.menu_surface = pygame.Surface((150, 60))

    def run(self):
        while self.running:
            self.screen.blit(self.bg, (0, 0))

            # 🌀 Affiche uniquement l'animation du perdant
            if self.winner == "Ryu":
                self.ken_animation.draw(self.screen)
            elif self.winner == "Ken":
                self.ryu_animation.draw(self.screen)

            # Mettre à jour l'animation (important)
            delta = self.clock.tick(60)
            if self.winner == "Ryu":
                self.ken_animation.animate(delta)
            elif self.winner == "Ken":
                self.ryu_animation.animate(delta)

            # Texte Game Over
            text = self.font.render(f"{self.winner} wins!" if self.winner in ["Ryu", "Ken"] else "Draw!", True, (255, 255, 255))
            replay_text = pygame.font.SysFont("Arial", 40).render("Press X pour recommencer ou O pour quitter", True, (200, 200, 200))

            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 50))
            self.screen.blit(replay_text, (self.screen.get_width() // 2 - replay_text.get_width() // 2, 150))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:  # START
                        return True
                    if event.button == 1:  # BACK
                        return False
