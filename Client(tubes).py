import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('192.168.56.1', 8000)

print(f'Connecting to server {server_address[0]} port {server_address[1]}')


client_socket.connect(server_address)

try: 
    try:
        
        request = 'GET /helloworld_tubes.html HTTP/1.1\r\nHost: localhost\r\n\r\n'
        client_socket.sendall(request.encode())

        
        response = b''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        
        print(f'Response from server:\n{response.decode()}')

    finally:
        # Menutup koneksi
        client_socket.close()


except socket.error as e:
    print(f'Error: {e}')
except Exception as e:
    print(f'An unexpected error occurred: {e}')