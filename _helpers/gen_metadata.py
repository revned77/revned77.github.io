#!/usr/bin/env python3

"""Populates ../_data/metadata.json with any missing entries, also generating thumbnails."""

import json
import os

from copy import deepcopy
from git import Repo
from PIL import Image
from urllib.parse import unquote


def main():
  git = Repo('.')
  with open('_data/maps.json', 'r') as f:
    maps = json.loads(f.read())
  with open('_data/metadata.json', 'r') as f:
    current = json.loads(f.read())

  results = deepcopy(current)

  for map in {m: maps[m] for m in maps if m not in current}:
    print('processing ' + map)

    path = '.' + unquote(maps[map]['path'])
    thumb_path = 'img/thumbs/%s.png' % map

    with Image.open(path) as im:
      width, height = im.size
      th = im.convert()
      th.thumbnail((256, 256), Image.ANTIALIAS)
      th.save(thumb_path, 'PNG')
      th.close()
    date = next(git.iter_commits(paths=path)).committed_date

    results[map] = {
      'thumbnail': '/' + thumb_path,
      'size': os.path.getsize(path),
      'height': height,
      'width': width,
      'date': date}

  with open('_data/metadata.json', 'w') as f:
    f.write(json.dumps(results, sort_keys=True, indent=2))


if __name__ == '__main__':
  main()
