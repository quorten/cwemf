#! /usr/bin/env perl

use strict;
use warnings;
use CGI;
use File::Spec;
use File::Copy;

my $forum = "index";
my $furl;

my $q = CGI->new;
my $topic = $q->param("topic");
my $post_error = "";
print $q->header("text/html");

my $turl = $topic;
$turl =~ s/[[:space:]]+/-/g;
$turl = "\L$turl";

# Change to the correct directory and define the forum file name.

# This filesystem path computation code gets pretty chummy with the
# client and server configuration.
my $preref = $q->referer;
if ($preref eq "") {
    $post_error = "The forum system could not get the name of the forum to
post to.";
} else {
    $preref =~ s~^http(s)?:(/){0,2}makouskys.com~/home/www~;
    $preref =~ s|^/home/www/~([[:alnum:]]+)/|/home/\1/.www/|;
    (my $volume, my $directories, my $page) =
	File::Spec->splitpath($preref);
    $page = "index" if $page eq "";
    my $gotopath = File::Spec->catpath($volume, $directories);
    $furl = $directories;
    $furl =~ s|^/home/([[:alnum:]]+)/.www/|/home/www/~\1/|;
    $furl =~ s~^/home/www~http://makouskys.com~;
    chdir $gotopath;
}

if (!$post_error && system("co", "-q", "-l", $forum . ".html"))
{
    $post_error =
	"The forum system could not obtain a lock on the forum.
This error might have occurred because two or more people
tried to post at the same time.  Going back and trying again may resolve
this problem.  If that doesn't solve the problem, then you should contact
the website administrator.";
}

if (!$post_error && !move($forum . ".html", $forum . ".html.old"))
{
    $post_error =
	"The forum system could not prepare to post your new message: $!";
}

my $fold;
my $fnew;

if (!$post_error && !open($fold, "<", $forum . ".html.old"))
{
    $post_error =
	"The forum system could not read the old forum contents: $!";
}

if (!$post_error && !open($fnew, ">", $forum . ".html"))
{
    $post_error =
	"The forum system could not write the new forum contents: $!";
}

if (!$post_error)
{
    while (<$fold>)
    {
	my $entry = "<p><a href=\"".$turl."\">".$topic."</a></p>\n";
	if ($_ =~ /<!-- CWEMF SPECIAL INSERTION TAG -->/) {
	    print $fnew $entry, "\n";
	    print $fnew $_;
	} elsif ($_ =~ /<!-- CWEBLOG SPECIAL INSERTION TAG -->/) {
	    print $fnew $_, "\n";
	    print $fnew $entry;
	} else {
	    print $fnew $_;
	}
    }

    if (!close($fnew) || !close($fold))
    {
	$post_error = "Error when closing file on server: $!";
    }

    unlink $forum . ".html.old";
}

if (!$post_error &&
    system("ci", "-q", "-u", "-mhttpd automatic forum post",
	   $forum . ".html"))
{
    $post_error =
	"The forum system could not check in the new forum contents.";
}

# Create the new topic directory.
my $sprefix = "/home/www/cwemf";

if (!$post_error)
{
    mkdir $turl;
    chmod 0775, $turl;
    (symlink($sprefix . "/post-form.html", $turl . "/post-form.html") &&
     symlink($sprefix . "/img-upload-form.html",
	  $turl . "/img-upload-form.html")) ||
	  ($post_error = "Failed to copy files for new topic.");
    chmod 0444, $turl . "/index.html",
	$turl . "/index.html,v" if !$post_error;
}

my $fout;
if (!$post_error)
{
    chdir $turl;
    if (!open($fout, ">", "index.html")) {
	$post_error = "The forum system could not check in the new forum contents.";
    }
}

if (!$post_error)
{
    my $ttopic = $topic;
    $ttopic =~ s/&/&amp;/g;
    $ttopic =~ s/</&lt;/g;
    $ttopic =~ s/>/&gt;/g;
    print $fout
'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>' . $ttopic . '</title>
  <link rel="stylesheet" href="/cwemf/cwemf.css" />
</head>
<body>

<!-- CWEMF SPECIAL INSERTION TAG -->

<p><a href="post-form">Post a new message to this forum.</a></p>

</body>
</html>
';
    (close($fout) &&
     !system("ci", "-q", "-u", "-i", "-t-", "index.html") &&
     !system("rcs", "-q", "-awww-data,fmadmin", "index.html")) ||
     ($post_error = "The forum system could not check in the new forum contents.");
}

if ($post_error)
{
    print $q->start_html("Error posting on forum"),
	$q->h1("Error posting on forum"), "\n",
	$q->p($post_error), "\n",
	$q->p($q->a({href => $furl}, "Return to the forum page.")),
	$q->end_html;
    exit;
}

print $q->start_html(-title => "Successful topic creation",
    -head => $q->meta({-http_equiv => "refresh",
		       -content => "2;url=" . $furl})),
    $q->h1("Successful topic creation"), "\n",
    $q->p("Your new topic has been added."), "\n",
    $q->p($q->a({href => $furl}, "Return to the forum page.")),
    $q->end_html;

# https://developer.mozilla.org/en-US/docs/Web/JavaScript?redirectlocale=en-US&redirectslug=JavaScript
