Title: Rewinding during rebase
Summary: Ever needed to go back in commits in rebase? This should help
Date: 2011-10-11
Tags: git version-control howto

A fellow pythonaut asked a question on #python.fi IRC channel: would
it be possible to "rewind" during `git rebase --interactive`? He
wanted to go back and edit a few commits during his massive rebase
operation and then continue the operation from the same point.

## Initial situation

I assume you know in general what
[rebase](http://help.github.com/rebase/) does (too bad the kernel.org
has no longer the man pages, or anything to that matter, served). If
not, I suggest to check that previous link or to run `git help
rebase` on your commandline.

Now, let's assume you have following repository structure:

<pre>
      D - E - F (*another-branch)
     /
A - B - C (master)
</pre>

You want to rebase `another-branch` on top of the `master` and edit
every one of those commits on the way. Naturally, you use `git rebase
--interactive master` while checked in `another-branch`. Now you edit
commits D and E, transforming them to D' and E' respectively, and you
have a following repository structure (in middle of the rebase):

<pre>
      D - E - F (another-branch)
     /
A - B - C - D' - E' - F (HEAD)
        ^
      master
</pre>

Now, while editing F, you notice that you forgot to add something in
D while rebasing it. Traditionally, the two options here are to abort
rebase, rebase again and correct mistakes or to skip remaining commits
and manually cherry-pick them back after rebase. But let's assume
you've modified a load of commits and need to modify yet another load
of commits in this rebase, so you don't want to abort. The solution?
Let's just mimick how the rebase works!

## Magic part: Rewinding in rebase!

First: Let's create us a point to return to by creating a temporary
branch in the F commit: `git branch continue`.

Then, let's checkout the commit we want to modify: `git checout D'`
and let's hack it for the parts that's needed. After hacking, we'll
replay the rebase: Technically rebase with edits is just cherry
picking of commits, so well do that. First let's see what to
cherry-pick by running `git log continue`, which returns something
like this:

<pre>
486106d edit edit (F)
ea857b6 Moar edits (E')
</pre>

Now we just replay the rebase by issuing `git cherry-pick ea857b6` and
`git-cherry-pick 486106d`. No we're back at where we checkouted back
to the D' and can continue rebase normally! Just do the edits on the F
you need to do and say `git rebase --continue` and you'll get on with
your rebase!

# Word of caution

This is more of a proof of consept trick and has worked on one real
life scenario (and I've tested it on simulated environment), but I
recommend you to back up your working directory / `.git` before trying
this at home :p

