#!/usr/bin/env python

import unittest
import maf.actions as actions
from speech_parser import parse

class SpeechParserTest(unittest.TestCase):
    def test_position_parsing(self):
        speech = "+1,9,10 -1,3,5 +3,4"
        self.assertEqual(parse(speech),
            [(actions.PLAY, 1),
             (actions.PLAY, 9),
             (actions.PLAY, 10),
             (actions.NOT_PLAY, 1),
             (actions.NOT_PLAY, 3),
             (actions.NOT_PLAY, 5),
             (actions.PLAY, 3),
             (actions.PLAY, 4)]
        )

        speech = "(3 4,5 6 | -3) (1 2|-1) (5,6|-2) (1-5 | -2) (1 | -1)"
        self.assertEqual(parse(speech),
            [(actions.SET, ([3, 4, 5, 6], -3)),
             (actions.SET, ([1, 2], -1)),
             (actions.SET, ([5, 6], -2)),
             (actions.SET, ([1, 2, 3, 4, 5], -2)),
             (actions.SET, ([1], -1))]
        )

    def test_check_parsing(self):
        speech = "c5,9 c10"
        self.assertEqual(parse(speech),
            [(actions.CHECK, 5),
             (actions.CHECK, 9),
             (actions.CHECK, 10)]
        )

    def test_nomination_parsing(self):
        speech = "n10,8,4 x8 x10,4 d4 n1"
        self.assertEqual(parse(speech),
            [(actions.NOMINATE, 10),
             (actions.NOMINATE, 8),
             (actions.NOMINATE, 4),
             (actions.CANCEL, 8),
             (actions.CANCEL, 10),
             (actions.CANCEL, 4),
             (actions.DENOMINATE, 4),
             (actions.NOMINATE, 1)]
        )

    def test_shot_parsing(self):
        speech = ">7 >4"
        self.assertEqual(parse(speech),
            [(actions.SHOT, 7), (actions.SHOT, 4)]
        )

    def test_not_voting_parsing(self):
        speech = "z1,2 z z3 (z10 1 10) (z?10)"
        self.assertEqual(parse(speech),
            [(actions.DO_NOT_VOTE, 1),
             (actions.DO_NOT_VOTE, 2),
             (actions.DO_NOT_VOTE, 0),
             (actions.DO_NOT_VOTE, 3),
             (actions.DO_NOT_VOTE, (10, [1, 10]))]
        )

    def test_sheriff_action_parsing(self):
        speech = "$ $++ $-+- $----"
        self.assertEqual(parse(speech),
            [(actions.SHERIFF, (0, None)),
             (actions.SHERIFF, (0, [(actions.PLAY, None),
                                         (actions.PLAY, None)])),
             (actions.SHERIFF, (0, [(actions.NOT_PLAY, None),
                                         (actions.PLAY, None),
                                         (actions.NOT_PLAY, None)])),
             (actions.SHERIFF, (0, [(actions.NOT_PLAY, None),
                                         (actions.NOT_PLAY, None),
                                         (actions.NOT_PLAY, None),
                                         (actions.NOT_PLAY, None)]))]
        )

    def test_sheriff_say_checks_parsing(self):
        speech = "($ +1,2 -3) ($ -1 -2)"
        self.assertEqual(parse(speech),
            [(actions.SHERIFF, (0, [(actions.PLAY, 1),
                                         (actions.PLAY, 2),
                                         (actions.NOT_PLAY, 3)])),
             (actions.SHERIFF, (0, [(actions.NOT_PLAY, 1),
                                         (actions.NOT_PLAY, 2)]))]
        )
        speech = 'n9 ($ +6)'
        self.assertEqual(parse(speech),
            [(actions.NOMINATE, 9),
             (actions.SHERIFF, (0, [(actions.PLAY, 6)]))]
        )

    def test_information_parsing(self):
        speech = "($$ -1,2) ($$ +2 +3 | 1)"
        self.assertEqual(parse(speech),
            [(actions.INFORMATION, (None, [(actions.NOT_PLAY, 1),
                                                (actions.NOT_PLAY, 2)])),
             (actions.INFORMATION, (1, [(actions.PLAY, 2),
                                             (actions.PLAY, 3)]))]
        )

    def test_who_is_sherif_parsing(self):
        speech = "($? (4:x) (5:-1,3)) $x ($x) x$"
        self.assertEqual(parse(speech),
            [(actions.SHERIFF, (4, actions.CANCEL)),
             (actions.SHERIFF, (5, [(actions.NOT_PLAY, 1),
                                         (actions.NOT_PLAY, 3)])),
             (actions.SHERIFF, (0, actions.CANCEL)),
             (actions.SHERIFF, (0, actions.CANCEL)),
             (actions.SHERIFF, (0, actions.CANCEL))]
        )

        alternative = "($? 4:(x) 5:(-1,3)) $x ($x) x$"
        self.assertEqual(parse(alternative), parse(speech))

    def test_doc_example_speech(self):
        speech = '+1,3 -7 n4 n7x7 (z?7) (z7 7) ($$ -7) z'
        self.assertEqual(parse(speech),
             [('+', 1), ('+', 3), ('-', 7),
              ('n', 4), ('n', 7), ('x', 7),
              ('z', (7, [7])),
              ('i', (None, [('-', 7)])),
              ('z', 0)]
        )


if __name__ == '__main__':
    unittest.main()
