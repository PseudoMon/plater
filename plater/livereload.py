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

def on_page_modified(event, page):
    print(f"Detecting changes on {event.src_path}")
    page.recreate_file()


def setup_observer(pages, indexes):
    observer = Observer()

    for page in pages:
        print("OBSERVING", page.source_file)
        page_handler = PatternMatchingEventHandler(patterns=[page.source_file])
        page_handler.on_modified = functools.partial(on_page_modified, page=page)

        observer.schedule(page_handler, 'contents')

    return observer

