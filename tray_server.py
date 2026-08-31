import os
import sys
import webbrowser
import threading
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pystray
from PIL import Image

# 配置
ROOT = Path("D:/htmltool2")
PORT = 8765
AUTO_OPEN = "--no-open" not in sys.argv


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass


def start_server():
    os.chdir(ROOT)
    server = HTTPServer(("0.0.0.0", PORT), SilentHandler)
    server.serve_forever()


def open_url():
    webbrowser.open("http://127.0.0.1:8765/index.html")


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def restart(icon, item):
    python = sys.executable
    os.execl(python, python, *sys.argv)


def exit_app(icon, item):
    icon.stop()
    os._exit(0)


def main():
    if is_port_in_use(PORT):
        if AUTO_OPEN:
            open_url()
        return

    threading.Thread(target=start_server, daemon=True).start()
    image = Image.open(ROOT / "icon.png")
    icon = pystray.Icon(
        "htmltool2",
        image,
        "htmltool2 HTML 编辑器 (http://127.0.0.1:8765)",
        menu=pystray.Menu(
            pystray.MenuItem("打开 htmltool2", lambda icon, item: open_url()),
            pystray.MenuItem("重新启动", restart),
            pystray.MenuItem("退出", exit_app),
        ),
    )
    if AUTO_OPEN:
        open_url()
    icon.run()


if __name__ == "__main__":
    main()
