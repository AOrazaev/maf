#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import actions as actions
import util.collection as CU
import util.strings as SU
import speech_parser
import votes_parser


class PlayerSpeech(object):
    """Player speech container.

    For constructing from string use `fromStr` method:
        >>> speech = PlayerSpeech.from_str("+1,2 -4 z $x")

    Then you can see player speech actions:
        >>> speech.actions
        [('+', 1), ('+', 2), ('-', 4), ('z', 0), ('$', (0, 'x'))]
    """
    def __init__(self):
        self._actions = []

    @staticmethod
    def from_str(s):
        """Constructs PlayerSpeech from str."""
        logging.debug("Parsing speech: {0}".format(s))
        if s is None:
            return PlayerSpeech()
        if s == 0:
            return PlayerSpeech()

        if isinstance(s, int):
            s = str(s) if s < 0 else '+' + str(s)

        ps = PlayerSpeech()
        ps._actions = speech_parser.parse(s)
        logging.debug("Parsing speech result: {0}".format(ps.actions))
        return ps

    @property
    def actions(self):
        return self._actions

    def __repr__(self):
        return self.actions.__repr__()


class Voting(object):
    """Game voting containter.

    Contains votes in voting order, and players speech in crash if
    present.

    For constructing votings use `from_list` function:
        >>> v = [
        ...   {'votes': [{3:'4-6'}, {6:'1 2,7'}, {7:'3 8 9'}, {'1,4,9': 0}],
        ...    'crash': [{3:'-4,5,6 +8'}, {6:'z'}, {7:'z -6 >6'}]},
        ...   {'votes': [{3:'1-10'}, {'6,7': 0}]}
        ... ]
        >>> vs = Voting.from_list(v)
        >>> vs
        [<Voting>, <Voting>]

    Now you can access to votings properties like `votes`:
        >>> vs[0].votes[:3]
        [(3, [4, 5, 6]), (6, [1, 2, 7]), (7, [3, 8, 9])]
        >>> vs[0].votes[3:]
        [(1, []), (4, []), (9, [])]
        >>> vs[1].votes
        [(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), (6, []), (7, [])]


    and `crash`:
        >>> vs[0].crash[0]
        (3, [('-', 4), ('-', 5), ('-', 6), ('+', 8)])
        >>> vs[0].crash[1:]
        [(6, [('z', 0)]), (7, [('z', 0), ('-', 6), ('>', 6)])]
        >>> vs[1].crash
        []

    Sometimes you can see special player number `both`:
        >>> v = [{1: '6-10'}, {6: '1-5'}, {'both': '2,4 5'}]
        >>> vs = Voting.from_list(v)[0]
        >>> vs.votes[:2]
        [(1, [6, 7, 8, 9, 10]), (6, [1, 2, 3, 4, 5])]
        >>> vs.votes[2] == (Voting.BOTH, [2, 4, 5])
        True
    """

    BOTH = 777

    def __init__(self):
        self._votes = []
        self._crash = []

    @property
    def votes(self):
        return self._votes

    @property
    def crash(self):
        return self._crash

    @staticmethod
    def from_list(l):
        """:returns: constructed list of votes from given voting list."""
        votings = []
        for v in l:
            if 'votes' in v:
                current = Voting()
                current._votes = Voting._parse_votes(v['votes'])
                if 'crash' in v:
                    current._crash = Voting._parse_crash(v['crash'])
                votings.append(current)
            else:
                current = Voting()
                current._votes = Voting._parse_votes(l)
                return [current]
        return votings

    def __repr__(self):
        return "<Voting>"

    @staticmethod
    def _parse_votes(votes):
        voting = []
        for v in votes:
            item = CU.undict(v)
            if SU.ci_equals(item[0], 'both'):
                item = (Voting.BOTH, item[1])
            players = (int(y.strip()) for x in str(item[0]).split(',') \
                       for y in x.split())
            hands = [hand for hand in votes_parser.parse(item[1]) if hand]
            voting.extend(((player, hands) for player in players))
        return voting

    @staticmethod
    def _parse_crash(c):
        speechs = (CU.undict(speech) for speech in c)
        return [(player, PlayerSpeech.from_str(speech)) \
                for player, speech in speechs]


class GameLap(object):
    """Content one game cycle: day speechs, voting and night after the day.

    For GameLap construction use `from_dict` constructing function:
        >>> dlap = {
        ...     'day': [
        ...         {8: 0},
        ...         {6: '-1 n1 -3 (1 3 | -2) -4'},
        ...         {7: '-1 +6'},
        ...         {9: '-1,3,4'},
        ...         {1: 'n9 ($ +6)'}],
        ...     'voting': [{'votes': [{1: '6 7 9'}, {9: 1}]}]
        ... }
        >>> lap = GameLap.from_dict(dlap)

    Now you can access to lap properties:
        >>> lap.speechs[1]
        (6, [('-', 1), ('n', 1), ('-', 3), ('s', ([1, 3], -2)), ('-', 4)])
        >>> lap.speechs[2:4]
        [(7, [('-', 1), ('+', 6)]), (9, [('-', 1), ('-', 3), ('-', 4)])]
        >>> lap.votings[0].votes
        [(1, [6, 7, 9]), (9, [1])]
        >>> lap.night
        {}
        >>> lap.dead
        []
    """
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

    @staticmethod
    def from_dict(d):
        """Constructs GameLap from dict"""
        logging.debug("Parsing day: {0}".format(d.keys()))
        lap = GameLap()
        lap._speechs = GameLap._parse_speechs(d.get('day', []))
        lap._votings = Voting.from_list(d.get('voting', []))
        lap._night_actions = d.get('night', {})
        lap._dead = []
        for p_sp in d.get('dead', []):
            logging.debug("Parsing dead: {0}".format(p_sp))
            p, sp = CU.undict(p_sp)
            lap._dead.append((p, PlayerSpeech.from_str(sp)))

        return lap

    @staticmethod
    def _parse_speechs(speechs):
        result = []
        for s in speechs:
            speech = CU.undict(s)
            result.append((speech[0], PlayerSpeech.from_str(speech[1])))

        return result


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

    @property
    def club(self):
        return self._club

    @property
    def locality(self):
        return self._locality

    @property
    def end(self):
        return self._end

    @staticmethod
    def from_yaml(game):
        """:returns: MafGame object created from parsed yaml game dict."""
        mg = MafGame()
        mg._locality = game.get('locality', None)
        logging.debug("Game locality: {0}".format(mg.locality))
        mg._date = game.get('date')
        logging.info("Game date: {0}".format(mg.date))
        mg._club = game.get('club')
        logging.info("Game club: {0}".format(mg.club))
        mg._players = game.get('players', [])
        logging.debug("Game players: {0}".format(CU.strlist(mg.players)))
        mg._roles = game.get('roles', {})
        logging.debug("Game roles: {0}".format(mg.roles))
        mg._end = game.get('laps', [{'end': None}])[-1]['end'].lower()
        logging.info("Game wins: {0}".format(mg.end))

        logging.info("Start parsing laps...")
        mg._laps = [GameLap.from_dict(lap) for lap in game['laps'][:-1]]

        return mg


if __name__ == '__main__':
    import doctest
    doctest.testmod()
