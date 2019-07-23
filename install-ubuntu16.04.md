Setting up py3status-pewpew on Ubuntu 16.04
===========================================

1. add deadsnakes PPA
2. install packages:
    python3.6 python3.6-venv python 3.6-dev
3. mkdir ~/.venvs && cd ~/.venvs
4. python3 -m venv py3status-env
5. source py3status-env/bin/activate
6. pip install --upgrade pip
7. pip install py3status evdev pyserial
8. git clone https://github.com/obestwalter/pew3wm
9. cd pew3wm
10. python setup.py install
11. cd ~/bin
12. ln -s ~/.venvs/py3status-env/bin/py3status
