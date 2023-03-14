import socket
import threading
import os

def handle_client(client_socket):
    # Envoyer un message d'accueil au client
    client_socket.send("220 Welcome to the FTP server\r\n".encode())

    # Attendre que le client envoie une commande
    while True:
        command = client_socket.recv(1024).decode().strip()
        if not command:
            continue

        # Gérer les commandes du client
        if command.startswith("USER "):
            client_socket.send("331 Username OK, password required\r\n".encode())
        elif command.startswith("PASS "):
            client_socket.send("230 Password OK, logged in\r\n".encode())
        elif command.startswith("STOR "):
            filename = command[5:]
            with open(filename, "wb") as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            client_socket.send("226 File transfer complete\r\n".encode())
        elif command.startswith("QUIT"):
            client_socket.send("221 Goodbye!\r\n".encode())
            break
        else:
            client_socket.send("500 Command not recognized\r\n".encode())

    # Fermer la connexion avec le client
    client_socket.close()

def run_server():
    # Créer un socket pour écouter les connexions entrantes
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 21))
    server_socket.listen()

    # Attendre les connexions entrantes et créer un thread pour chaque client
    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    run_server()