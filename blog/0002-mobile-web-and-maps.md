Title: Mobile Web Development and Maps
Summary: Handling location data and maps in mobile web applications
Date: 2011-07-28
Tags: mobile web maps geolocation integration

Lately I've been working on
[Helsinki Festival mobile site](http://m.juhlaviikot.fi) (in Finnish).
The main idea of the site is to provide mobile information for users,
including location and maps of the venues. While implementing the
venue locations and other, yet upcoming, features, I've run in to a
series of problems of which some should be shared to the wild.

## Supporting wide range of devices

Due to heterogeneity of attendees the site should support a wide range
of devices. At [Taiste](http://taiste.fi) we sport a few test devices:
iPhone 4, HTC Desire with original firmware and another one rooted
with [Cyanogenmod](http://cyangenmod.com) and two Nokia devices, the
flagship N8 and an older E75. Pretty decent coverage of mobile
platforms in circulation in Finland.

I'm not going to discuss about rendering woes and missing `<meta
name="viewport">` support here, even though they are challenges that
just need to be handled when building a site like this. The problem I
want to focus on is the functionality of maps and navigation on a
mobile web site.

## Displaying a map

I started with a dual-mode map: A static image, courtesy of Google,
for devices without proper JavaScript support and a fancy embedded
Google Map for devices with JavaScript support. However, this turned
out to be a bit problematic.

First caveat: scrolling. On touch screen phones the scrolling of venue
pages, which have embedded map, was misleading; if user started
scrolling (i.e. placed her finger) on the map, she would end up
scrolling the map instead of the site. By scrolling the map user would
also lose sight of the marker, placed on the map. On
[Google Maps API](http://code.google.com/apis/maps/index.html) this is
fairly easy to disable just by passing `draggable: false` to options
of the constructor of a `Map` object.

Second caveat: The marker. On the embedded map we drew a nice yellow
marker. However, the Nokia N8 failed to display this marker. According
to my debugging sessions the problem resides somewhere in the Google's
Map Marker API, though I can't say for sure. The phone does not report
any JavaScript errors, so it must be rendering the Marker to a wrong
place or underneath the map element (if it renders it at all). Even
with furious debugging applied, the marker could not be seen on the
map.

Now the second problem was a bit harder to solve: there didn't seem to
be any way we could solve it. The N8 sports a Symbian browser 7.2,
which is equipped with Webkit version 525, the
[same version Chrome 1.0, iPhone 2.2 and Android 1.0 had in 2008](http://www.quirksmode.org/webkit.html#link2),
except that somehow it's crappier than those. Luckily, the new Symbian
Anna upgrade should bring Browser 7.3, which has a newer webkit and
it even includes `viewport` meta-tag support!

To overcome these two problems I wrote a custom template tag that just
outputs an `img` tag that has an URL to a 240x240 map picture (240 is
the smallest horizontal resolution we support) showing the location.
The `img` tag is then later on accompanied with a small JavaScript
that transforms the `src` attribute to point to a wider map picture.
JavaScript is needed to sniff the width of the containing `div`
element by using `element.clientWidth`. Oh, and while doing this I
also discovered that Google Maps API limits the image width to 640
pixels. Damn.

Not only the static image overcame these both problems but it also
renders a neater marker, with drop shadows and all!

## Providing links to the internal navigator application

To ease the finding of a venue site provides a link to an internal map
application. Or more specific: *tries* to provide one. We started with
linking directly to [Google Maps](http://maps.google.com/) with proper
longitudes and latitudes in the URL. This works *mostly* fine: on
iPhone and on Android it, in *almost* every case, opens up the native
Google Maps application. *Almost*.

### HTC woes

During last firmware update [HTC](http://htc.com/) rolled out a new
version of their customized Android Browser (which they call
"Internet"). This updated Internet contains a small, but pretty
annoying bug: it seems to break URL handling so that the Google Maps
links are now opened in browser by default and there's no way to
change this default. I haven't explored if it does the same with other
URLs. My hypothesis is that this could be related to their own
navigation software, Route 66, which is shipped with newer HTC Android
devices. It could possibly open by default the Google Maps links in
this application. However, the app is not available for Desire.
Apparently I'm not
[alone](http://www.google.ru/support/forum/p/Google+Mobile/thread?tid=635945813b796094&hl=en)
[with](http://www.google.ru/support/forum/p/Google+Mobile/thread?tid=10cad2d45a87a24f&hl=en)
[this](http://www.google.com/support/forum/p/maps/thread?tid=73662f90526a8cca&hl=en).
Funny thing is that if I type `maps.google.com` in the Google Search
app (not the website), it asks me politely if I want to open Maps or
Browser. So HTC has definitely broke something while modifying the
browser.

Needless to say, the link works fine on the Cyanogenmod Desire, as it
sports nearly vanilla Android browser by Google. The bad thing here
is that there's no other way to send a link that suggests the phone to
open Maps application with correct coordinates.

### N8 woes and yays

[The Nokia Browser documentation developer.nokia.com](http://www.developer.nokia.com/Resources/Library/Web/nokia-browsers.html)
does not say a thing about opening Ovi Maps from a website. After some
excessive googling I found a forum post that mentioned briefly about
an undocumented `services` URI scheme. By calling that URI scheme with
a properly formatted URL, in this case
`services://C2A?C2Aid=2305&Version=1.0&2305=Landmark(lat=XXX&long=YYY)`,
it opens up the Ovi Maps application with a marker at the latitude and
longitude specified. You can even supply a name with additional `name`
parameter given to the `Landmark` "constructor"!

### ...and the issues with Series 60

Even though Nokia E75 has the same generation browser as N8, it does
not support `services` URI scheme, at least not in the same format. I
also failed to find any documentation or experience about opening Ovi
Maps application from a link, so the built-in navigation is a no-go
with E75. With S60, we're stuck with mobile Google Maps URL and the
experience is not optimal. You could even craft a URL that gives you
directions, but that would require knowing your current location and
E75s browser does not support Geolocation API, so that's a no-go too.


## Conclusion

If it would be satsifying for us to serve only iPhone/iOS and Android
devices (sans current incarnation of HTC Desire, possibly other HTC
Android devices too) the mapping would be easy: Either display a
JavaScript map (pretty usable on those devices) or use static image
provided by El Goog with a properly formatted link to
`maps.google.com`.

However, if you need to support other OSs, it might require tremendous
amounts of googling around the interwebs. I don't even have a clue how
Bada or WP7 works, but luckily they both are a small minority in the
browser market. I also couldn't find anything for Series 40, so the
Nokia seems to keep consistent line of undocumenting through the
product line.

My suggestion to mobile phone manufacturers would be a single page of
documentation describing the supported URI schemes of the built-in
applications to tell the developer what's possible and what's not.
With examples, of course.

P.S. At the moment of writing this, we yet haven't launched the new
maps and map links in to the wild, but we're in the process of doing
so.
