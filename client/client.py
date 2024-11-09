import socket
import threading
from typing import NoReturn

# Client configuration
SERVER_HOST: str = 'localhost'
SERVER_PORT: int = 5000
BUFFER_SIZE: int = 1024

def receive_messages(client_socket: socket.socket, username: str) -> NoReturn:
    """Receive and display messages from the server."""
    while True:
        try:
            message: str = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not message.startswith(f"{username}:"):
                print(f"\n{message}")
        except Exception as e:
            print(f"Connection to server lost: {e}")

    # This line is never reached, but satisfies type checking
    raise RuntimeError("This code should never be reached")

def start_client() -> None:
    """Initialize and run the chat client."""
    client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")
    except:
        print("Could not connect to server.")
        return

    # Handle username process
    username_prompt: str = client.recv(BUFFER_SIZE).decode('utf-8')
    print(username_prompt, end='')
    username: str = input()
    client.send(username.encode('utf-8'))

    # Start thread for receiving messages
    receive_thread: threading.Thread = threading.Thread(target=receive_messages, args=(client, username))
    receive_thread.start()
    
    # Main loop for sending messages
    while True:
        try:
            message: str = input(f"{username}> ")
            if message:
                client.send(message.encode('utf-8'))
        except:
            print("Could not send the message.")
            break

    client.close()

if __name__ == "__main__":
    start_client()