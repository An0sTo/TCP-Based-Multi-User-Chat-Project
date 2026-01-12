import socket
import threading


class ChatClientLogic:
    def __init__(self, ip='127.0.0.1', port=55555):
        self.ip, self.port = ip, port
        self.client_socket = None
        self.on_message_received = None

    def connect(self, name):
        try:
            # Create a fresh socket for every attempt
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip, self.port))
            self.client_socket.send(name.encode('utf-8'))

            threading.Thread(target=self._receive_loop, daemon=True).start()
            return True
        except:
            return False

    def _receive_loop(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message and self.on_message_received:
                    self.on_message_received(message)
                if not message: break
            except:
                break

    def send_message(self, message):
        try:
            if self.client_socket:
                self.client_socket.send(message.encode('utf-8'))
        except:
            pass

    def disconnect(self):
        try:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
        except:
            pass