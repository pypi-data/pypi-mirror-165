===================
 Technical details
===================

.. currentmodule:: flufl.lock

The :doc:`flufl.lock <apiref>` package provides NFS-safe file locking.  We say
"NFS-safe" because the behavior of the locks are dictated by POSIX standards,
and are guaranteed to work even when the processes involved are running on
different machines which only share a common file system over `NFS`_.

The basic implementation of our :class:`Lock` objects is described by the
GNU/Linux `open(2)`_ manpage, under the description of the ``O_EXCL`` option:

    [...] O_EXCL is broken on NFS file systems, programs which rely on it for
    performing locking tasks will contain a race condition.  The solution for
    performing atomic file locking using a lockfile is to create a unique file
    on the same fs (e.g., incorporating hostname and pid), use link(2) to make
    a link to the lockfile.  If link() returns 0, the lock is successful.
    Otherwise, use stat(2) on the unique file to check if its link count has
    increased to 2, in which case the lock is also successful.

The assumption here is that there will be no *outside interference*, e.g. no
agent external to this code will ever `link()`_ to the specific lock files
used.


Lock files and claim files
==========================

When a :class:`Lock` object is instantiated, the user names a file system
path in the constructor.  This is the file that all processes will synchronize
on when attempting to acquire the lock.  We call this the *lock file*.  This
file should not already exist.

Locks have a *lifetime* which is the period of time that the process expects
to keep the lock, once it has been acquired.  This lifetime is used to
calculate whether a lock is stale, i.e. the process that acquired the lock
exited without cleanly unlocking it.  Stale locks can be broken by another
process.

It's good to use a reasonable lifetime, not too long and not too short.  If
the lifetime is too long, then stale locks may not be broken for quite some
time.  Too short and another process will break a lock that isn't stale.  Keep
in mind though that lock lifetimes can be explicitly extended, and in some
cases will be implicitly extended.  So if you're using the lock to protect a
resource for a long time, try to periodically refresh the lock after you've
acquired it, and set the lifetime to just longer than your expected refresh
period.

Internally, every :class:`Lock` object also has a *claim file*.  This is a
file system path unique to the object which will be hard linked to the lock
file.  The claim file isn't actually created until the process attempts to
acquire the lock.  The name of the claim file is made up of several bits of
data intended to make this claim file name unique across all :class:`Lock`
object.  The claim file name consists of:

* The name of the lock file
* The current  hostname as returned by :func:`socket.getfqdn()`
* The current process id
* A random integer from 0 to :data:`sys.maxsize`

Once defined, the claim file name never changes.  The claim file only ever
actually exists while the process is acquiring or has acquired the lock,
although it may hang around in an unlinked state if the lock has been broken.


Acquiring the lock
==================

These are the steps for acquiring a lock:

* The user defines a *timeout* period, which is the length of time in seconds
  that the lock acquisition will be attempted.  If the lock cannot be acquired
  within this time period, a :class:`TimeOutError` is raised.
* The claim file is created.  The name of the claim file is written to the
  contents of the claim file.  The reason for this will be evident later.
* The claim file is *touched*.  Touching the file means that the file's
  ``atime`` and ``mtime`` are modified to point to a timestamp some time in the
  future.  This future time is the current time plus the lock's lifetime, and
  it indicates the the time in the future after which the lock will be
  considered stale.
* A `hard link`_ is created with the claim file as the source and the lock file
  as the destination.  This makes sense: the claim file has already been
  created (see above), and if no other process has acquired the lock, then
  this step creates the lock file.  On success, the lock file and claim file
  will point to the same physical file and the lock will be considered
  acquired.
* If the hard link is successful, the lock's lifetime is immediately
  refreshed to ensure it represents the lifetime plus the timestamp when the
  lock was acquired.  This is because if a process needed to wait some amount
  of time for another process to release the lock, you want the current lock's
  lifetime to be relative to the actual lock acquisition time.

