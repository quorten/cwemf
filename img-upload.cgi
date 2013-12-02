#! /usr/bin/env perl

use strict;
use warnings;
use CGI;
use File::Spec;

my $post_error = "";
my $no_unlink = 1;

my $q = CGI->new;
my $filename = $q->param("filename");

print $q->header("text/html");

# Change to the correct directory.

# This filesystem path computation code gets pretty chummy with the
# client and server configuration.
my $preref = $q->referer;
if ($preref eq "") {
    $post_error = "The forum system could not get the name of the directory
on the server to upload to.";
} else {
    $preref =~ s~^http(s)?:(/){0,2}makouskys.com~/home/www~;
    $preref =~ s|^/home/www/~([[:alnum:]]+)/|/home/\1/.www/|;
    (my $volume, my $directories, my $page) =
	File::Spec->splitpath($preref);
    $page = "index" if $page eq "";
    my $gotopath = File::Spec->catpath($volume, $directories);
    chdir $gotopath;
}

if (!$post_error && -e $filename)
{
    $post_error = "A file of the upload image filename already exists.";
}
else
{
    $no_unlink = 0;
}

my $fout;

if (!$post_error && !open($fout, ">", $filename))
{
    $post_error = "Could not create upload image filename on server: $!";
}

my $lightweight_fh;
$lightweight_fh = $q->upload("image") if !$post_error;
if (!$post_error && !(defined $lightweight_fh))
{
    $post_error = "Could not upload the image data.";
}

if (!$post_error)
{
    my $io_handle = $lightweight_fh->handle;
    my $bytesread; my $buffer;
    while ($bytesread = $io_handle->read($buffer, 1024)) {
	print $fout $buffer;
    }
    if (!close($fout))
    {
	$post_error = "Error when closing file on server: $!";
    }
    close($lightweight_fh);
}

if (!$lightweight_fh && $q->cgi_error)
{
    print $q->header(-status => $q->cgi_error);
    unlink $filename if !$no_unlink;
    exit;
}

if ($post_error)
{
    print $q->start_html("Error posting on forum"),
	$q->h1("Error posting on forum"), "\n",
	$q->p($post_error), "\n",
	$q->end_html;
    unlink $filename if !$no_unlink;
    exit;
}

print $q->start_html("Successful image upload"),
    $q->h1("Successful image upload"), "\n",
    $q->p("Your image has been uploaded."), "\n",
    $q->end_html;
