Title: The impact of document IDs on performance of CouchDB
Summary: A story of the impact of the bad document IDs in CouchDB
Date: 2010-11-11
Tags: couchdb performance nosql databases

(This text is copied from [blog.inoi.fi](http://blog.inoi.fi) to my
personal blog, as I no longer work there and think this is a keeper)

<p>
 One major part of our product is a data acquisition framework. The
 framework is responsible of gathering data on devices and sending it
 to the server. The server then processes the data and eventually
 stores it in <a href="http://couchdb.org/">CouchDB</a>.
</p>
<p>
 CouchDB storage is pretty simple. It's just a single database where
 the data gets inserted with a random ID. Removals or modifications
 are hardly done to the data after it has been inserted there, its
 only function is just to be read later and to be displayed as graphs
 and such
</p>

<h2>Things started to get weird</h2>

<p>
 However, the data server started to behave strangely. First symptoms
 were slow inserts and huge disk usage of the database. For the slow
 inserts we first suspected the reason was that we were not using
 <a href="http://wiki.apache.org/couchdb/HTTP_Bulk_Document_API">CouchDB's
 bulk document API</a> for inserting the data but after fixing that
 we only got a minor speed increase. The compaction of the database
 didn't really help, as it compacted the database too slow, peak rate
 being 300 documents per second and the average about 100 doc/s. With
 8 million docs that takes a while. Worst thing was that the
 compaction didn't even reduce the disk usage. The database ate 26
 gigabytes of disk containing only 8 million documents. That's a
 whopping 3 kilobytes per document, and the documents were really
 about 100 bytes in size.
</p>
<p>
 What was even weirder we didn't really see anything strange in the
 way the server performed. IO ops were low, CPU usage was low and
 there was a plenty of free memory. Heck, we even could write zeros
 (<tt>dd if=/dev/zero of=/var/somefile.img</tt>) on the disk at the
 rate of 50Mb/s. Even killing most of the other services didn't help:
 CouchDB just kept being slow. We even upgraded the CouchDB in our
 test environment to try if it helped, but we only gained small
 performance gain from that operation.
</p>

<h2>Let's not be that random</h2>

<p>
 As you might have
 heard, <a href="http://dilbert.com/strips/comic/2001-10-25/">the
 problem with the random is that you never can be sure</a>. So after
 a week or so pondering the issue we stumbled upon
 on <a href="http://guide.couchdb.org/draft/performance.html#bulk">a
 chapter about bulk inserts and monotonic DocIDs</a> in the
 excellent <a href="http://guide.couchdb.org/">CouchDB guide</a>.
 With a tip from the awesome folks
 at <a href="irc://irc.freenode.net/couchdb">#couchdb</a> we rebuilt
 our system using sequential IDs instead of purely random IDs.
</p>

<p>
 We copied the idea of sequential IDs straight from CouchDB which
 uses them for its auto-generated DocIDs. We just needed to implement
 it in Python and ended up with the following:
</p>

 <script src="https://gist.github.com/672279.js"> </script>

<p>
 The </p><tt>SequentialID</tt> is a random 32 character hexadecimal
 string. The first 26 characters is a prefix that stays the same for
 approx. 8000 subsequent calls. The suffix is increased
 monotonically. After around 8000 calls the the prefix is regenerated
 and the suffix is reseted to a small positive value. We also built
 another one using ISO-formatted UTC-timestamp with few random digits
 suffixed.
<p></p>

<p>
 Now you might think that we would have collisions with the
 </p><tt>SequentialID</tt>, especially if multiple processes are
 writing to the same CouchDB database. However, we're not since the
 prefix is a random generated string and the entropy (i.e. string
 length) is big enough to make the collision highly unlikely. Plus
 the SequentialID is never shared between processes it is regenerated
 for every single one instead.
<p></p>

<h2>Performance rocketed through the roof</h2>

<p>
 No fix would be good without performance metrics so Petri
 wrote <a href="https://gist.github.com/672229">a small benchmarking
 script</a>.
</p>
<p>
 This showed us the huge performance increase we got. The write speed
 is almost <b>four</b> times as fast with sequential IDs than with
 random IDs. Not to mention that the database takes a one
 seventh of the space on the disk! We didn't try the compaction
 speed, but everything indicates that should be a lot faster too.
</p>

<h2>How does it work?</h2>
<p>
 The reason why this worked is due to the design how CouchDB stores
 it data on the disk. Internally CouchDB uses
 <a href="http://en.wikipedia.org/wiki/B%2B-tree">B+-tree</a> (from
 now on referred as B-tree) to store the data of a single database.
 Now if the data that is inserted in the B-tree (in this case, the
 DocIDs) is random, it causes the tree to fan out quickly. As the
 minimum fill rate is 1/2 for every internal node, the nodes are
 mostly filled up to the 1/2 (as the data spreads evenly due to its
 randomness) generating more internal nodes than before.
</p>
<p>
 More the internal nodes the more disk seeks the CouchDB has to
 perform to write the correct leaf to write the data in to. This is
 why we didn't see any IO ops stacking up: <em>the disk seeks do not
   show up in the iostat</em>! And this was the single biggest cause
 to slow down both reads and especially writes of our CouchDB
 database.
</p>
<p>
 The problem aren't even limited to the disk seeking. The randomness
 of the DocIDs causes the tree structure to be changed often (due to
 the nature of B-trees). When using append only log the database has
 no other way to do than rewrite the whole new structure of the tree
 to the end of the append only log. As this gets more common and
 common as more random data gets poured in, the disk usage grows
 rapidly, eventually hogging a lot more disk than the data in the
 database is actually requiring. Not only this, this <em>slow down
 compaction</em> too, as the compaction needs to constantly rebuild
 the new database.
</p>
<p>
 The B-tree is why using the (semi-)sequential IDs is a real life
 saver. The new model causes the database to be filled in orderly
 fashion and the buckets (i.e. leafs) are filled in instead of
 leaving them half full. Best part here is that the auto generated
 IDs by CouchDB (which were not an option for us) already use the
 sequential ID scheme, so using those IDs you don't really need to
 worry a thing.
</p>
<p>
 So remember kids: if you cram loads of data in your CouchDB, remember to select your document ID scheme carefully!
</p>
