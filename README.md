# SANE_scanner
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


