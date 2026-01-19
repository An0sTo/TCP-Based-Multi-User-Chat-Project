import socket
import threading

# Server configuration
IP = '127.0.0.1'
PORT = 55555
clients = {}  # Stores {Name: Socket}


def broadcast_user_list():
    # Sends the current list of online users to everyone
    user_list_msg = "LIST:" + ",".join(clients.keys())
    for client_socket in clients.values():
        try:
            client_socket.send(user_list_msg.encode('utf-8'))
        except:
            continue


def broadcast_announcement(message):
    # Sends system announcements (Join/Leave) to everyone
    for client_socket in clients.values():
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            continue


def handle_client(client_socket, address):
    name = None
    try:
        # Step 1: Receive name and normalize (Avi == avi)
        raw_name = client_socket.recv(1024).decode('utf-8').strip()
        if not raw_name: return
        name = raw_name.capitalize()

        # Step 2: Validation - Is name taken?
        if name in clients:
            client_socket.send("ERR_NAME_TAKEN".encode('utf-8'))
            client_socket.close()
            return

        # Step 3: Registration
        clients[name] = client_socket
        print(f"[CONNECTED] {name} from {address}")
        broadcast_user_list()
        broadcast_announcement(f"--- {name} HAS JOINED THE CHAT! ---")

        while True:
            # Step 4: Communication Loop
            data = client_socket.recv(1024).decode('utf-8')
            if not data: break

            if ":" in data:
                target, msg = data.split(":", 1)
                target = target.strip().capitalize()

                # Validation: Can't message yourself
                if target == name:
                    client_socket.send("[SYSTEM] You cannot message yourself.".encode('utf-8'))
                elif target in clients:
                    clients[target].send(f"From {name}: {msg}".encode('utf-8'))
                else:
                    client_socket.send(f"[SYSTEM] User '{target}' does not exist.".encode('utf-8'))

    except:
        pass
    finally:
        # Step 5: Safe Cleanup - Only delete if this socket is the owner of the name
        if name and clients.get(name) == client_socket:
            del clients[name]
            print(f"[DISCONNECTED] {name}")
            broadcast_announcement(f"--- {name} HAS LEFT THE CHAT! ---")
            broadcast_user_list()
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(10)
    print(f"Server is running on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
