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
  import logging
  import traceback
  
  for mix in mixes:
    try:
      mix.download()
    except Exception as e:
      logging.error(f'Failed to download track: https://www.youtube.com/watch?v={track["id"]}')
      traceback.print_exc()
