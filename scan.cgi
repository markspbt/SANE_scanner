#!/usr/local/bin/perl
use strict;
our %in=();
eval {require '/home/fscan/cgi-bin/cgi-lib.pl'};
unless($@) {&ReadParse;}

my %pgs = (1,'Left Page',2,'Right Page');
my %pgnmb = (1,'L',2,'R');
my %scanners = (
1,'pixma:04A98913_4167B2',
2,'pixma:04A91234_48KKJ1'
);
my %colorsby = (
'gray','Gray',
'color','Color'
);

unless($colorsby{$in{c}}) {print "Content-type: text/html\n\n$pgs{$in{s}}<br />\nNot Scanned<br /><img src=\"scanner.open.png\">";	exit(0);}
my $imn = time;
my $rotate='';
if($pgnmb{$in{s}} eq 'R') {$rotate = ' -rotate 180';}

`scanimage --mode $colorsby{$in{c}} --device-name=$scanners{$in{s}} --resolution 300 --format=tiff > /home/fscan/scans/$imn.$pgnmb{$in{s}}.tif`;

my $printImage='';
if(-f "/home/fscan/scans/$imn.$pgnmb{$in{s}}.tif") {
`convert -density 72 /home/fscan/scans/$imn.$pgnmb{$in{s}}.tif -resize x300$rotate /home/fscan/http/images/$imn.$pgnmb{$in{s}}.jpg`;
`convert -density 72 /home/fscan/scans/$imn.$pgnmb{$in{s}}.tif -resize x1400$rotate /home/fscan/http/images/$imn.$pgnmb{$in{s}}.b.jpg`;
$printImage = "<img src=\"/images/$imn.$pgnmb{$in{s}}.jpg\" alt=\"$pgs{$in{s}}\" onclick=\"showimage('/images/$imn.$pgnmb{$in{s}}.b.jpg');return false;\">\n";
} ## END FILE PRESENT

print "Content-type: text/html\n\n$pgs{$in{s}}<br />\n$printImage";

exit(0);
