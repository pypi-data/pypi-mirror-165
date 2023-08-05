============================
Using the flufl.lock library
============================

.. currentmodule:: flufl.lock

The :doc:`flufl.lock <apiref>` package provides safe file locking with
timeouts for POSIX and Windows systems.  You can read more about how the
library works in the :doc:`technical details <theory>`.

Lock objects support lock-breaking so that you can't wedge a process forever.
Locks have a *lifetime*, which is the maximum length of time the process
expects to retain the lock.  It is important to pick a good number here
because other processes will not break an existing lock until the expected
lifetime has expired.  Too long and other processes will hang; too short and
you'll end up trampling on existing process locks -- and possibly corrupting
data.  However, lock lifetimes can be explicitly extended, and are implicitly
extended in some cases.

In a distributed (NFS) environment, you also need to make sure that your
clocks are properly synchronized.


Creating a lock
===============

To create a lock, you must first instantiate a :class:`Lock` object,
specifying the path to a file that will be used to synchronize the lock.  This
file should not already exist.
::

    # This function comes from the test infrastructure.
    >>> filename = temporary_lockfile()

    >>> from flufl.lock import Lock
    >>> lock = Lock(filename)
    >>> lock
    <Lock ... [unlocked: 0:00:15] pid=... at ...>

Locks have a default lifetime...

    >>> lock.lifetime.seconds
    15

...which you can change.

    >>> from datetime import timedelta
    >>> lock.lifetime = timedelta(seconds=30)
    >>> lock.lifetime.seconds
    30
    >>> lock.lifetime = timedelta(seconds=15)

You can ask whether the lock is acquired or not.

    >>> lock.is_locked
    False

Acquiring the lock is easy if no other process has already acquired it.

    >>> lock.lock()
    >>> lock.is_locked
    True

Once you have the lock, it's easy to release it.

    >>> lock.unlock()
    >>> lock.is_locked
    False

It is an error to attempt to acquire the lock more than once in the same
process.
::

    >>> from flufl.lock import AlreadyLockedError
    >>> lock.lock()
    >>> try:
    ...     lock.lock()
    ... except AlreadyLockedError as error:
    ...     print(error)
    We already had the lock

    >>> lock.unlock()

Lock objects also support the context manager protocol.

    >>> lock.is_locked
    False
    >>> with lock:
    ...     lock.is_locked
    True
    >>> lock.is_locked
    False


Lock acquisition can block
==========================

When trying to lock the file when the lock is unavailable (because another
process has already acquired it), the lock call will block.
::

    >>> import time
    >>> t0 = time.time()

    # This function comes from the test infrastructure.
    >>> acquire(filename, lifetime=5)
    >>> lock.lock()
    >>> t1 = time.time()
    >>> lock.unlock()

    >>> t1 - t0 > 4
    True


Refreshing a lock
=================

A process can *refresh* a lock if it realizes that it needs to hold the lock
for a little longer.  You cannot refresh an unlocked lock.

    >>> from flufl.lock import NotLockedError
    >>> try:
    ...     lock.refresh()
    ... except NotLockedError as error:
    ...     print(error)
    <Lock ...

To refresh a lock, first acquire it with your best guess as to the length of
time you'll need it.

    >>> from datetime import datetime
    >>> lock.lifetime = 2 # seconds
    >>> lock.lock()
    >>> lock.is_locked
    True

After the current lifetime expires, the lock is stolen from the parent process
even if the parent never unlocks it.
::

    # This function comes from the test infrastructure.
    >>> t_broken = waitfor(filename, lock.lifetime)
    >>> lock.is_locked
    False

However, if the process holding the lock refreshes it, it will hold it can
hold it for as long as it needs.

    >>> lock.lock()
    >>> lock.refresh(5) # seconds
    >>> t_broken = waitfor(filename, lock.lifetime)
    >>> lock.is_locked
    False


Time outs
=========

When attempting to acquire a lock, you can specify a timeout interval as
either an integer number of seconds, or as a :class:`datetime.timedelta`.
If the lock is not acquired within this interval, a :class:`TimeOutError` is
raised.

You can specify a default timeout interval in the :class:`Lock` constructor.

    >>> from flufl.lock import TimeOutError
    >>> acquire(filename, lifetime=5)
    >>> try:
    ...     with Lock(filename, default_timeout=1) as my_lock:
    ...         pass
    ... except TimeOutError:
    ...     print('Timed out, as expected')
    Timed out, as expected

