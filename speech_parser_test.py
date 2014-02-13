#!/usr/bin/env python

import unittest
from maf_game import PlayerSpeech
from speech_parser import parse

class SpeechParserTest(unittest.TestCase):
    def test_position_parsing(self):
        speech = "+1,9,10 -1,3,5 +3,4"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.PLAY, 1),
             (PlayerSpeech.PLAY, 9),
             (PlayerSpeech.PLAY, 10),
             (PlayerSpeech.NOT_PLAY, 1),
             (PlayerSpeech.NOT_PLAY, 3),
             (PlayerSpeech.NOT_PLAY, 5),
             (PlayerSpeech.PLAY, 3),
             (PlayerSpeech.PLAY, 4)]
        )

        speech = "(3 4,5 6 | -3) (1 2|-1) (5,6|-2)"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.SET, ([3, 4, 5, 6], -3)),
             (PlayerSpeech.SET, ([1, 2], -1)),
             (PlayerSpeech.SET, ([5, 6], -2))]
        )

    def test_check_parsing(self):
        speech = "c5,9 c10"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.CHECK, 5),
             (PlayerSpeech.CHECK, 9),
             (PlayerSpeech.CHECK, 10)]
        )

    def test_nomination_parsing(self):
        speech = "n10,8,4 x8 x10,4 d4 n1"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.NOMINATE, 10),
             (PlayerSpeech.NOMINATE, 8),
             (PlayerSpeech.NOMINATE, 4),
             (PlayerSpeech.CANCEL, 8),
             (PlayerSpeech.CANCEL, 10),
             (PlayerSpeech.CANCEL, 4),
             (PlayerSpeech.DENOMINATE, 4),
             (PlayerSpeech.NOMINATE, 1)]
        )

    def test_shot_parsing(self):
        speech = ">7 >4"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.SHOT, 7), (PlayerSpeech.SHOT, 4)]
        )

    def test_not_voting_parsing(self):
        speech = "z1,2 z z3 (z10 1 10) (z?10)"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.DO_NOT_VOTE, 1),
             (PlayerSpeech.DO_NOT_VOTE, 2),
             (PlayerSpeech.DO_NOT_VOTE, 0),
             (PlayerSpeech.DO_NOT_VOTE, 3),
             (PlayerSpeech.DO_NOT_VOTE, (10, [1, 10]))]
        )

    def test_sheriff_action_parsing(self):
        speech = "$ $++ $-+- $----"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.SHERIFF, (0, None)),
             (PlayerSpeech.SHERIFF, (0, [(PlayerSpeech.PLAY, None),
                                         (PlayerSpeech.PLAY, None)])),
             (PlayerSpeech.SHERIFF, (0, [(PlayerSpeech.NOT_PLAY, None),
                                         (PlayerSpeech.PLAY, None),
                                         (PlayerSpeech.NOT_PLAY, None)])),
             (PlayerSpeech.SHERIFF, (0, [(PlayerSpeech.NOT_PLAY, None),
                                         (PlayerSpeech.NOT_PLAY, None),
                                         (PlayerSpeech.NOT_PLAY, None),
                                         (PlayerSpeech.NOT_PLAY, None)]))]
        )

    def test_sheriff_say_checks_parsing(self):
        speech = "($ +1,2 -3) ($ -1 -2)"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.SHERIFF, (0, [(PlayerSpeech.PLAY, 1),
                                         (PlayerSpeech.PLAY, 2),
                                         (PlayerSpeech.NOT_PLAY, 3)])),
             (PlayerSpeech.SHERIFF, (0, [(PlayerSpeech.NOT_PLAY, 1),
                                         (PlayerSpeech.NOT_PLAY, 2)]))]
        )

    def test_information_parsing(self):
        speech = "($$ -1,2) ($$ +2 +3 | 1)"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.INFORMATION, (None, [(PlayerSpeech.NOT_PLAY, 1),
                                                (PlayerSpeech.NOT_PLAY, 2)])),
             (PlayerSpeech.INFORMATION, (1, [(PlayerSpeech.PLAY, 2),
                                             (PlayerSpeech.PLAY, 3)]))]
        )

    def test_who_is_sherif_parsing(self):
        speech = "($? (4:x) (5:-1,3)) $x ($x) x$"
        self.assertEqual(parse(speech),
            [(PlayerSpeech.SHERIFF, (4, 'x')),
             (PlayerSpeech.SHERIFF, (5, [(PlayerSpeech.NOT_PLAY, 1),
                                         (PlayerSpeech.NOT_PLAY, 3)])),
             (PlayerSpeech.SHERIFF, (0, 'x')),
             (PlayerSpeech.SHERIFF, (0, 'x')),
             (PlayerSpeech.SHERIFF, (0, 'x'))]
        )


if __name__ == '__main__':
    unittest.main()
