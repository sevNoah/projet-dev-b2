import socket
import pygame
from Button import Button
import time  # Importer la bibliothèque time

# --- Configuration du serveur ---
HOST = "127.0.0.1"
PORT = 12346

# --- Initialisation du socket ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  # Connexion au serveur
print("✅ Connecté au serveur !")

# --- Initialisation de Pygame ---
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# --- Chargement des backgrounds ---
bg1 = pygame.image.load("../src/street-fighter-japanese-signs-1280x720.png").convert()
bg2 = pygame.image.load("../src/street_fighter_1.png").convert()
current_bg = bg1  # Arrière-plan par défaut

# --- Vérification de la manette ---
if pygame.joystick.get_count() == 0:
    print("⚠️ Aucune manette détectée.")
    pygame.quit()
    exit()

# --- Initialisation de la manette ---
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"🎮 Manette détectée : {joystick.get_name()}")

# --- Fonction pour envoyer un message au serveur ---
def send_to_server(message):
    try:
        client.send(message.encode())  # Encode le message en bytes
    except Exception as e:
        print(f"❌ Erreur d'envoi : {e}")

# --- Initialisation des boutons ---
PLAY_BUTTON = Button(
    image=pygame.image.load("../src/start_btn.png"),
    pos=(640, 300)
)
OPTIONS_BUTTON = Button(
    image=pygame.image.load("../src/button_options.png"),
    pos=(640, 450)
)
QUIT_BUTTON = Button(
    image=pygame.image.load("../src/button_quit.png"),
    pos=(640, 600)
)

button_list = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]  # Liste des boutons
selected_index = 0  # Par défaut, le premier bouton est sélectionné
joystick_moved = False  # Évite les mouvements rapides

# --- Ajout d'un délai entre les changements ---
last_move_time = time.time()  
move_delay = 0.5  

# --- Fonction pour redimensionner les boutons pour l'animation ---
def animate_buttons():
    for i, button in enumerate(button_list):
        if i == selected_index:
            # Augmente légèrement la taille pour le bouton sélectionné
            scaled_image = pygame.transform.scale(button.image, 
                                                  (button.rect.width + 20, button.rect.height + 20))
            rect = scaled_image.get_rect(center=(button.rect.center))
            screen.blit(scaled_image, rect)
        else:
            # Taille normale pour les autres boutons
            screen.blit(button.image, button.rect)

# --- Boucle principale ---
while running:
    screen.blit(current_bg, (0, 0))  # Affiche l'arrière-plan

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # --- Gestion du joystick pour la navigation (axes) ---
        if event.type == pygame.JOYAXISMOTION:
            # Axe vertical (Y) - Descendre/Monter dans le menu
            if event.axis == 1 and abs(event.value) > 0.5 and not joystick_moved:
                # Vérifie si assez de temps s'est écoulé
                current_time = time.time()
                if current_time - last_move_time > move_delay:  # Si le délai est écoulé
                    if event.value > 0:  # Vers le bas
                        selected_index = (selected_index + 1) % len(button_list)
                    else:  # Vers le haut
                        selected_index = (selected_index - 1) % len(button_list)
                    print(f"🎮 Bouton sélectionné : {selected_index}")
                    last_move_time = current_time  # Met à jour l'heure du dernier mouvement
                    joystick_moved = True  # Évite les mouvements rapides

            # Relâchement de l'axe pour permettre un autre mouvement
            if abs(event.value) < 0.1:
                joystick_moved = False

        # --- Sélection du bouton avec le bouton X ---
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # Bouton X (PS5)
                print(f"✅ {button_list[selected_index].text_input} activé !")
                send_to_server(f"{button_list[selected_index].text_input} activé !")

                # Exemple de comportement :
                if button_list[selected_index] == PLAY_BUTTON:
                    current_bg = bg2 if current_bg == bg1 else bg1
                elif button_list[selected_index] == OPTIONS_BUTTON:
                    print("⚙️ Options ouvertes !")
                elif button_list[selected_index] == QUIT_BUTTON:
                    running = False

    # --- Animation et affichage des boutons ---
    animate_buttons()

    pygame.display.flip()
    clock.tick(60)

# --- Fermeture propre ---
pygame.quit()
client.close()
print("👋 Déconnexion du serveur.")
