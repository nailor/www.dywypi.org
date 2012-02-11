Title: Back on Linux
Summary: A few thoughts on switching from Os X back to Linux
Date: 2012-02-11
Tags: osx debian linux

About a month ago I moved to Stockholm, Sweden and started working at
[Spotify](http://spotify.com). A month before starting I was asked
about my preferred setup for working. Having used OS X for year as the
primary operating system at work the choice was clear, I wanted to go
back to Linux, in this case to Debian to be exact.

## Working with Macbook Pro, a year in retrospective, the hardware

There's one thing that really stands out of Apple's laptops, the build
quality. The aluminium unibody is manufactured with precision, there's
no air intakes in the bottom of the machine (this is really useful if
you use a laptop in your lap) and the peripherals, like the touchpad,
are top quality. I really miss those and keep on wondering why there's
no PC manufacturers that would have the same overall quality of the
hardware.

The choices Apple has made also have drawbacks: The mini-DisplayPort
requires you to carry around a load of adapters, the amount of USB
ports is pretty limited and due to the missing of proper air intake
the laptop can get pretty hot, but that was really rare in my use.

Operating system OS X excelled in the hardware drivers: when you have
limited amount of hardware you need to support, building good drivers
for it is much easier. Feature that I probably miss the most was the
somewhat smart handling of external displays, along with the brilliant
multitouch gestures of the touchpad.

## ...and the software

However, the operating system was in no way par with the hardware.
Biggest grief was the memory usage. Judging from the interwebs, the
most developers purchased 8 gigabytes of memory on their machines to
start with. I had four. For web development, Python programming and
such four is more than plenty. Except if you're running OS X,
apparently.

### Completely failed memory management

OS X has a feature called
[inactive memory](http://support.apple.com/kb/HT1342). This is memory
that was recently used by an app you closed and can be quickly made to
active memory if you resume to use that app. A nice concept, that
fails miserably. OS X's documentation says, that this memory *may* be
freed at any moment. However in practice, it just keeps on
accumulating until you run out of free memory. In this case a sane
option for the OS would be freeing the inactive memory. Instead the OS
X decides to *swap the inactive memory on the disk*. So when running
out of free memory and having a 1,5 gigabytes of inactive memory left,
your OS starts paging the *unused* inactive memory to disk instead of freeing
it for applications to use. Not only this causes your computer to slow
down, it also is counter-intuitive in the terms of the original idea
of inactive memory: when it's on disk, it definitely is not made
active quickly.

I managed to find out that this memory can be freed with combination
of XCode's `purge`-command and repairing *disk* permissions. First
usually freed around 200MB of memory while latter freed almost every
bit of inactive memory. Eventually this became a daily routine. When
arriving to work the first thing was to hit repair disk permissions
button and do something else than actually use the computer for the
next five to ten minutes. Sigh.

### Messed up software installation

There are at least four different ways of installing software on OS X.
Download a DMG image, drag the icon from there to Applications folder,
run an installer, install stuff from Mac App Store or compile it
yourself. There seems to be no standard way how to do this properly.
Of course, being a software dev, I ended up using the last alternative
a lot.

However, someone had come up with a solution for manual installing: a
package distribution system that takes care of all requirements for
you. There are multiple flavours of those, I ended up using
[homebrew](http://mxcl.github.com/homebrew/).

When you have pretty much unified hardware (32/64-bit Intel) with
pretty limited number of operating system versions, one could think
that distributing binaries would be the way to go. Apparently it is
not. Using homebrew is like using Gentoo, except that it's even more
screwed up. There's no central repository for sources, it tries to
download everything from the projects sites using different methods.
After that, it compiles *everything*. Want to install library X?
Please wait, compiling and downloading tons of crap from the
interwebs, might take tens of minutes of wall time.

And of course this does not support installing Python, Ruby, Perl on
any other software that has its own way of distributing software. And
in case you mix up MacPorts and homebrew, you're deeply screwed.

And don't even get me started with the closed ecosystem thing Apple
and OS X are heading towards with rapid speed.

## Why Debian?

I'm a long time [Ubuntu](http://ubuntu.com) user, but this time I
decided to go with [Debian](http://debian.org). Why? Mostly because
our servers are Debian and because latest updates of Ubuntu have
mostly focused on breaking the desktop environment. With Debian
Squeeze I get the old and reliable Gnome 2.30 with the ability of
pinning newer packages from either backports or from testing and
unstable distributions.

Most notably I get the ultimate software installation tool, `apt-get`.
A tool that installs *binary* packages with their dependencies. A
tool, that's universally supported by Google et al., so I don't even
have any problems installing newest Chrome, for example.

Linux in general brings other improvements with it, like working
command line tools. GNU version of common tools like find and grep are
much more powerful when compared to the BSD alternatives available on
OS X.

## Do I miss something?

Sure. Even though Linux in modern times mostly works out of the box,
there's still slight issues with external displays, for example I
can't set the 30" Dell monitor at work to be the only display without
doing some `xrand` magic. I guess that's really the only thing I'm
missing from OS X, a sane and automatic way of handling external
displays. I also miss the Macbook's superior touchpad, the joystick of
Lenovo is nothing in comparison.

Would I consider switching back? No. I got working virtual desktops,
package manager and properly working memory model now, currently using
3 gigabytes out of total eight, and it includes running four virtual
machines 512 megs of memory each.

So long OS X. You were a nice experiment and I miss some parts of you,
however we definitely were not a match made in heaven.
