from djmix.bootstrap import bootstrap
from djmix.config import *

__all__ = [
  'mixes',
  'tracks',
  'get_root',
  'set_root',
  'download',
]

mixes, tracks = bootstrap()


def download():
  for mix in mixes:
    mix.download()
