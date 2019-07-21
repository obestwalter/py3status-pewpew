[![Travis CI status](https://api.travis-ci.org/obestwalter/pew3wm.png)](https://travis-ci.org/obestwalter/pew3wm)

# pew3wm

A [py3status](https://github.com/ultrabug/py3status) module turning the [PewPew](https://pewpew.readthedocs.io) into a controller and external workspace display for the [i3wm](https://i3wm.org/) tiling window manager.

[![Watch a short demo video](http://img.youtube.com/vi/0Oy2CE2GZ7s/0.jpg)](http://www.youtube.com/watch?v=0Oy2CE2GZ7s "pew3wm status controller")

Extend i3 with your PewPew. Use the buttons to send messages to i3 (or do whatever else you like) and always see which workspace you are on.

## install

We hope to do a release on PyPi soon, but at the moment, clone repo and `tox -e deploy` :)

Make sure your user is part of the 'input' and 'dialout' groups if you are on Ubuntu, this is for evdev to be able to read the buttons:

    $ sudo usermod -a -G dialout `whoami`
    $ sudo usermod -a -G input `whoami`
    $ groups   # should return list containing both groups; logout to apply changes

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

    $ screen /dev/ttyACM0   # open a screen session. May need to reboot and/or hit Ctrl+C if are not greeted by a welcome message