You can also specify a timeout interval in the :func:`Lock.lock` call.  This
overrides the constructor argument.

    >>> acquire(filename, lifetime=5)
    >>> my_lock = Lock(filename, default_timeout=1)
    >>> try:
    ...     my_lock.lock(timeout=10)
    ...     my_lock.is_locked
    ... finally:
    ...     my_lock.unlock()
    True


Lock details
============

Lock files are written with unique contents that can be queried for
information about the host name the lock was acquired on, the id of the
process that acquired the lock, and the path to the lock file.

    >>> import os
    >>> lock.lock()
    >>> hostname, pid, lockfile = lock.details
    >>> hostname == lock.hostname
    True
    >>> pid == os.getpid()
    True
    >>> lockfile == filename
    True
    >>> lock.unlock()

Even if another process has acquired the lock, the details can be queried.

    >>> acquire(filename, lifetime=3)
    >>> lock.is_locked
    False
    >>> hostname, pid, lockfile = lock.details
    >>> hostname == lock.hostname
    True
    >>> pid == os.getpid()
    False
    >>> lockfile == filename
    True

However, if no process has acquired the lock, the details are unavailable.

    >>> lock.lock()
    >>> lock.unlock()
    >>> try:
    ...     lock.details
    ... except NotLockedError as error:
    ...     print(error)
    Details are unavailable

You can also get the time at which the lock will expire.

    >>> now = datetime.now()
    >>> import time
    >>> time.sleep(1)
    >>> with lock:
    ...     lock.refresh()
    ...     lock.expiration > now + lock.lifetime
    True


Lock state
==========

You might want to try to infer the state of the lock.  This is not always
possible, but this library does try to provide some insights into the lock's
state.  However, it is up to the user of the library to enforce policy based
on the lock state.

The lock state is embodied in an enumeration.

    >>> from flufl.lock import LockState

The lock can be in the unlocked state.

    >>> lock.state
    <LockState.unlocked: 1>

We could own the lock, as long as it is still fresh (i.e. it hasn't expired
its lifetime yet), the state will tell us.

    >>> with lock:
    ...     lock.state
    <LockState.ours: 2>

It's possible that we own the lock, but that its lifetime has expired.  In
this case, another process trying to acquire the lock will break the original
lock.

    >>> lock.lifetime = 1
    >>> with lock:
    ...     time.sleep(1.5)
    ...     lock.state
    <LockState.ours_expired: 3>

It's also possible that another process once owned the lock but it exited
uncleanly.  If the lock file still exists, but there is no process running
that matches the recorded pid, then the lock's state is stale.

    >>> acquire(lock.lockfile, lifetime=10)
    >>> simulate_process_crash(lock.lockfile)
    >>> lock.state
    <LockState.stale: 4>

If some other process owns the lock, we can't really infer much about it.
while we can see that there is a running process matching the pid in the lock
file, we don't know whether that process is really the one claiming the lock,
or what its intent with the lock is.
::

    # This function comes from the test infrastructure.
    >>> acquire(lock.lockfile, lifetime=2, extra_sleep=3)
    >>> lock.state
    <LockState.unknown: 6>

However, once the lock has expired, we can at least report that.

    >>> time.sleep(2)
    >>> lock.state
    <LockState.theirs_expired: 5>


Lock file separator
===================

Lock claim file names contain useful bits of information concatenated by a
*separator character*.  This character is the caret (``^``) by default on
Windows and the vertical bar (``|``) by default everywhere else.  You can
change this character.  There are some restrictions:

* It cannot be an alphanumeric;
* It cannot appear in the host machine's fully qualified domain name
  (e.g. the value of :data:`Lock.hostname`);
* It cannot appear in the lock's file name (the argument passed to the
  :class:`Lock` constructor)

It may also be helpful to avoid `any reserved characters
<https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words>`_ on
the file systems where you intend to run the code.

    >>> lock = Lock(filename, separator='+')
    >>> lock.lock()
    >>> hostname, pid, lockfile = lock.details
    >>> hostname == lock.hostname
    True
    >>> pid == os.getpid()
    True
    >>> lockfile == filename
    True
    >>> with open(filename) as fp:
    ...     claim_file = fp.read().strip()
    ...     '+' in claim_file
    True
    >>> lock.unlock()
