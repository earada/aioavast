Asyncio library for Avast Antivirus
===================================

asyncio (PEP 3156) Avast Linux support

Features
--------

- Scanning files and/or directories.
- Checking URLs.
- Exclude files from the scanning.
- Get and set the list of enabled or disabled pack and flags.


Requirements
------------

- Python >= 3.3
- asyncio https://pypi.python.org/pypi/asyncio


License
-------

``aioavast`` is offered under the MIT license.


Source code
------------

The latest developer version is available in a github repository:
https://github.com/earada/aioavast

Getting started
---------------

Scanning
^^^^^^^^

Scan a file and prints its output:

.. code-block:: python

  import asyncio
  from aioavast import Avast

  @asyncio.coroutine
  def scan(item):
      av = Avast()
      yield from av.connect()
      return (yield from av.scan(item))

  if __name__ == '__main__':
      loop = asyncio.get_event_loop()
      results = loop.run_until_complete(scan('/bin/ls'))
      print(results)


You can check an url too:

.. code-block:: python

  return (yield from av.checkurl('http://python.org'))


Exclude items
^^^^^^^^^^^^^

There is also a possibility to exclude certain files from being scanned.

.. code-block:: python

  import asyncio
  from aioavast import Avast

  @asyncio.coroutine
  def dont_scan(item):
      av = Avast()
      yield from av.connect()
      yield from av.exclude(item)
      return (yield from av.scan(item))

  if __name__ == '__main__':
      loop = asyncio.get_event_loop()
      results = loop.run_until_complete(scan('/bin/ls'))
      print(results)

You can retrieve excluded items by:

.. code-block:: python

  excluded = yield from av.exclude()


Other methods
^^^^^^^^^^^^^

You could modify Flags and Packs too.

.. code-block:: python

  flags = yield from av.flags()
  yield from av.flags("-allfiles")

  packs = yield from av.pack()
  yield from av.flags("-ole")
