import socket
import os
import shutil

DIR = os.path.join(os.getcwd(), 'server')
if not os.path.exists(DIR):
    os.makedirs(DIR)


def handle_request(request):
    try:
        parts = request.split(' ')
        command = parts[0]

        if command == 'pwd':
            return DIR

        elif command == 'ls':
            return '; '.join(os.listdir(DIR))

        elif command == 'mkdir':
            if len(parts) < 2:
                return 'Error: Directory name not specified'
            dirname = os.path.join(DIR, parts[1])
            os.makedirs(dirname, exist_ok=True)
            return f'Directory {parts[1]} created'

        elif command == 'rmdir':
            if len(parts) < 2:
                return 'Error: Directory name not specified'
            dirname = os.path.join(DIR, parts[1])
            if os.path.exists(dirname) and os.path.isdir(dirname):
                shutil.rmtree(dirname)
                return f'Directory {parts[1]} removed'
            return 'Error: Directory not found'

        elif command == 'rm':
            if len(parts) < 2:
                return 'Error: File name not specified'
            filename = os.path.join(DIR, parts[1])
            if os.path.exists(filename) and os.path.isfile(filename):
                os.remove(filename)
                return f'File {parts[1]} removed'
            return 'Error: File not found'

        elif command == 'rename':
            if len(parts) < 3:
                return 'Error: Usage rename <old_name> <new_name>'
            old_name = os.path.join(DIR, parts[1])
            new_name = os.path.join(DIR, parts[2])
            if os.path.exists(old_name):
                os.rename(old_name, new_name)
                return f'File renamed from {parts[1]} to {parts[2]}'
            return 'Error: File not found'

        elif command == 'upload':
            if len(parts) < 3:
                return 'Error: Usage upload <filename> <content>'
            filename = os.path.join(DIR, parts[1])
            content = ' '.join(parts[2:])
            with open(filename, 'w') as f:
                f.write(content)
            return f'File {parts[1]} uploaded'

        elif command == 'download':
            if len(parts) < 2:
                return 'Error: File name not specified'
            filename = os.path.join(DIR, parts[1])
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, 'r') as f:
                    return f.read()
            return 'Error: File not found'

        elif command == 'q':
            return 'Quitting'

        else:
            return 'Error: Unknown command'

    except Exception as e:
        return f'Error: {str(e)}'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

print("Server is running.")
print(f"Working directory: {DIR}")

while True:
    conn, addr = sock.accept()
    print(f"Connection: {addr}")

    request = conn.recv(1024).decode()
    print(f"Request: {request}")

    response = handle_request(request)
    conn.send(response.encode())

    if request == 'q':
        break

conn.close()
