import plater
import argparse 
import livereload

parser = argparse.ArgumentParser(
    description="Generate a document with Plater")

parser.add_argument("-l", "--live", action='store_true', help="Enable live reload")

args = parser.parse_args()

if args.live:
    pages, indexes = plater.init_plater(islocal=True)

    observer = livereload.setup_observer(pages, indexes)

    observer.start()

    try:
        livereload.run_server()
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()

else:
    plater.init_plater()
