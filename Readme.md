Linux Load Stanley Driver
===========

A driver to record system load information from a Linux machine to a [Stanley] database.

https://gitlab.com/claudiomattera/linux-load-stanley-driver/

[Stanley]: https://gitlab.com/claudiomattera/stanley/

Copyright Claudio Mattera 2019

You are free to copy, modify, and distribute PyStanley with attribution under the terms of the MIT license. See the `License.txt` file for details.


Installation
----

The library is available as three different packages:

-   Debian package, usable on Debian/Ubuntu and derivatives (anything that uses `apt`/`apt-get`).
    Install it with the following command (possibly prepended with `sudo`).

        dpkg -i /path/to/python3-pystanley_1.0.0-1_all.deb

-   Python wheel package, usable on Windows and almost every system with a Python 3 distribution.
    Install it with the following command (possibly prepended with `sudo`, or passing the `--user` option).

        pip3 install /path/to/pystanley-1.0.0-py3-none-any.whl

-   Tarball source package.
    It can be used by maintainers to generate a custom package.


Usage
----

This library includes a command line utility named `pystanley`, which can be used to retrieve and plot data from a Stanley archiver.

~~~~text
usage: linux-load-stanley-driver [-h] [-v] --url URL --username USERNAME
                                 [--ca-cert CA_CERT] --machine MACHINE

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        increase output
  --url URL            Stanley archiver URL
  --username USERNAME  Stanley archiver username
  --ca-cert CA_CERT    Custom certification authority certificate
  --machine MACHINE    Name of the current machine

Stanley password is read from environment variable STANLEY_PASSWORD
~~~~
