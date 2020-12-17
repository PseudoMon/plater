import settings
from jinja2 import Environment, FileSystemLoader
from jinja2 import exceptions as jinjaerror
import markdown
import glob
import re
import os

if not os.path.exists(settings.outdir):
    os.makedirs(settings.outdir)

env = Environment(loader=FileSystemLoader(settings.templatedir))
md = markdown.Markdown(extensions=
    ['markdown.extensions.nl2br', 'markdown.extensions.smarty', 'markdown.extensions.meta'])

class Page:
    """A single page, generated from a single content file"""
    def __init__(self, filename, local=False):
        # filename is the path to the content file
        self.source_file = filename
        self.postdata = self.process_file(filename)

        self.type = self.postdata['type']

        if local:
            self.siteurl = settings.localurl
        else:
            self.siteurl = settings.siteurl


        if 'draft' in self.postdata or self.type in settings.dontpost:
            self.dontpost = True 
        else:
            self.dontpost = False

        if not self.dontpost:
            self.result_file = self.create_page(self.postdata, self.siteurl)


    def process_file(self, filename):
        """Process a filename to a templateable post"""
        print(filename)

        with open(filename, 'r') as file:
            content = md.convert(file.read())
        
        meta = md.Meta

        for data in meta:
            if len(meta[data]) == 1:
                meta[data] = meta[data][0]

        if 'type' not in meta:
            meta['type'] = "none"

        if 'slug' in meta:
            pass
        elif 'title' in meta:
            # Create valid output file name from title
            meta['slug'] = re.sub(r'[^\w\d\s\-\_]', '', meta['title'])
            meta['slug'] = re.sub(r'\s', '-', meta['slug']).lower()
        else:
            # Create output file name from file name
            filename = filename.split('.')[0]
            meta['slug'] = re.sub(r'\s', '-', filename).lower()

        if 'date' not in meta:
            meta['date'] = "0"

        post = meta
        post['content'] = content
        
        return post


    def create_page(self, postdata, siteurl=settings.siteurl):
        """Create a page from a processed post and a template.
        Returns path of the created file"""
        try:
            platefile = settings.templates[postdata['type']]
        except KeyError:
            platefile = settings.templates['default']

        try:
            template = env.get_template(platefile)
        except jinjaerror.TemplateNotFound:
            print("Template file", platefile, "not found.")
            exit()


        if 'subdir' in postdata:
            if postdata['subdir'] != ('home' or 'none'):
                dir = f"{ settings.outdir }/{ postdata['subdir'] }"
                
                if not os.path.exists(dir):
                    os.makedirs(dir)
                
                dir = dir + "/"

            else:
                dir = f"{ settings.outdir }/"

        else:
            dir = f"{ settings.outdir }/"

        filename = f"{ dir }{ postdata['slug'] }.html"
        
        template.stream(siteurl=siteurl, post=postdata).dump(filename)

        print("Created", postdata['slug'])

        return filename


    def recreate_file(self):
        #TODO
        print("WE SHOULD BE RECREATING THE FILE HERE")
        pass

class Index: 
    """An index page, containing pages of the same type"""
    def __init__(self, type, pages, local=False):
        # pages should be a list of Page objects
        self.type = type
        try:
            self.indexname = settings.indexes[self.type]
        except KeyError:
            print("Index name for type", self.type, "is not found!")
            exit()

        self.pages = pages

        if local:
            self.siteurl = settings.localurl
        else:
            self.siteurl = settings.siteurl

        self.postsdata = self.get_postsdata(pages)
        self.result_file = self.create_index(self.type, self.indexname, self.postsdata, self.siteurl)

        
    def get_postsdata(self, pages):
        postsdata = []
        for page in pages:
            postsdata.append(page.postdata)
        return postsdata 

    def create_index(self, type, indexname, postsdata, siteurl=settings.siteurl):
        """Create index page from template."""
        if type == 'home':
            platefile = settings.templates['home']
        else:
            try:
                platefile = settings.templates[type + "_index"]
            except KeyError:
                print("Template for", type + "_index", "not found!")
                print("Please provide it in settings.py")
                exit()

        try:
            template = env.get_template(platefile)
        except jinjaerror.TemplateNotFound:
            print("Template file", platefile, "not found.")
            exit()

        try:
            filename = settings.indexes[type]
        except KeyError:
            print("Index name for type",type,"is not found!")
            exit()

        filename = f"{settings.outdir}/{settings.indexes[type]}.html"

        template.stream(siteurl=self.siteurl, posts=postsdata).dump(filename)

        print("Created", settings.indexes[type])

        return filename


def index_pages(pages, islocal=False):
    """Sort (processed) pages and create index pages."""
    indexed = {}
    allpages = []

    indexes = []

    for page in pages:
        try:
            indexed[page.type].append(page)
        except KeyError:
            print("Found type:", page.type)
            indexed[page.type] = [page]
        finally:
            allpages.append(page)

    # Sort all the pages
    for pagetype in indexed:
        pages = sorted(indexed[pagetype], key=lambda p: p.postdata['date'], reverse=True)
        
        if pagetype in settings.indexes:
            print("Creating index for type", pagetype)
            indexes.append(Index(pagetype, pages, islocal))

    if 'home' in settings.indexes:
        indexes.append(Index('home', allpages, islocal))

    return indexes


def create_pages(islocal=False):
    print(f"{ settings.contentdir }/**/*{ settings.contentext }")

    files = glob.glob(f"{ settings.contentdir }/**/*{ settings.contentext }", recursive=True)

    pages = []
    for file in files:
        pages.append(Page(file, islocal))

    return pages

def init_plater(islocal=False):
    print("Creating pages from files...")
    pages = create_pages(islocal)

    print("Sorting pages and creating indexes...")
    indexes = index_pages(pages, islocal)

    print("Site generated!")

    return pages, indexes

if __name__ == "__main__":
    init_plater()

