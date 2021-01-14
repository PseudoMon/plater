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

def on_new_page(event, observer):
    print(f"Detecting new page at {event.src_path}")
    page = plater.Page(event.src_path, islocal=True)

    print("Attempting to create watcher...")
    page_handler = PatternMatchingEventHandler(patterns=[page.source_file])
    page_handler.on_modified = functools.partial(on_page_modified, page=page)

    observer.schedule(page_handler, 'contents')


def setup_observer(pages, indexes):
    observer = Observer()

    observed_files = []

    # Observe changes on each existing file
    for page in pages:
        print("Observing changes on", page.source_file)
        page_handler = PatternMatchingEventHandler(patterns=[page.source_file])
        page_handler.on_modified = functools.partial(on_page_modified, page=page)

        observer.schedule(page_handler, 'contents')

        observed_files.append(page.source_file)

    new_page_handler = PatternMatchingEventHandler(
        patterns=[f"{ settings.contentdir }/**/*{ settings.contentext }"],
        ignore_patterns=observed_files)

    new_page_handler.on_modified = functools.partial(on_new_page, observer)


    return observer

