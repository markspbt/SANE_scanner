# FreeBSD SANE scanner
FreeBSD running two SANE scanners at the same time to control two CanoScan LiDE 300 scanners at the same time.

After OS installation ports collection is installed with:
```bash
eportsnap fetch
portsnap extract # for the first time installation
or
portsnap fetch update
```

Install portsmaster to make life easier:
```bash
# cd /usr/ports/ports-mgmt/portmaster && make install clean
```

Next install Perl (yes, it is our weapon of choice)
```bash
portmaster -d lang/perl5.30 && make install clean
```

Now install Apache Web server (NGINX would work as well):
```bash
portmaster -d www/apache24 && make install clean
```

For image manipulation ImageMagick (convert) is installed:
```bash
portmaster -d graphics/ImageMagick7-nox11 && make install clean
```

since X11 Windows not used - anything related to it not installed.

and now SANE backends:
```bash
portmaster -d graphics/sane-backends && make install clean
```

Next, making sure we can use scanners from Apache. For this we need proper user/group/permissions.

This example creates a group called usb:
```bash
# pw groupadd usb
```

Then, make the /dev/ugen0.2 symlink and the /dev/usb/0.2.0 device node accessible to the usb group with write permissions of 0660 or 0664 by adding the following lines to /etc/devfs.rules:
```bash
[system=5]
add path ugen0.2 mode 0660 group usb
add path usb/0.2.0 mode 0666 group usb
```

Note: It happens the device node changes with the addition or removal of devices, so one may want to give access to all USB devices using this ruleset instead:
```bash
[system=5]
add path 'ugen*' mode 0660 group usb
add path 'usb/*' mode 0666 group usb
```

Refer to devfs.rules(5) for more information about this file.

Next, enable the ruleset in /etc/rc.conf:
```bash
devfs_system_ruleset="system"
```

And, restart the devfs(8) system:
```bash
# service devfs restart
```

Finally, add the users to usb in order to allow access to the scanner:
```bash
# pw groupmod usb -m webserver
```

instead of user "webserver" use the one set in Apache config file.

When SANE permissions are properly set and scanners working from Terminal a simple Web interface can be set to scan.

This is a web page:
```html
<!DOCTYPE html>
<html dir="ltr" lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Scanning</title>
<link href="/css/fonts.exo.css" rel="stylesheet">
<link href="/css/fonts.exo2.css" rel="stylesheet">
<link rel="profile" href="https://gmpg.org/xfn/11">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="stylesheet" type="text/css" href="/css/all.css" media="screen" />
<script>
function formsubmit(frm) {
var col = document.getElementById(frm).elements["color"].value;
var scan = document.getElementById(frm).elements["scanner"].value;
var img = 'image' + scan;
var scanimgs = 'Scanning..<br /><img src="/scanning.gif">';
document.getElementById(img).style.display="inline-block";
document.getElementById(img).innerHTML = scanimgs;
var url = '/scan.cgi?c=' + col + '&s=' + scan;
request = new XMLHttpRequest();
try {
request.onreadystatechange = function() {
if (request.readyState == 4) {
var val = request.responseText;
document.getElementById(img).innerHTML = val;
document.getElementById(img).style.display="inline-block";
}
}
request.open("GET", url, true);
request.send();
}
catch (e) {
alert("Unable to connect to server - Scanner" + scan);
}
}

function formsubmit2(frm) {
var cols = document.getElementById(frm).elements["color"].value;
var scans = document.getElementById(frm).elements["scanner"].value;
var imgs = 'image' + scans;
var scanimg = 'Scanning..<br /><img src="/scanning.gif">';
document.getElementById(imgs).style.display="inline-block";
document.getElementById(imgs).innerHTML = scanimg
var urls = '/scan.cgi?c=' + cols + '&s=' + scans;
xhr = new XMLHttpRequest();
try {
xhr.onreadystatechange = function() {
if (xhr.readyState == 4) {
var vals = xhr.responseText;
document.getElementById(imgs).innerHTML = vals;
document.getElementById(imgs).style.display="inline-block";
}
}
xhr.open("GET", urls, true);
xhr.send();
}
catch (e) {
alert("Unable to connect to server - Scanner" + scans);
}
}
</script>
<script>
function showimage(im) {
var div = document.createElement('div');
var img = document.createElement('img');
img.src = im;
img.id = 'inlimg';
div.className = 'hdimg';
div.id = 'imrm';
div.onclick = function () {
    this.parentElement.removeChild(this);
};
window.onkeyup = function (event) {
    if (event.keyCode == '27') {
    document.getElementById("imrm").remove();
    }
}
div.appendChild(img);
document.body.appendChild(div);
document.body.style.height = 'auto';
}
</script>
<script>
function chknumber(cnt) {
var urlc = '/count.cgi?do=' + cnt;
xcnt = new XMLHttpRequest();
try {
xcnt.onreadystatechange = function() {
if (xcnt.readyState == 4) {
var cntval = xcnt.responseText;
	if(cntval === "") {
		document.getElementById("toimgs").innerHTML = 'no data';
	} else {
		document.getElementById("toimgs").innerHTML = cntval;
	}
}
}
xcnt.open("GET", urlc, true);
xcnt.send();
}
catch (e) {
alert("Unable to connect to server to count scanned images");
}
}
</script>

<style>
#imrm {position:absolute;top:20px;left:20px;height:1250px;visibility:visible;z-index:999;}
</style>
</head>
<body>
<div id="content">
<h1>Scanning images</h1>
<div id="headimages">
<div id="image1" style="display:none;"></div>
<div id="image2" style="display:none;"></div>
</div>
<div id="forms">
<div id="forms1">
<h4>Left Page</h4>
<form id="scan1">
<input type="radio" name="color" id="color11" value="gray" checked> <label for="color11">Gray</label>
<input type="radio" name="color" id="color21" value="color"> <label for="color21">Color</label>
<input type="radio" name="color" id="color31" value="noscan"> <label for="color31">No Scan</label>
<input type="hidden" name="scanner" value="1">
</form>
</div><!-- form 1-->
<div id="forms2">
<h4>Right Page</h4>
<form id="scan2">
<input type="radio" name="color" id="color12" value="gray" checked> <label for="color12">Gray</label>
<input type="radio" name="color" id="color22" value="color"> <label for="color22">Color</label>
<input type="radio" name="color" id="color32" value="noscan"> <label for="color32">No Scan</label>
<input type="hidden" name="scanner" value="2">
</form>
</div><!-- form 2-->
</div><!-- forms-->
<div id="fsubm">
<a href="#" class="myButton" onclick="formsubmit('scan1');formsubmit2('scan2');return false;">Scan</a>
</div>
<div id="toimgs"><a href="#" onclick="chknumber('count');return false">See Count</a></div>
</div><!-- content-->
</body>
</html>
```

Webpage uses two Ajax requests to send scan requests.

Here is the Perl script that actually handles scanning:
```perl
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
```
