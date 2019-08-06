Setting up py3status-pewpew on Ubuntu 16.04
===========================================
Approximate steps on how to install py3status-pewpew:

    (add deadsnakes PPA)
    sudo apt-get install python3.6 python3.6-venv python 3.6-dev
    mkdir ~/.venvs
    cd ~/.venvs
    python3 -m venv py3status-env
    source py3status-env/bin/activate
    pip install --upgrade pip
    pip install py3status evdev pyserial
    git clone https://github.com/obestwalter/py3status-pewpew
    cd py3status-pewpew
    python setup.py install
    cd ~/bin
    ln -s ~/.venvs/py3status-env/bin/py3status
    usermod -a -G input `whoami`
    usermod -a -G dialout `whoami`
    (logout and in again, plug in pewpew and power up!)

