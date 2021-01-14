import settings
import plater

import http.server
import socketserver
import functools
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

def run_server():
    PORT = settings.localport
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=settings.outdir)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port ", PORT)
        httpd.serve_forever()

def on_content_changes(event):
    print(f"Detecting changes at {event.src_path}")
    print("Rebuilding...")
    plater.init_plater(islocal=True)

def setup_observer(pages, indexes):
    observer = Observer()

    print("Observing any changes to content...")
    content_handler = PatternMatchingEventHandler(
        patterns=[f"{ settings.contentdir }/*{ settings.contentext }"])
    content_handler.on_any_event = on_content_changes

    observer.schedule(content_handler, 'contents')

    return observer

