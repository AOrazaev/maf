#!/usr/bin/env python
"""Console application for logging and analizing maf game."""

import argparse
import textwrap
import logging
import cmd2 as cmd
import sys

from collections import deque

import maf

VERSION = 0.1

class MafGameAnalizerApp(cmd.Cmd):
    multilineCommands = ['sp', 'spe', 'spee', 'speec', 'speech']
    prompt = '[mga]>>> '
    continuation_prompt = '... '
    intro = textwrap.dedent('''
        MGA -- maf game analizer console application for
        logging and analize maf games.

        Version: {0}

        All questions you may send to mga.app@ya.ru
        Copyright 2014 Aman Orazaev.

    ''').format(VERSION)

    def __init__(self):
        cmd.Cmd.__init__(self)
        self._interpretor = maf.interp.GameInterpretor()
        self._players_on_table = deque(self._interpretor.state.alive)
        self._lap = 0
        self._next_speech = 0
        self._next_crash = 0
        self._dead_speech = deque()
        self._first_voting = True

    def _cur_player(self):
        return self._dead_speech[0] if self._dead_speech \
               else self._players_on_table[self._next_speech]

    def _kill(self, num):
        try:
            num = int(num)
            if num not in self._players_on_table:
                raise LookupError("No player {0} on table, can't kill".format(num))
        except ValueError:
                raise LookupError("No player {0} on table, can't kill".format(num))
        self._interpretor.kill(num)
        self._players_on_table.remove(num)

    def help_quit(self):
        print textwrap.dedent('''
            q[uit]
            ex[it]
                    quit from maf-game-analizer
            ''')
    help_exit = help_q = help_quit

    def _is_next_lap(self):
        return self._next_speech == 0

    def _check_is_speech_now(self):
        if self._interpretor.state.nominated \
           and self._is_next_lap():
               raise RuntimeError("Error: Can't accept next speech, becouse"
                       " there must be voting now!\n")

    def _interp_speech(self, current_player, speech):
        logging.debug("Start accepting speech No {0}\n".format(current_player))
        self._interpretor.interp_speech(current_player, speech)
        print "Speech No {0} accepted\n".format(current_player)


    def do_speech(self, speech):
        self._check_is_speech_now()
        self._first_voting = True
        current_player = self._cur_player()
        self._interp_speech(current_player, speech)

        if not self._dead_speech:
            self._next_speech += 1
            if self._next_speech == len(self._players_on_table):
                self._next_speech = 0
                self._players_on_table.rotate(-1)
                self._lap += 1
        else:
            self._dead_speech.popleft()


    def help_speech(self):
        print textwrap.dedent('''
            sp[eech] <ACTIONS>
                    Writes next player speech.
            ''')

    def do_now(self, line):
        if self._is_next_lap() and self._interpretor.state.nominated:
            print "Lap #{0}".format(self._lap - 1)
            print "Now is voting."
        else:
            print "Lap #{0}".format(self._lap)
            if not self._dead_speech:
                print "Now is speech No {0}".format(self._cur_player())
            else:
                print "Now is last speech of No {0}".format(self._dead_speech)
        print "There are {0} players on table".format(
                list(self._players_on_table))
        print "Nominated: {0}\n".format(self._interpretor.state.nominated)

    def help_now(self):
        print textwrap.dedent('''
            now
                    print current game situation.
            ''')

    def do_dead(self, players):
        for player in players.split():
            try:
                self._kill(player)
                self._dead_speech.append(player)
            except LookupError as le:
                print le
                return

    def help_dead(self):
        print textwrap.dedent('''
            dead <P_0> <P_1> ...
                    kill players No P_0, P_1, etc.
        ''')

    def _nominated_just_one_player(self, nominated):
        if len(nominated) != 1:
            return False

        print "There was just on nominated player No {0}".format(nominated[0])
        if self._lap == 1:
            print "But it is first day. No dead players."
        else:
            print "Dead No {0}".format(nominated[0])
            self._dead_speech.append(nominated[0])
            self._kill(nominated[0])
        return True

    def _check_is_time_for_voting(self):
        if self._next_speech != 0 or self._dead_speech:
            raise RuntimeError("Error: Can't do voting now.\n"
                    "There are players who are not talking in this lap.\n")

    def _vote_for_both(self):
        votes = raw_input('... both: ')
        votes = maf.Voting._parse_votes([{maf.Voting.BOTH: votes}])[0][1]
        votes = [v for v in votes if v in self._players_on_table]
        logging.debug("Votes for both: {0}".format(votes))

        return len(votes) * 2 > len(self._players_on_table)

    def _update_nominated(self, voting):
        def cmp_votes(x, y):
            if len(x[1]) == len(y[1]):
                return 0
            return 1 if len(x[1]) > len(y[1]) else -1
        voting.sort(cmp=cmp_votes, reverse=True)
        new_nominated = [p for p, h in voting if len(h) == len(voting[0][1])]
        logging.debug("Max hands for players No {0}".format(new_nominated))

        if new_nominated == self._interpretor.state.nominated \
           and not self._first_voting:
            if self._vote_for_both():
                for p in self._interpretor.state.nominated:
                    self._kill(p)
                    self._dead_speech.append(p)
            self._interpretor.state.nominated = []
            return

        if len(new_nominated) == 1:
            self._kill(new_nominated[0][1])
            self._dead_speech.append(p)
            self._interpretor.state.nominated = []
            return

        logging.debug("Crash, update nominated")
        self._first_voting = False
        self._interpretor.state.nominated = [
                n for n in self._interpretor.state._nominated
                if n[1] in new_nominated]

    def do_autovoting(self, line):
        self._check_is_time_for_voting()
        nominated = self._interpretor.state.nominated
        if not nominated:
            return

        print 'Start voting!'
        if self._nominated_just_one_player(nominated):
            self._interpretor.state.nominated = []
            return

        votes = []
        for n in self._interpretor.state.nominated:
            hands = raw_input('... {0}: '.format(n))
            votes.append({n: hands})
        logging.debug("Accepted voting: {0}".format(votes))
        voting = maf.Voting._parse_votes(votes)
        voting = [(p, [h for h in hands if h in self._players_on_table]) \
                  for p, hands in voting]
        logging.debug("Parsed and alive voting {0}".format(voting))
        self._update_nominated(voting)

    def help_autovoting(self):
        print 'autovo[ting]'
        print '        Start voting on this lap'

    def do_debug(self, line):
        if line.strip() == 'off':
            logging.getLogger().setLevel(logging.ERROR)
            print 'Debug mode OFF\n'
        else:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug('Debug mode ON')

    def help_debug(self):
        print 'debug [on]|off'
        print '        On/off debug mode'



def main():
    MafGameAnalizerApp().cmdloop()


if __name__ == '__main__':
    main()
