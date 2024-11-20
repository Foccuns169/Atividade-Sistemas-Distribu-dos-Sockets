import socket
import threading
import os

SOCKET_PATH = "/tmp/socket_server"

def handle_client(client_socket, client_address):
    try:
        
        client_id = client_socket.recv(1024).decode('utf-8')
        print(f"Cliente conectado: {client_id}")

        while True:
            
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  
            print(f"Mensagem de {client_id}: {message}")
    except Exception as e:
        print(f"Erro ao lidar com o cliente {client_address}: {e}")
    finally:
        print(f"Cliente {client_address} desconectado")
        client_socket.close()

def start_server():
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)
    print("Servidor iniciado. Aguardando conexões...")

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Encerrando o servidor...")
    finally:
        server.close()
        os.unlink(SOCKET_PATH)

if __name__ == "__main__":
    start_server()
