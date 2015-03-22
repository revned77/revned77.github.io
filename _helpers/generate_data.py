#!/usr/bin/env python3

"""Generates ../_data/metadata.json, ../_data/history.json, and any missing thumbnails."""

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

  metadata = {}
  history = {}

  for map in maps:
    path = '.' + unquote(maps[map]['path'])
    thumb_path = 'img/thumbs/%s.png' % map

    with Image.open(path) as im:
      width, height = im.size
      if not os.path.isfile(thumb_path):
        with im.convert() as th:
          print('thumbnailing ' + map)
          th.thumbnail((256, 256), Image.ANTIALIAS)
          th.save(thumb_path, 'PNG')
    with Image.open(thumb_path) as th:
      thumbnail_width, thumbnail_height = th.size

    metadata[map] = {
        'thumbnail': '/' + thumb_path,
        'size': os.path.getsize(path),
        'height': height,
        'width': width,
        'thumbnail_height': thumbnail_height,
        'thumbnail_width': thumbnail_width,
        'date': next(git.iter_commits(paths=path)).committed_date}

    for commit in git.iter_commits(paths=path):
      if not commit.committed_date in history:
        history[commit.committed_date] = {
            'commit': commit.hexsha,
            'games': set(),
            'maps': set()}
      history[commit.committed_date]['games'].add(maps[map]['game'])
      history[commit.committed_date]['maps'].add(map)

  with open('_data/metadata.json', 'w') as f:
    f.write(json.dumps(metadata, sort_keys=True, indent=2))
  with open('_data/history.json', 'w') as f:
    f.write(json.dumps(history, sort_keys=True, indent=2,
        default=lambda o: sorted(list(o)) if isinstance(o, set) else o))


if __name__ == '__main__':
  main()
