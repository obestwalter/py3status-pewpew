[![Travis CI status](https://api.travis-ci.org/obestwalter/py3status-pewpew.png)](https://travis-ci.org/obestwalter/py3status-pewpew)
[![PyPI version](https://badge.fury.io/py/i3configger.svg)](https://pypi.org/project/i3configger/)

# py3status-pewpew

A [py3status](https://github.com/ultrabug/py3status) module turning the [PewPew](https://pewpew.readthedocs.io) into a controller and external workspace display for the [i3wm](https://i3wm.org/) tiling window manager.

[![Watch a short demo video](http://img.youtube.com/vi/0Oy2CE2GZ7s/0.jpg)](http://www.youtube.com/watch?v=0Oy2CE2GZ7s "py3status-pewpew status controller")

Extend i3 with your PewPew. Use the buttons to send messages to i3 (or do whatever else you like) and always see which workspace you are on.

## install

```text
pip install py3status-pewpew
```

See install-ubuntu16.04.md for specific instructions on that distribution.

# testing

run the tests with tox:

```console
$ cd </path/to/this/repo>
$ tox
```

## development

install a development environment:

```console
$ cd </path/to/this/repo>
$ tox -e dev
```

... and activate it e.g via `source .tox/dev/bin/activate`. Then run tests with `pytest`.

Debugging hint - use screen to get direct access and run commands in the REPL:

    $ screen /dev/ttyACM0

This will open a screen session. Ctrl+C and Enter is useful to soft reboot pewpew in there.
