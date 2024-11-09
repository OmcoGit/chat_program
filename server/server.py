import socket
import threading
from typing import Dict, Tuple, Optional

# Server configuration
SERVER_IP: str = '0.0.0.0'
SERVER_PORT: int = 5000
BUFFER_SIZE: int = 1024

# Store connected clients: {socket: username}
clients: Dict[socket.socket, str] = {}

def pushToAll(message: str, sender_socket: socket.socket) -> None:
    """Broadcast message to all clients except the sender."""
    sender_username = clients[sender_socket]
    formatted_message = f"{sender_username}: {message}"
    for client_socket, username in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(formatted_message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to {username}: {e}")
                del clients[client_socket]
                client_socket.close()

def manage_client(client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
    """Handle communication with a single client."""
    client_socket.send("Enter your username: ".encode('utf-8'))
    username: str = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
    clients[client_socket] = username
    
    pushToAll("\nhas joined the chat!", client_socket)
    
    # Main client communication loop: receive and broadcast messages
    while True:
        try:
            message: Optional[str] = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not message:
                break
            print(f"{username}: {message}")
            pushToAll(message, client_socket)
        except:
            break
     # Clean up when client disconnects
    del clients[client_socket]
    pushToAll("has left the chat.", client_socket)
    client_socket.close()

def start_server() -> None:
    """Initialize the server and handle new client connections."""
    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        
        client_thread: threading.Thread = threading.Thread(target=manage_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()