==================================
flufl.lock - An NFS-safe file lock
==================================

This package is called ``flufl.lock``.  It is an NFS-safe file-based lock with
timeouts for POSIX systems.


Requirements
============

``flufl.lock`` requires Python 3.7 or newer.


Documentation
=============

A `simple guide`_ to using the library is available, along with a detailed
`API reference`_.


Project details
===============

 * Project home: https://gitlab.com/warsaw/flufl.lock
 * Report bugs at: https://gitlab.com/warsaw/flufl.lock/issues
 * Code hosting: https://gitlab.com/warsaw/flufl.lock.git
 * Documentation: https://flufllock.readthedocs.io/

You can install it with ``pip``::

    % pip install flufl.lock

You can grab the latest development copy of the code using git.  The master
repository is hosted on GitLab.  If you have git installed, you can grab
your own branch of the code like this::

    $ git clone https://gitlab.com/warsaw/flufl.lock.git

You can contact the author via barry@python.org.


Copyright
=========

Copyright (C) 2004-2022 Barry A. Warsaw

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Table of Contents and Index
===========================

* :ref:`genindex`

.. toctree::
    :glob:

    using
    theory
    apiref
    NEWS


.. _`simple guide`: using.html
.. _`API reference`: apiref.html
