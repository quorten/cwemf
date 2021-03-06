Cwemf README
============

This is cwemf (the Coolest Website Ever Message Forum), a simple and
lightweight CGI forum system.  It is useful in special-case scenarios
in private intranets where minimalism is preferred and authentication
within in the forum software is unnecessary.

Installation
============

Before installing cwemf, you'll need to verify that you have its
dependencies installed first.  Cwemf depends on the following
software: Perl, CGI.pm, RCS, TinyMCE.  (And a web server, of course.)
Note that cwemf has only been tested on Trisquel GNU/Linux 10.04 LTS,
so it might not work on non-Unix operating systems without tiny
modifications.

Next, you need to configure your web server.  Cwemf should be
installed such that its entire contents are accessible from "/cwemf",
including the CGI scripts.  You must also have your server setup to
perform content negotiation on the CGI scripts in cwemf.  "Topic
forums" (see below) will also require special configuration for XHTML
headers on automatic index generation.  Here's an example
configuration for Apache 2:

```
	Alias /cwemf/ /usr/local/share/cwemf/
	<Directory /usr/local/share/cwemf/>
		Options Indexes MultiViews FollowSymLinks ExecCGI
		AllowOverride None
		IndexIgnore HEADER.html
		IndexOptions +SuppressHTMLPreamble +XHTML
		AddHandler cgi-script .cgi
		MultiviewsMatch Handlers
		Order allow,deny
		Allow from all
	</Directory>
```

You should also verify that the directory cwemf is installed in cannot
be modified by the web server.

To test if the cwemf installation is working, you should try setting
up simple forums by following the instructions below.

Using Cwemf
===========

There are two main modes of using cwemf:

1. Single-page forum mode
2. Topic forum mode

Single-page forum mode only has one web page where the content can be
edited.  Topic forum mode basically adds a topic page that links to
several single-page forums.

Here's how to setup a new single-page forum:

    mkdir new-forum # Create a new directory visible from a browser.
    cd new-forum
    chgrp www-data .
    chmod g+w .
    # In some cases, you might need to copy or hardlink for the
    # following two commands instead of symlink.
    ln -s /usr/local/share/cwemf/post-form.html .
    ln -s /usr/local/share/cwemf/img-upload-form.html .
    cp /usr/local/share/cwemf/schema.html index.html
    vi index.html # Edit the schema to your preferences.
    ci -u -i -t-'New forum for testing' index.html
    # Restrict access to httpd and a forum administrator.
    rcs -awww-data,fmadmin index.html

If you installed cwemf correctly, you should be able visit the new
forum and add a "first post!" entry to the forum.  Note that if you
want a blank line to follow your entry, you need to type two blank
lines in TinyMCE.  All of this simplicity of implementation behavior
is intentional in the design of cwemf, even though it forces the forum
poster to add more information manually.

Once you've got the single-page form mode tested and working, you can
move on to testing topic forum mode:

    mkdir topic-forum # Create a new directory visible from a browser.
    cd topic-forum
    chgrp www-data .
    chmod g+w .
    cp /usr/local/share/cwemf/tocHEADER.html HEADER.html
    vi HEADER.html # Edit the schema to your preferences.

You'll notice that when you create new topic forums, there is no title
heading printed within the web page.  If you want such a heading in
your post, you can post that in manually, otherwise, you can leave it
out if you don't want such a heading.

Using cwemf is that simple.  Its source code is also correspondingly
simple.

Copying Conditions
==================

All files in cwemf are in Public Domain.

See the file "UNLICENSE" in the top level directory for details.
