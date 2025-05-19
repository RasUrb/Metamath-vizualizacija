import http.server
import socketserver
import webbrowser
import threading
import os

PORT = 8000
DIR = os.path.dirname(os.path.abspath(__file__))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serveris paleistas http://localhost:{PORT}")
        httpd.serve_forever()

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}/index.html")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    start_server()
