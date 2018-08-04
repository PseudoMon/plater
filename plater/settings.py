siteurl = 'something.com' #the site's base url
templatedir = 'templates' # the name of your template dir
contentdir = 'contents' # the name of your content dir
contentext = '.md' #file extension of content
outdir = 'output' # where Plater will put the result

dontpost = ['dataonly']

# Template files used for generating specific pages
# type of post: name of template file in templates folder
templates = {
    'home': 'index.html',
    'default': 'single.html' }

# Used for creating index files
# type of posts: the index's filename
indexes = {'home': 'index'}