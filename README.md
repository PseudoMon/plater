# Plater #
Plater is a simple static site generator made in Python. It's specifically made to be highly customizable with few default configurations. In essence, it takes a bunch of text files, parse them through Markdown, optionally sort them by type, then create a page out of it using Jinja2.

I made Plater because I'm just looking for a simple way to make static sites with Jinja2's extensible layouting. To create custom static websites using Plater you'll need some knowledge of web-designing and [Jinja2](http://jinja.pocoo.org).

## Setting up
To run Plater you'll need Python 3. Plater requires Markdown and Jinja2.

Copy or clone this repository to wherever directory you want to work in. This repo already contains example template and contents, but you can remove those if you like.

The files `__main__.py` and `settings.py` should be in a directory named `plater`.

Edit `settings.py` as you like. For more details see the sections below.

When you start Plater, you should have at least three different directories in your main directory: templates, contents, and plater. Output directory will be made if it doesn't already exist.

In the main directory, run `python plater` and your website will be generated, assuming the templates and contents are there.

## Content and Metadata
Plater will look at your content directory and create a page out of every markdown file in there, unless noted otherwise (see below sections). The file can have some metadata written at its top like this:
```
title: Title of the page
type: blog
---
```
Metadata will then be processed by either Plater or your Jinja2 templates. Metadata must be separated with the main content with three dashes (`---`).

You can make as many or as few metadata you like according to your needs. Every metadata will be sent to the Jinja template, which you can then use as you will.

These metadatas are used by Plater:

- `type` define what kind of content it is, which will be used when deciding the page's template, whether it will be indexed, and whether the page will be generated at all.

- `slug` will be used for the filename of the generated page. Don't include extensions. Slug will be used as-is, so please make sure it can be used as a clean URL (see below section)

- `subdir`, if provided and is anything but 'home' or 'none', will cause the page to be generated in a subdirectory. Multiple subdirectories is not yet supported. (Example: `subdir: fiction` will create the directory fiction in your output directory if it doesn't already exist, and put the generated file in there)

- `title` will be used to generated a filename if `slug` is not provided

- `date` will be used to sort your content in indexes (latest date at the top, assuming you use ISO date). If not provided, your content will have a default date of 0.

- `content` **may not** be used as a metadata, as Plater will use this key to contain the, well, the content of the post.

All the above metadatas are optional.

## Permalink and Filename
URL to the pages in your site may varies depending on where you host your website. To prevents redirection problems and whathaveyous, you should put in the absolute address to your hosted website in the `siteurl` variable in the settings file.

Plater assumes that the output filename will be used as its URL when it's live, so it'll attempt to keep it clean (no capital letters, no spaces, only English alphanumeric characters).

If provided, Plater will use the name provided in the 'slug' metadata. Afterwards, it will try to clean the 'title' metadata. If neither are provided, it'll clean and use the content's filename (minus extension).

## Choosing Templates
You can have different templates depending on the `type` you give to a content. Just modify the variable `templates` in the settings file according to your needs. If no specific template is mentioned, it'll use the one listed as default. For stability reasons, please don't remove the default template.

For instance, if you have contents with the type "post", contents with the type "photo album", and the templates in your settings file look like this:
```
templates = {
    'home': 'index.html',
    'default': 'single.html',
    'photo album': 'album.html',
    'blog_index': archive.html' }
```
When generating a content with the type "photo album", Plater will look in your template directory for `album.html` and use that. When it's generating a content with type "post", it will use the default `single.html` as there isn't a specific template for that type.

"home" is a special template used for your homepage. Those that ends in `_index` are used for index pages (see below).

## Indexes
To create an index of your content pages (like an archive page, etc) add to the `indexes` variable in the settings file.

For example, if the variable "indexes" in your settings file look like this:
```
indexes = {'home': 'index', 'blog': 'archive'}
```
Then it will look at the template named `blog_index` in the `templates` variable, and use that to create an index of pages that are labeled as "blog". The resulting file will be named `archive.html`.

As no other index is mentioned, Plater will not generate an index page for any other pages whose type isn't set as "blog". However, the "home" index will always receive every pages handed to it. See below section.  

## Homepage
By default, Plater will always generate a home index, using the template marked as `home` in the `templates` variable and the filename marked as `home` in the `indexes` variable. Home index will always receive the variable `posts` that contains every pages generated by Plater, but you don't have to use all of them (or at all).

This is useful, for instance, when you want to have specific index pages for specific types but also a single place that link to all your pages. Or if you want to make your homepage only show the latest couple of pages and everything else is indexed elsewhere. It will all depend on your templates.   

You can also make a custom homepage by either not using the `posts` variable at all in your home index template, or by making a normal content page that's set to have the filename `index.html`. In this case, please don't set the type as "home", for stability sake.   

## Templating
Please read the [Jinja2](http://jinja.pocoo.org/docs) documentation for more details. Plater will hands the following arguments to the template when it's generating a page:

- `siteurl`, which is the site's base URL as set in the settings file. Use it for every link.

- Per-content pages are given `post` which contains the post.

- Per-type index will receive `posts` that contains a list filled with posts of that type.

- Home index will receive `posts` that contains a dict. Each key of this dict is the name of a type, and its value is a list of that type's posts.

Content of a post can be accessed by using `post['content']`. Metadatas can be accessed the same way (`post['title']`, `post['date']`, etc)

## Dontpost and Drafts
It's possible to create a content file without later generating a page out of it (you might want that such as when creating a draft, or if you only need to use its metadata). There are two ways to go about it. You can either add a `draft` metadata to the content (it doesn't matter what you fill it with), or you can put the content's type in the variable `dontpost` in the settings file.

Please note that these pages will still be available in the `posts` variable when generating indexes. If you don't want your index page to contain these posts, simply don't include them in your template.

## Static Files
Plater doesn't do anything to your output directory other than inserting the pages it generated. If you want to add static files, such as stylesheets, Javascripts, images, etc, you can simply add them to the output directory. Plater also doesn't remove any files from the output directory, so if there's any unused files, you'll have to remove them yourself.

## Local Testing
For local testing, I suggest setting `siteurl` to `http://localhost:[port]`. And then when you're trying to test the site, make a local server by running `python -m http.server [port]`. The default port is `8000`. Just remember to change `siteurl` back and regenerating when you're ready to upload to the real server.    

## Future Features
- Sort by something other than date
- Turn this into a proper PyPi package?
