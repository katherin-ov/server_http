import argparse
import datetime
import logging
import os
import socket
import urllib.parse
from concurrent.futures import ThreadPoolExecutor


logger = logging.getLogger(__name__)
DOCUMENT_ROOT = "./documents"


def get_content_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.swf': 'application/x-shockwave-flash'
    }
    return types.get(ext, 'application/octet-stream')


def handle_client(workers_pool, client_socket, root) -> None:
    workers_pool.submit(handle_request, client_socket, root)


def is_safe_path(requested_path, root):
    full_path = os.path.join(root, requested_path.lstrip('/'))
    real_path = os.path.realpath(full_path)
    return real_path.startswith(os.path.realpath(root))


def handle_request(client_socket, root):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return

        headers = request.split('\n')
        method, path, _ = headers[0].split()

        if method not in ['GET', 'HEAD']:
            response = 'HTTP/1.1 405 Method Not Allowed\n\nMethod Not Allowed'
            client_socket.sendall(response.encode('utf-8'))
            return

        path = urllib.parse.unquote(path)

        if '?' in path:
            path = path.split('?')[0]

        # Удаление начального символа '/'
        if path == '/':
            path = '/index.html'
        elif path.endswith('/'):
            path = path + 'index.html'

        file_path = root + path
        safe_path = is_safe_path(file_path, root)

        if safe_path and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                body = file.read()

            now = datetime.datetime.now(datetime.UTC)
            date_header = now.strftime('%a, %d %b %Y %H:%M:%S') + ' GMT'
            file_type = get_content_type(file_path)

            response_headers = 'HTTP/1.1 200 OK\r\n'
            response_headers += f'Content-Length: {len(body)}\r\n'
            response_headers += f'Content-Type: {file_type}\r\n'
            response_headers += 'Server: HTTPServer\r\n'
            response_headers += f'Date: {date_header}\r\n'
            response_headers += 'Connection: close\r\n\r\n'
            response = response_headers.encode('utf-8')

            if method == 'GET':
                response += body
        elif not safe_path:
            response = 'HTTP/1.1 403 Forbidden\r\nServer: HTTPServer\r\nConnection: close\r\n\r\n403 Forbidden'
            response = response.encode('utf-8')
        else:
            response = 'HTTP/1.1 404 Not Found\r\nServer: HTTPServer\r\nConnection: close\r\n\r\n404 Not Found'
            response = response.encode('utf-8')

        client_socket.sendall(response)
    finally:
        client_socket.close()


def start_server(root: str, workers: int) -> None:
    """Сервер, который реализует протокол HTTP"""
    listening_socket = socket.create_server(
        ("127.0.0.1", 8080),
        family=socket.AF_INET,
        backlog=1024,
        reuse_port=True,
    )
    workers_pool = ThreadPoolExecutor(max_workers=workers)
    try:
        while True:
            client_socket, _ = listening_socket.accept()
            handle_client(workers_pool=workers_pool, client_socket=client_socket, root=root)
    finally:
        listening_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='./documents')
    parser.add_argument('-w', '--workers', type=int, default=2)
    args = parser.parse_args()
    start_server(args.root, args.workers)