There are several reasons why the hard link attempt could fail.  If any of
these conditions occur, the :meth:`Lock.lock()` method will sleep for a short
amount of time and try again, assuming the timeout period hasn't expired, and
that the lock isn't considered stale.

* The *link count* of the lock file is not 2.  The only way this can happen is
  if some outside agent is messing with us.  That weird state is logged, but
  the lock acquisition attempt continues after a sleep.
* Some weird, but innocuous exception can occur, such as an ``ENOENT`` or an
  ``ESTALE``.  NFS servers can return these errnos depending on the platform.
  As above, when this happens, the lock acquisition just sleeps for a short
  time and tries again.
* Any other :class:`OSError` will get logged, the claim file will be unlinked
  and the exception will get re-raised immediately.
* If the contents of lock file is equal to the claim file name, then this
  indicates that the current process *already* has the lock acquired, and a
  :class:`AlreadyLockedError` is raised.  This is why we write the claim file
  name into the file.


Breaking the lock
=================

Let's say the linking operation fails because :meth:`Lock.lock()` determines
that another process has acquired the lock.  The next thing that happens is a
check for lock staleness.  Remember that a lock is defined to be stale if the
timestamp recorded in its ``atime`` and ``mtime`` have been exceeded.  In this
case, the lock will be broken.  This is also known as *stealing the lock*.

When breaking a lock, the lock file is first removed.  This is technically the
act that breaks the lock.  However, before removing the lock file, its
contents are read to find the other process's claim file path.  This claim
file, if it exists, is also removed.  This should leave the file system in a
fairly clean state, even if process that used to own the lock has exited
uncleanly.

There are a few caveats to keep in mind.

First, it's not technically possible to determine whether another active,
running process actually owns the lock.  This is especially true if the locks
are acquired on different machines coordinating through a shared (e.g. NFS)
file system.  However you can gain some insight into the state of a lock by
using the :data:`Lock.state` attribute and checking the :class:`LockState`
enum that's returned.  This state is *not* consulted when deciding whether to
break a lock though; in that case only the lock's lifetime is considered.

There is a small race condition window present when breaking the lock.  It's
possible that two processes are blocked on acquiring a stale lock that was
previously acquired by a now-defunct third process.  To reduce this (it cannot
be totally eliminated), a process breaking the lock starts by *touching* the
lock, thus simulating an extension of the lock's lifetime.  If the second
process looks at the expiration time, it may in fact see that the lock has
*not* yet expired, closing the race window.  Ultimately, even if this fails,
the lock is still guaranteed to be acquired by only one process, because the
link creation operation is guaranteed to be atomic by POSIX.


Lifetime extension
==================

As mentioned, processes can explicitly extend the lifetime of a lock it owns,
which can be used to ensure continuous ownership of resources in long running
tasks.  There are some cases where the :class:`Lock` implementation implicitly
extends the lifetime of a lock:

* When first attempting to acquire a lock
* After a lock is acquired
* When asking whether a lock is acquired through the :data:`Lock.is_locked`
  property.  This prevents a lock breaking race condition between the time the
  property is accessed and the answer is returned.
* When a lock is about to be broken

Generally, you don't need to worry about implicit lifetime extension since the
only user-facing case is when accessing :data:`Lock.is_locked`.

Locks always have a default lifetime, but this can be set in the :class:`Lock`
constructor.  It can also be optionally changed in the :meth:`Lock.refresh()`
method.  In any case, the lifetime always represents the number of seconds
into the future at which the lock will expire, relative to "now".  "Now" is
always calculated when the lock is refreshed, either explicitly or implicitly.


.. _`open(2)`: http://manpages.ubuntu.com/manpages/dapper/en/man2/open.2.html
.. _`link()`: https://manpages.ubuntu.com/manpages/focal/en/man2/link.2.html
.. _`NFS`: https://en.wikipedia.org/wiki/Network_File_System
.. _`hard link`: https://en.wikipedia.org/wiki/Hard_link
