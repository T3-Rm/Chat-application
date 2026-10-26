
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    while True:
        try:
            message = client.recv(4096).decode("utf-8")

            if not message:
                break

            print(message, end="")

        except OSError:
            break

    print("\nDisconnected from the chat server.")


def main():
    name = input("Enter your name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        client.sendall(name.encode("utf-8"))

        threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        ).start()

        print("Connected! Type a message and press Enter.")
        print("Type 'exit' to leave the chat.")

        while True:
            message = input()

            if message.lower() == "exit":
                client.sendall(b"exit")
                break

            client.sendall(message.encode("utf-8"))

    except ConnectionRefusedError:
        print("Server not running. Start server.py first.")

    except OSError as error:
        print("Connection error:", error)

    finally:
        client.close()


if __name__ == "__main__":
    main()
