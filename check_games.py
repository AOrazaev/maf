#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse given yaml files with game logs."""

import maf

import sys
import yaml
import logging

def game_from_yaml(f):
    """:returns: game.MafGame list from file @f"""
    data = yaml.load(f)
    num = 1
    for g in data:
        logging.info("Start loading game {0}...".format(num))
        yield maf.MafGame.from_yaml(g['game'])
        num += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Error: you must set file with games"
        print >>sys.stderr, "Usage:", sys.argv[0], "<GAME_LOGS_IN_YAML_FORMAT>"
        sys.exit(1)

    if len(sys.argv) < 3:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)
    logging.info("Loading games from: {0}".format(sys.argv[1]))

    games = []
    with open(sys.argv[1], 'rb') as f:
        games = list(game_from_yaml(f))

    print games
