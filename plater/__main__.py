import plater
import argparse 
import livereload

parser = argparse.ArgumentParser(
    description="Generate a document with Plater")

parser.add_argument("-live", action='store_true', help="Enable live reload")

args = parser.parse_args()

pages, indexes = plater.init_plater()

if args.live == True:
    livereload.run_server()