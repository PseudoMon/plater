import settings
from jinja2 import Environment, FileSystemLoader
from jinja2 import exceptions as jinjaerror
import markdown
import glob
import os

if not os.path.exists(settings.outdir):
    os.makedirs(settings.outdir)

env = Environment(loader=FileSystemLoader(settings.templatedir))
md = markdown.Markdown(extensions=
    ['markdown.extensions.nl2br', 'markdown.extensions.smarty', 'markdown.extensions.meta'])

def createPage(post):
    """Create a page from a processed post and a template"""
    try:
        platefile = settings.templates[post['type']]
    except KeyError:
        platefile = settings.templates['default']

    try:
        template = env.get_template(platefile)
    except jinjaerror.TemplateNotFound:
        print("Template file", platefile, "not found.")
        exit()

    output = template.render(siteurl=settings.siteurl, post=post)

    if 'subdir' in post:
        if post['subdir'] != ('home' or 'none'):
            dir = "{}/{}".format(settings.outdir, post['subdir'])
            if not os.path.exists(dir):
                os.makedirs(dir)
            dir = dir + "/"

        else:
            dir = "{}/".format(settings.outdir)
    else:
        dir = "{}/".format(settings.outdir)

    filename = "{}{}.html".format(dir, post['slug'])
    with open(filename, 'w') as fout:
        fout.write(output)

    print("Created", post['slug'])

def createIndex(type, posts):
    """Create a single index page."""
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

    output = template.render(siteurl=settings.siteurl, posts=posts)

    filename = "{}/{}.html".format(
        settings.outdir, settings.indexes[type])
    with open(filename, 'w') as fout:
        fout.write(output)

    print("Created", settings.indexes[type])


def processFile(filename):
    """Process a filename to a templateable post"""
    print(filename)
    file = open(filename, "r")
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
        meta['slug'] = "-".join(meta['title'].lower().split())
    else:
        filename = filename.split('.')[0]
        meta['slug'] = "-".join(
            filename.lower().split())

    if 'date' not in meta:
        meta['date'] = "0"

    post = meta
    post['content'] = content
    return post


def indexPosts(posts):
    """Sort (processed) posts and create index pages."""
    indexed = {}
    for post in posts:
        try:
            indexed[post['type']].append(post)
        except KeyError:
            print("Found type:", post['type'])
            indexed[post['type']] = [post]

    # Sort all the posts
    for type in indexed:
        indexed[type] = sorted(indexed[type], key=lambda k: k['date'], reverse=True)
        if type in settings.indexes:
            createIndex(type, indexed[type])

    if 'home' in settings.indexes:
            createIndex('home', indexed)


posts = []
print("Searching {}/*{}".format(
    settings.contentdir, settings.contentext))
contentfiles = glob.glob('{}/**/*{}'.format(
    settings.contentdir, settings.contentext), recursive=True)

print("Processing files:")
for filename in contentfiles:
    post = processFile(filename)

    if not ('draft' in post or post['type'] in settings.dontpost):
        createPage(post)

    posts.append(post)

print("Sorting posts and creating indexes...")
indexPosts(posts)

print("Done!")
