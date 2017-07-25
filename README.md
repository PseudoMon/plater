# Plater #
Plater is a simple static site generator made in Python. It's specifically made to be highly customizable with few default configurations. In essence, it takes a bunch of text files, parse them through Markdown, optionally sort them by type, then create a page out of it using Jinja2. 

I made Plater because I'm just looking for a simple way to make static sites with Jinja2's extensible layouting. To create custom static websites using Plater you'll need some knowledge of web-designing and [Jinja2](http://jinja.pocoo.org).

## Setting up
To run Plater you'll need Python 3. Plater requires Markdown and Jinja2. 

Copy or clone this repository to wherever directory you want to work in. Put `__main__.py` and `settings.py` in a folder title `plater`.

Edit `settings.py` as you like. For more details see the sections below.

Create a folder for your templates and another folder for your site contents. You can name them whatever as long as it's consistent with the names in `settings.py`. By the end you should have three different folders in your working directory: templates, contents, and plater.

In that directory, run `python plater` and your website will be generated, assuming the templates and contents are there.

## Content and Metadata
Plater will look at your content folder and create a page out of every markdown file in there, unless noted otherwise (see below sections). The file can have some metadata written at its top like this:"
```
title: Title of the page
type: blog
---
```
Metadata will then be processed by either Plater or your Jinja2 templates. Metadata must be separated with the main content with three dashes (`---`). 

You can make any metadata you like according to your needs. These metadatas are used by Plater:

- 'type' define what kind of content it is, which will be used when deciding the page's template, whether it will be indexed, and whether the page will be generated at all.

- 'slug' will be used for the filename of the generated page. Don't include extensions. Slug will be used as-is, so please make sure it can be used as a clean URL (see below section) 

-  'subdir', if provided and is anything but 'home' or 'none', will cause the page to be generated in a subdirectory. Multiple subdirectories is not yet supported. (Example: `subdir: fiction` will create the directory fiction  in your output directory if it doesn't already exist, and put the generated file in there)

- 'title' will be used to generated a filename if 'slug' is not provided

- 'date' will be used to sort your content in indexes (latest date at the top, assuming you use ISO date). If not provided, your content will have a default date of 0.
 
## Permalink and Filename
URL to the pages in your site may varies depending on where you host your website. To prevents redirection problems and whathaveyous, you should put in the absolute address to your hosted website in the settings file. 
Plater assumes that the filename of a page will be used as its URL, so it'll attempt to keep it clean (no capital letters, no spaces, only English alphanumeric characters). If provided, Plater will use the name provided in the 'slug' metadata. Afterwards, it will try to clean the 'title' metadata. If neither are provided, it'll clean and use the content's filename (minus extension).


## Choosing Templates
You can have different templates depending on what 'type' you give your content. Just list what template that type of content will use in `templates` in the settings file. Plater will look for the template in the template folder. If no specific template is mentioned, it'll use the one listed as default. For stability reasons, please don't remove the default template.

For instance, if you have contents with the type "post" and "photo album" and the templates in your settings file look like this:
```
templates = {
    'home': 'index.html',
    'default': 'single.html',
    'photo album': 'album.html',
    'blog_index': archive.html' }
```
Plater will look in your template folder for `single.html` and use it forcontents with the type "post", and it'll look for 'album.html' and use it for contents with the type "photo album".

"home" is a special template used for your homepage. Those that ends in "_index" are used for index pages (see below). 

## Indexes
To create an index of your pages (like an archive page, etc) add to `indexes` in the settings file. 

For example if the variable "indexes" in your settings file look like this:
```
indexes = {'home': 'index', 'blog': 'archive'}
```
Then it will create an index of your pages that are labeled as "blog", using the template set as "blog_index" in the templates list. The resulting file will be named "archive.html". Any page in your site whose type isn't set as "blog" will not be indexed.

Note that if you don't have the index template set in the variable "templates", Plater will thrown an error.

## Dontpost and Drafts
You can create a content file that won't be generated as a page (you might want that such as when creating a draft, or if you only need its metadata). There are two ways to go about it. You can either add a 'draft' metadata to the content (it doesn't matter what you fill into it), or you can put the name of content's type in the variable "dontpost" in the settings file. 

## Static Files
Plater doesn't do anything to your output folder other than generating its pages. If you want to add static files, such as stylesheets, Javascripts, images, etc, you can simply add them to the output foldedr. 

## Future Features
- Sort by something other than date
- Turn this into a proper PyPi package?
 



