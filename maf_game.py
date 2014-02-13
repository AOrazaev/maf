#!/usr/bin/env python

import logging


class PlayerSpeech(object):
    """Player speech container."""

    PLAY = '+'
    NOT_PLAY = '-'
    SHERIFF = '$'
    SHOT = '>'
    NOMINATE = 'n'
    DENOMINATE = 'd'
    CANCEL = 'x'
    DO_NOT_VOTE = 'z'
    CHECK = 'c'
    INFORMATION = 'i'
    SET = 's'

    def __init__(self):
        self._actions = []

    @classmethod
    def fromStr(s):
        raise NotImplementedError()


class GameLap(object):
    """Content one game cycle: day speechs, voting and night after the day."""
    def __init__(self, **kwargs):
        self._speechs = kwargs.get('speechs', [])
        self._votings = kwargs.get('votings', [])
        self._night_actions = kwargs.get('night', {})
        self._dead = kwargs.get('dead', [])

    @property
    def speechs(self):
        return self._speechs

    @property
    def votings(self):
        return self._votings

    @property
    def night(self):
        return self._night_actions

    @property
    def dead(self):
        return self._dead


class MafGame(object):
    """Contains log of mafia game."""
    def __init__(self, **kwargs):
        self._laps = kwargs.get('laps', [])
        self._players = kwargs.get('players', [])
        self._roles = kwargs.get('roles', [])
        self._end = kwargs.get('end', None)
        self._date = kwargs.get('date', None)
        self._club = kwargs.get('club', None)
        self._locality = kwargs.get('locality', None)

    @property
    def laps(self):
        return self._laps

    @property
    def players(self):
        return self._players

    @property
    def roles(self):
        return self._roles

    @property
    def end(self):
        return self._end

    @property
    def date(self):
        return self._date

    @classmethod
    def fromYamlDict(game):
        """:returns: MafGame object created from parsed yaml game dict."""
        pass
