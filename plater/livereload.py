import settings

import http.server
import socketserver
import functools
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

def run_server():
    PORT = 8000
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=settings.outdir)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port ", PORT)
        httpd.serve_forever()


def livereload(pages, indexes):
    pass