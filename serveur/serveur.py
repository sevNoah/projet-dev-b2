import socket

host = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
port = 12346  # Change de port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permet de réutiliser le port immédiatement
server.bind((host, port))
server.listen(5)

print(f"📡 Serveur en attente de connexion sur le port {port}...")

while True:
    try:
        conn, addr = server.accept()
        print(f"✅ Connexion établie avec {addr}")
        
        # Boucle pour recevoir des données en continu
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break  # Si aucune donnée reçue, quitter la boucle
            print(f"🎮 Données reçues : {data}")
        
        conn.close()
        print(f"❌ Connexion fermée avec {addr}")
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
