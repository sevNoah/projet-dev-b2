import pygame
import sys

class Clavier:
    def __init__(self, joystick_id=0):
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("⚠️ Aucune manette détectée.")
            pygame.quit()
            sys.exit()
        self.joystick = pygame.joystick.Joystick(joystick_id)
        self.joystick.init()

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Clavier virtuel manette")
        self.clock = pygame.time.Clock()

        self.keys = [
            list("ABCDEFGHIJKLM"),
            list("NOPQRSTUVWXYZ"),
            list("0123456789"),
            ["SPACE", "BACK", "ENTER"]
        ]

        self.row = 0
        self.col = 0
        self.pseudo = ""
        self.last_move_time = 0
        self.move_delay = 200  # en ms

        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

    def draw_keyboard(self):
        self.screen.fill((30, 30, 30))

        # Afficher pseudo
        pseudo_surface = self.font.render(f"Pseudo: {self.pseudo}", True, (255, 255, 255))
        self.screen.blit(pseudo_surface, (20, 20))

        key_width, key_height = 50, 50
        margin_x, margin_y = 20, 10
        start_y = 100

        for r, line in enumerate(self.keys):
            start_x = (self.screen.get_width() - (len(line) * (key_width + margin_x))) // 2
            for c, key in enumerate(line):
                x = start_x + c * (key_width + margin_x)
                y = start_y + r * (key_height + margin_y)
                rect = pygame.Rect(x, y, key_width, key_height)

                color = (200, 200, 50) if (r == self.row and c == self.col) else (100, 100, 100)
                pygame.draw.rect(self.screen, color, rect)

                text_surface = self.small_font.render(key, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)

    def move_cursor_horizontal(self, axis_val):
        now = pygame.time.get_ticks()
        if now - self.last_move_time < self.move_delay:
            return
        if axis_val < -0.5:
            self.col = (self.col - 1) % len(self.keys[self.row])
            self.last_move_time = now
        elif axis_val > 0.5:
            self.col = (self.col + 1) % len(self.keys[self.row])
            self.last_move_time = now

    def move_cursor_vertical(self, axis_val):
        now = pygame.time.get_ticks()
        if now - self.last_move_time < self.move_delay:
            return
        if axis_val < -0.5:
            self.row = (self.row - 1) % len(self.keys)
            self.col = min(self.col, len(self.keys[self.row]) - 1)
            self.last_move_time = now
        elif axis_val > 0.5:
            self.row = (self.row + 1) % len(self.keys)
            self.col = min(self.col, len(self.keys[self.row]) - 1)
            self.last_move_time = now

    def press_key(self):
        key = self.keys[self.row][self.col]
        if key == "BACK":
            self.pseudo = self.pseudo[:-1]
        elif key == "SPACE":
            self.pseudo += " "
        elif key == "ENTER":
            return True
        else:
            self.pseudo += key
        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.JOYAXISMOTION:
                    if event.joy == self.joystick.get_id():
                        if event.axis == 0:  # Horizontal
                            self.move_cursor_horizontal(event.value)
                        elif event.axis == 1:  # Vertical
                            self.move_cursor_vertical(event.value)

                if event.type == pygame.JOYBUTTONDOWN and event.joy == self.joystick.get_id():
                    if event.button == 0:  # Bouton X pour valider
                        if self.press_key():
                            running = False  # Validation

            self.draw_keyboard()
            pygame.display.flip()
            self.clock.tick(60)

        return self.pseudo
