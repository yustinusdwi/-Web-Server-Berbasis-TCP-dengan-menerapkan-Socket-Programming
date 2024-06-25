import socket
import threading

def handle_client(connection, address):
    try:
        print(f'Connection from {address}')

        # Menerima data dalam bentuk byte
        data = connection.recv(1024)
        print(f'Received: {data.decode()}')

        # Parse request HTTP
        request_method = data.decode().split()[0]
        requested_file = data.decode().split()[1][1:]

        # Membaca file yang diminta
        try:
            with open(requested_file, 'rb') as file:
                response_body = file.read()
            # Membuat response HTTP
            response_headers = 'HTTP/1.1 200 OK\n\n'
        except FileNotFoundError:
            response_body = b'404 Not Found'
            response_headers = 'HTTP/1.1 404 Not Found\n\n'

        # Mengirim response ke klien
        response = response_headers.encode() + response_body
        connection.sendall(response)

    finally:
        # Menutup koneksi
        connection.close()

def start_server():
    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mendapatkan localhost dan port
    server_address = ('192.168.56.1', 8000)
    print(f'Starting server on {server_address[0]} port {server_address[1]}')

    # Mengikat socket ke alamat server
    server_socket.bind(server_address)

    # Mendengarkan koneksi masuk
    server_socket.listen(5)  # Mengizinkan maksimal 5 koneksi dalam antrian

    while True:
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        # Membuat thread baru untuk menangani permintaan klien
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()