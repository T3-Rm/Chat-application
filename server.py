
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

clients = []
names = []
lock = threading.Lock()


def broadcast(message, sender=None):
    with lock:
        recipients = [
            client for client in clients if client != sender
        ]

    for client in recipients:
        try:
            client.sendall(message.encode("utf-8"))
        except OSError:
            pass


def handle_client(client):
    name = "A user"

    try:
        name = client.recv(1024).decode("utf-8").strip()
        if not name:
            name = "Anonymous"

        with lock:
            clients.append(client)
            names.append(name)

        broadcast(f"{name} joined the chat!\n", sender=client)

        while True:
            message = client.recv(1024).decode("utf-8").strip()

            if not message or message.lower() == "exit":
                break

            timestamp = datetime.now().strftime("%H:%M")
            broadcast(f"[{timestamp}] {name}: {message}\n")

    except (ConnectionError, OSError):
        pass

    finally:
        with lock:
            if client in clients:
                index = clients.index(client)
                clients.pop(index)
                names.pop(index)

        client.close()
        broadcast(f"{name} disconnected.\n")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Chat server running on {HOST}:{PORT}")
    print("Waiting for users...")

    try:
        while True:
            client, address = server.accept()
            print("Connected:", address)

            thread = threading.Thread(
                target=handle_client,
                args=(client,),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.close()


if __name__ == "__main__":
    main()
