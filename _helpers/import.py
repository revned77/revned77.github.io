#!/usr/bin/env python3

"""Creates preliminary entries in ../_data/maps.json for files in ../maps."""

import glob
import json
import re
import unicodedata


def main():
  with open('_data/maps.json', 'r') as f:
    maps = json.loads(f.read())

  map_paths = [ unicodedata.normalize('NFC', maps[map_id]['path']) for map_id in maps ]
  game_ids_by_name = {
      get_game_from_map_path(maps[map_id]['path']): maps[map_id]['game'] for map_id in maps }

  all_paths=map(lambda p: unicodedata.normalize('NFC', '/' + p), glob.glob('maps/*/*.png'))

  for path in set(all_paths).difference(map_paths):
    print('importing ' + path)
    game = get_game_from_map_path(path)
    entry = {
      'game': game_ids_by_name.get(game, slugify(game)),
      'name': re.sub('.*/', '', re.sub('\.png$', '', path)),
      'path': path,
    }
    maps[entry['game'] + '-' + slugify(entry['name'])] = entry

  with open('_data/maps.json', 'w') as f:
    f.write(json.dumps(maps, sort_keys=True, indent=2, ensure_ascii=False))


def get_game_from_map_path(map_path):
  return re.sub('/.*', '', re.sub('^/?maps/', '', map_path))


def slugify(s):
  return re.sub('[^a-z0-9-]', '', re.sub('[ -]+', '-', s.lower()))


if __name__ == '__main__':
  main()
