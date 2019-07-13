import logging

from pew3wm import pew3wm as mut


log = logging.getLogger(__name__)


def test_sanity():
    assert True


def test_path_finder():
    log.debug("testing")
    path = mut.find_pew_pew_path()
    print(f'Path is {path}')
    assert ['test'] == mut.find_pew_pew_path
