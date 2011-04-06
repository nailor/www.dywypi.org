Title: rxvt-unicode and OS X
Summary: Collection of tips on running rxvt-unicode on OS X
Date: 2011-04-05
Tags: osx terminal urxvt

When I started at my current job at [Taiste](http://taiste.fi) I
got 15" Macbook Pro as my primary computer at work. As a long time
Ubuntu user I was faced with series of problems, mainly due to
differences in platforms. Package management is a pain I just have to
live with, [Emacs](http://emacsformacosx.com) works almost out of the
box as it should, but the terminal requires some heavy tweaking.

## Available alternatives

OS X has few alternatives available. The system ships with
[Terminal.app](http://en.wikipedia.org/wiki/Apple_Terminal), which has
been redone for Snow Leopard (aka 10.6). It's decent, looks like a
terminal, but has at least one minor and one major drawback. Minor
drawback is the lack of proper color support (yes, I **need** colors
in terminal). Terminal.app supports only 16 colors. 16, Six-teen. 70s
called and they want their terminal back.

Major drawback is that you simply can't override cmd key functionality
in any sane way to make it work as a Meta key in terminal. In
practice, your forced to use ESC as Meta key, which just does not cut
it.

Another option is [iTerm2](https://sites.google.com/site/iterm2home/).
Feels like the Swiss army knife of OS X terminals. Has load of
configuration options, even supports, in latest versions, rebinding
cmd keys as Meta keys! So after all it looks that even this milky
white cloud has a silver lining.

But unfortunately, the iTerm2 also has a major drawback: If you rebind
either of cmd keys as Meta, it wont let cmd+Tab (aka the Alt-Tab
equivalent of OS X) go through to OS X level (Emacs knows how to do
this, can't be that hard...). So basically you can't switch between
applications with keyboard when using iTerm, unless you bind Option
key to cmd, which makes option+tab switching possible, which on the
other hand breaks every single option+key combo (like parenthesis)...

## Back to the One That (Mostly) Works

I was a happy user of
[rxvt-unicode](http://software.schmorp.de/pkg/rxvt-unicode.html) on
Ubuntu, so I started searching if it would cut on OS X too. First
caveat is that it needs to be run under X11, or
[XQuartz](http://xquartz.macosforge.org/). I've been told that that's
the final frontier no true OS X user wants to confront.

However, everything went smoother than expected. First thing was to
install rxvt-unicode. I used
[homebrew](http://mxcl.github.com/homebrew/) for that:

<pre>
  brew install urxvt
</pre>

After compiling a while (binary packages, anyone?) rxvt-unicode got
installed. Butt ugly as usual, but there it was. After configuring
colors (see
[here](http://sdkmvx.wordpress.com/2008/08/13/rxvt-unicode-terminal-colors/)
for example) it was time to make it more Mac-compatible.

### Copy & Paste

As every true programmer knows, when deadlines hit the tool that Gets
Job Done is Copy & Paste. So it was essential to get copy & paste
functionality in urxvt. I use a slightly modified clipboard script on
urxvt to do the magic. It's available as a
[gist](https://gist.github.com/906248).

To get it working, you need to define it (and the shortcuts) in
`.Xdefaults` with few lines:

<pre>
  URxvt.perl-ext-common: macosx-clipboard
  URxvt*keysym.M-c: perl:macosx-clipboard:copy
  URxvt*keysym.M-v: perl:macosx-clipboard:paste
</pre>

After this, I got traditional copy & paste with cmd-C and cmd-V in
urxvt!

### Opening urls

Bart Trojanowski's excellent
[mark-yank-urls](https://github.com/bartman/urxvt-scripts) comes to
help with URLs. For OS X use, I've
[modified it a bit](https://gist.github.com/906263). In addition to
the script, I use a custom applescript to launch URLs in background in
Chrome:

<pre class="highlight applescript">
  on run argv
    tell application "Google Chrome"
      set taburl to item 1 of argv
      set myTab to make new tab at end of tabs of window 1 with properties {URL:taburl}
    end tell
  end run
</pre>

Applescript is launched via bash script (yo dawg!), which just calls
`osascript <path-to-applescript> argument`. Next step is
just to add this script and keybinding in `.Xdefaults`:

<pre>
  URxvt.perl-ext: selection,mark-yank-urls
  URxvt.keysym.M-u: perl:mark-yank-urls:activate_mark_mode
</pre>

After this, Meta-U goes to URL selection mode, C-p/C-n scroll through
URLs, y yanks (that's copying, you lesser emacsers) and Return opens
URLs in background in your Chrome.
