``tofipa`` finds each file in a torrent beneath one or more download locations
and prints the download location where the first file was found or adds the
torrent to a BitTorrent client.

Matching files are found by comparing the file size and a few piece hashes.

Matching files with a path that differ from what the torrent expects are linked
to the expected paths. To get the expected path, the download location of the
first matching file is combined with the relative file path from the
torrent. Hard links are created if possible, symbolic links are used as a
fallback.

A default download location is used if not even a single file from the torrent
can be found in the file system.

If the torrent is added to a BitTorrent client, there is no output. Otherwise,
the the download location is printed to stdout. Errors and warnings are printed
to stderr.

Algorithm
---------

``TORRENT`` refers to the provided torrent file.

``LOCATION`` is a download directory (the download path without the torrent's
name) provided via ``--location`` and ``~/.config/tofipa/locations``.

1. Find files from ``TORRENT`` in the file system. For each file in ``TORRENT``:

   a) Find a file beneath each ``LOCATION`` with the same size.

   b) Sort multiple size matching files by file name similarity. The file name
      most similar to the one in ``TORRENT`` is processed first.

   c) Hash some pieces to confirm the file content is what ``TORRENT`` expects.

2. If at least one matching file is found, set the download location to the
   ``LOCATION`` of the first matching file.

   If there are no matching files, set the download location to the location
   specified via ``--default`` or the first ``LOCATION``.

3. Make sure every matching file exists beneath the download location with the
   same relative path as in ``TORRENT``. Try to create a hard link and default
   to a symbolic link if source and target are on different file systems.

4. If a client is configured and ``--noclient`` is not given, add ``TORRENT`` to
   the client specified via ``--client`` or the first client in
   ``~/.config/tofipa/clients.ini``.

   If no client is configured or ``--noclient`` is given, print the download
   location to stdout. This is the only output on stdout.

Installation
------------

``tofipa`` is on `PyPI <https://pypi.org/project/tofipa/>`_. The recommended
installation method is with `pipx <https://pypa.github.io/pipx/>`_:

.. code-block:: sh

   $ pipx install tofipa

Configuration
-------------

Besides command line options, there are configuration files in
``$XDG_CONFIG_HOME/tofipa/``. ``$XDG_CONFIG_HOME`` defaults to ``~/.config/``.

``~/.config/tofipa/locations``
==============================

``~/.config/tofipa/locations`` is a simple list of download directories. These
are searched for torrent files. There is some support for globbing and
environment variables.

Any directories provided via the ``--location`` argument are searched first in
addition to the directories from ``~/.config/locations``.

Example ``locations``
^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    # Lines that start with "#" and empty lines are ignored.

    # The first download location is the default that is used if no matches are
    # found and --default is not given.
    /downloads/

    # More directories can be listed individually.
    /stuff/various/
    /stuff/more/
    /stuff/other/

    # ... or you can use "*" to include all subdirectories.
    /stuff/*

    # Environment variables can be used as usual. There is no support for fancy
    # expansion stuff like "${FOO:-bar}".
    # NOTE: To keep you sane, unset and empty environment variables are an
    # error case.
    $HOME/downloads

``~/.config/tofipa/clients.ini``
================================

``~/.config/tofipa/clients.ini`` contains all the information that is needed to
add a torrent to a BitTorrent client. Section names are arbitrary strings that
can be passed to ``--client``. If ``--client`` is not given, the first client in
``~/.config/tofipa/clients.ini`` is used.

Comments start with ``#``.

Options
^^^^^^^

.. list-table::

   * - Option
     - Description
     - Valid Values
     - Default

   * - client
     - Name of the BitTorrent client
     - ``deluge``, ``qbittorrent``, ``rtorrent``, ``transmission``
     - Must be provided for every section

   * - url
     - How to connect to ``client``
     - See below
     - See below

   * - username
     - Username for authentication against ``client``
     - Any string
     - Empty

   * - password
     - Password for authentication against ``client``
     - Any string
     - Empty

   * - verify
     - Whether a torrent should be hash checked by the client after it is added
     - true/false, yes/no, on/off, 1/0
     - ``true`` for ``transmission``, ``false`` for other clients

   * - stopped
     - Whether a torrent should be active right away
     - true/false, yes/no, on/off, 1/0
     - ``false``

Client URLs
^^^^^^^^^^^

.. list-table::

   * - Client
     - Format
     - Default

   * - ``deluge``
     - ``[USERNAME:PASSWORD@]HOST[:PORT]``
     - ``localhost:58846``

   * - ``qBittorrent``
     - ``[http[s]://][USERNAME:PASSWORD@]HOST[:PORT]``
     - ``http://localhost:8080``

   * - ``rTorrent``
     - ``[scgi://]HOST[:PORT]`` or
       ``[file://]SOCKET_PATH`` or
       ``http[s]://[USERNAME:PASSWORD@]HOST[:PORT][/PATH]``
     - ``scgi://127.0.0.1:5000``

   * - ``Transmission``
     - ``[http[s]://][USERNAME:PASSWORD@]HOST[:PORT][/PATH]``
     - ``http://localhost:9091/transmission/rpc``

Example ``clients.ini``
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    [foo]
    client = qbittorrent
    url = localhost:5000
    username = hunter1
    password = hunter2

    [bar]
    client = rtorrent
    url = http://localhost:12345
    verify = true

    [baz]
    client = transmission
    stopped = yes
