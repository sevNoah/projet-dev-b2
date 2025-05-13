import pygame
import sys

class OptionsMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.options = [
            {"name": "Axis Sensitivity", "value": 0.2, "min": 0.1, "max": 0.5, "step": 0.05, "type": "range"},
            {"name": "Kick Button", "value": 1, "type": "button"},
            {"name": "Punch Button", "value": 2, "type": "button"},
            {"name": "Hadouken Button", "value": 3, "type": "button"},
            {"name": "Return", "type": "return"},
            {"name": "Quit", "type": "quit"}
        ]
        self.selected_option = 0
        self.waiting_for_input = False
        self.input_prompt = ""

        # Dictionary to map button codes to controller button names
        self.button_names = {
            0: "X",
            1: "Circle",
            2: "Square",
            3: "Triangle",
            4: "L1",
            5: "R1",
            6: "L2",
            7: "R2",
            8: "Share",
            9: "Options",
            10: "L3",
            11: "R3",
            12: "PS",
            13: "Touchpad"
        }

        # Initialize joysticks
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.waiting_for_input:
                    if event.key == pygame.K_ESCAPE:
                        self.waiting_for_input = False
                    else:
                        self.options[self.selected_option]["value"] = event.key
                        self.waiting_for_input = False
                else:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_LEFT:
                        self.adjust_option(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.adjust_option(1)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected_option]["type"] == "button":
                            self.waiting_for_input = True
                            self.input_prompt = f"Press a key for {self.options[self.selected_option]['name']}"
                        elif self.options[self.selected_option]["type"] == "return":
                            self.save_and_exit()
                        elif self.options[self.selected_option]["type"] == "quit":
                            pygame.quit()
                            sys.exit()
                        else:
                            self.save_and_exit()
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 and abs(event.value) > 0.5:
                    if not self.waiting_for_input:
                        self.selected_option = (self.selected_option + 1) % len(self.options) if event.value > 0 else (self.selected_option - 1) % len(self.options)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # X button
                    if self.waiting_for_input:
                        self.waiting_for_input = False
                    else:
                        if self.options[self.selected_option]["type"] == "button":
                            self.waiting_for_input = True
                            self.input_prompt = f"Press a button for {self.options[self.selected_option]['name']}"
                        elif self.options[self.selected_option]["type"] == "return":
                            self.save_and_exit()
                        elif self.options[self.selected_option]["type"] == "quit":
                            pygame.quit()
                            sys.exit()
                        else:
                            self.save_and_exit()
                elif self.waiting_for_input:
                    self.options[self.selected_option]["value"] = event.button
                    self.waiting_for_input = False
                    self.update_game_buttons()

    def adjust_option(self, direction):
        option = self.options[self.selected_option]
        if "min" in option and "max" in option:
            option["value"] = max(option["min"], min(option["max"], option["value"] + direction * option.get("step", 1)))

    def update_game_buttons(self):
        # Update game buttons with configured values
        for option in self.options:
            if option["name"] == "Kick Button":
                self.game.kick_button = option["value"]
            elif option["name"] == "Punch Button":
                self.game.punch_button = option["value"]
            elif option["name"] == "Hadouken Button":
                self.game.hadouken_button = option["value"]

    def save_and_exit(self):
        self.update_game_buttons()
        self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Controller Options", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            if option["type"] == "button":
                button_name = self.button_names.get(option["value"], "Unknown")
                text = self.font.render(f"{option['name']}: {button_name}", True, color)
            elif option["type"] in ["return", "quit"]:
                text = self.font.render(f"{option['name']}", True, color)
            else:
                text = self.font.render(f"{option['name']}: {option['value']}", True, color)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 100 + i * 50))

        if self.waiting_for_input:
            prompt = self.font.render(self.input_prompt, True, (255, 255, 0))
            self.screen.blit(prompt, (self.screen.get_width() // 2 - prompt.get_width() // 2, 300))

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)