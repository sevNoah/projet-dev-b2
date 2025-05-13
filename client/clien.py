import socket
import pygame
from Button import Button
from Game import Game
from option import OptionsMenu  # Importation du module option
import time

# --- Configuration du serveur ---
HOST = "127.0.0.1"
PORT = 12346

# --- Initialisation du socket ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("✅ Connecté au serveur !")

# --- Initialisation de Pygame ---
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
game = Game()

# --- Chargement des backgrounds avec gestion d'erreur ---
def load_image(path, default_size=(100, 50)):
    try:
        return pygame.image.load(path).convert()
    except pygame.error:
        print(f"❌ Image introuvable : {path}")
        return pygame.Surface(default_size)

bg1 = load_image("../src/background/street-fighter-japanese-signs-1280x720.png")
current_bg = bg1

# --- Vérification et initialisation de la manette ---
if pygame.joystick.get_count() == 0:
    print("⚠️ Aucune manette détectée.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"🎮 Manette détectée : {joystick.get_name()}")

# --- Fonction pour envoyer un message au serveur ---
def send_to_server(message):
    try:
        client.send(message.encode())
    except Exception as e:
        print(f"❌ Erreur d'envoi : {e}")

# --- Chargement sécurisé des boutons ---
def load_button(image_path, pos):
    return Button(image=load_image(image_path), pos=pos)

TITTLE = load_button("../src/button/titre.png", (640, 150))
PLAY_BUTTON = load_button("../src/button/start_btn.png", (640, 300))
OPTIONS_BUTTON = load_button("../src/button/button_options.png", (640, 450))
QUIT_BUTTON = load_button("../src/button/button_quit.png", (640, 600))

button_list = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]
selected_index = 0
joystick_moved = False

# --- Délai entre les mouvements ---
last_move_time = time.time()
move_delay = 0.5

# --- Optimisation de l'animation des boutons ---
resized_images = {}

def get_scaled_image(button, scale_factor=1.2):
    if button not in resized_images:
        width = int(button.rect.width * scale_factor)
        height = int(button.rect.height * scale_factor)
        resized_images[button] = pygame.transform.scale(button.image, (width, height))
    return resized_images[button]

def animate_buttons():
    for i, button in enumerate(button_list):
        if i == selected_index:
            scaled_image = get_scaled_image(button)
            rect = scaled_image.get_rect(center=button.rect.center)
            screen.blit(scaled_image, rect)
        else:
            screen.blit(button.image, button.rect)

# --- Boucle principale ---
while running:
    screen.blit(current_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # --- Gestion du joystick ---
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1 and abs(event.value) > 0.5 and not joystick_moved:
                current_time = time.time()
                if current_time - last_move_time > move_delay:
                    selected_index = (selected_index + 1) % len(button_list) if event.value > 0 else (selected_index - 1) % len(button_list)
                    print(f"🎮 Bouton sélectionné : {selected_index}")
                    last_move_time = current_time
                    joystick_moved = True

            if abs(event.value) < 0.1:
                joystick_moved = False

        # --- Sélection avec le bouton X ---
        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
            print(f"✅ Bouton {selected_index} activé !")
            send_to_server(f"Bouton {selected_index} activé !")

            if button_list[selected_index] == PLAY_BUTTON:
                game.run()
            elif button_list[selected_index] == OPTIONS_BUTTON:
                options_menu = OptionsMenu(screen, game)  # Correction : passer game
                options_menu.run()
            elif button_list[selected_index] == QUIT_BUTTON:
                running = False

    # --- Animation des boutons ---
    animate_buttons()

    pygame.display.flip()
    clock.tick(60)

# --- Fermeture propre ---
pygame.quit()
client.close()
print("👋 Déconnexion du serveur.")