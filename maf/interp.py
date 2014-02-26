#!/usr/bin/env python
# -*- coding: utf-8 -*-

import maf.game
import maf.actions
import maf.utils

import logging
import math

from StringIO import StringIO


class SpeechCallback(object):

    def __init__(self, coeff=0.6):
        self.factory = {
            maf.actions.PLAY: self._play,
            maf.actions.NOT_PLAY: self._not_play,
            maf.actions.SET: self._set
            }
        self._coeff = coeff

    @property
    def coeff(self):
        return self._coeff

    def __call__(self, action, player_num, data, state):
        if action in self.factory:
            return self.factory[action](player_num, data, state)
        return state

    def _play(self, player_num, players, state):
        logging.debug("{1} plays with: {0}".format(players, player_num))
        if isinstance(players, int):
            players = [players]
        for p in players:
            if p not in state.alive:
                continue
            cur = state.position[player_num - 1][p - 1]
            state.position[player_num - 1][p - 1] = self._update_position(cur)
        return state

    def _not_play(self, player_num, players, state):
        logging.debug("{1} not plays with: {0}".format(players, player_num))
        if isinstance(players, int):
            players = [players]
        for p in players:
            if p not in state.alive:
                continue
            cur = 1 - state.position[player_num - 1][p - 1]
            state.position[player_num - 1][p - 1] = 1 - self._update_position(cur)
        return state

    def _set(self, player_num, data, state):
        if data[1] > 0:
            data[1] += -len(data[0])
        logging.debug("{0} thinks what in {1} {2} black players" \
                      .format(player_num, data[0], -data[1]))
        save_coeff = self._coeff
        self._coeff *= -data[1] / float(len(data[0]))
        logging.debug("Change coeff to {0}".format(self._coeff))
        self._not_play(player_num, data[0], state)
        self._coeff = save_coeff
        return state

    def _update_position(self, cur):
        return cur + self.coeff * (1 - cur)


def print_pmatrix(mat):
    buf = StringIO()
    for num, row in enumerate(mat):
        print >>buf, "\n[" if num == 0 else "\n ",
        print >>buf, "%2d:" % (num + 1, ),
        for n, r in enumerate(row):
            print >>buf, "[%.3f," % (r,) if n == 0 else \
                        ("%.3f," % (r,) if n + 1 != len(row) else \
                         "%.3f]"% (r)),
    print >>buf, ']'
    return buf.getvalue()


class GameState(object):
    """Players position and alive players container."""
    def __init__(self):
        self._positions = [[0.5 if i != j else 1. for i in range(10)] \
                           for j in range(10)]
        self._alive = set(i + 1 for i in range(10))

    @property
    def position(self):
        return self._positions

    @property
    def alive(self):
        return self._alive

    def kill(self, num):
        self._alive.remove(num)

    def __repr__(self):
        return "<GamePosition:\n" + maf.utils.str_pmatrix(self.position) + '>'



class GameInterpretor(object):
    def __init__(self, game, callback=SpeechCallback()):
        self._state = GameState()
        self._game = game
        self._now = {'lap': 0, 'player': 0} # (now lap, now speech)
        self._callback = callback

    @property
    def game(self):
        return self._game

    @property
    def state(self):
        return self._state

    @property
    def now(self):
        return self._now

    def step(self):
        """Move to the next game step. Change and return state."""
        for lap in self.game.laps:
            self.now['lap'] += 1
            self.now['speech'] = 0
            for p, speech in lap.speechs:
                self.now['speech'] += 1
                for action, data in speech.actions:
                    self._callback(action, p, data, self.state)
                    yield self.state

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
