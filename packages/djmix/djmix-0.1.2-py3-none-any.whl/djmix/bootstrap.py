import json
import logging
from pathlib import Path
from djmix import config
from .models import Mix


def bootstrap():
  logging.basicConfig(level=logging.INFO)
  
  package_path = Path(__file__).parent.parent.parent.resolve()
  metadata_path = package_path.joinpath('dataset/djmix-dataset.json')
  assert metadata_path.is_file(), f'djmix-dataset.json does not exist at: {metadata_path}'
  
  json_mixes = json.load(open(metadata_path))
  
  data_dir = config.get_root()
  mixes = [
    Mix(data_dir, **json_mix)
    for json_mix in json_mixes
  ]
  
  return mixes
