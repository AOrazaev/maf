#!/usr/bin/env python

from maf_game import PlayerSpeech

from ply import lex
from ply import yacc
import re

tokens = (
    'PLUS',
    'MINUS',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'LINE',
    'SHOT',
    'CANCEL',
    'NOMINATE',
    'DENOMINATE',
    'DO_NOT_VOTE',
    'CHECK',
    'DIGIT',
    'COMMA',
    'DOLLAR',
    'QUESTION',
    'DDOT'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_OPEN_BRACE = r'\('
t_CLOSE_BRACE = r'\)'
t_LINE = r'\|'
t_SHOT = r'>'
t_CANCEL = r'[xX]'
t_NOMINATE = r'[nN]'
t_DENOMINATE = r'[dD]'
t_DO_NOT_VOTE = r'[zZ]'
t_CHECK = r'[cC]'
t_COMMA = r','
t_DOLLAR = r'\$'
t_QUESTION = r'\?'
t_DDOT = r':'

t_ignore = r' '

def t_DIGIT(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

def p_speech(p):
    """
    speech :
    speech : action speech
    """
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] if isinstance(p[1], list) else [p[1]]
        p[0].extend(p[2])

def p_action(p):
    """
    action : position
    action : sheriff
    action : CHECK player_comma_list
    action : NOMINATE player_comma_list
    action : CANCEL player_comma_list
    action : CANCEL DOLLAR
    action : DENOMINATE DIGIT
    action : SHOT DIGIT
    action : DO_NOT_VOTE player_comma_list
    action : OPEN_BRACE brace_action CLOSE_BRACE
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1].lower() in (PlayerSpeech.CHECK, PlayerSpeech.CANCEL,
                PlayerSpeech.NOMINATE, PlayerSpeech.DO_NOT_VOTE):
            if p[2] == PlayerSpeech.SHERIFF:
                p[0] = [(PlayerSpeech.SHERIFF, (0, PlayerSpeech.CANCEL))]
            else:
                p[0] = [(p[1].lower(), num) for num in p[2]]
        else:
            p[0] = (p[1].lower(), p[2])
    else:
        p[0] = p[2]

def p_sheriff(p):
    """
    sheriff : DOLLAR
    """
    p[0] = [('$', (0, None))]

def p_position(p):
    """
    position : PLUS player_comma_list
    position : MINUS player_comma_list
    """
    p[0] = []
    for player in p[2]:
        p[0].append((p[1], player))

def p_position_list(p):
    """
    position_list : position
    position_list : position position_list
    """
    p[0] = p[1]
    if len(p) > 2:
        p[0].extend(p[2])

def p_sign_list(p):
    """
    sign_list : MINUS
    sign_list : MINUS sign_list
    sign_list : PLUS
    sign_list : PLUS sign_list
    """
    p[0] = [(p[1], None)]
    if len(p) > 2:
        p[0].extend(p[2])

def p_player_comma_list(p):
    """
    player_comma_list : DIGIT
    player_comma_list : DIGIT COMMA player_comma_list
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]]
        p[0].extend(p[3])

def p_player_list(p):
    """
    player_list : player_comma_list
    player_list : player_comma_list player_list
    """
    p[0] = p[1]
    if len(p) > 2:
        p[0].extend(p[2])

def p_brace_action(p):
    """
    brace_action : DOLLAR sign_list
    brace_action : DOLLAR position_list
    brace_action : DOLLAR CANCEL
    brace_action : DOLLAR DOLLAR position_list
    brace_action : DOLLAR DOLLAR position_list LINE DIGIT
    brace_action : DOLLAR QUESTION sheriff_list
    brace_action : DO_NOT_VOTE DIGIT player_list
    brace_action : DO_NOT_VOTE QUESTION DIGIT
    brace_action : player_list LINE MINUS DIGIT
    brace_action : player_list LINE PLUS DIGIT
    """
    if len(p) == 3:
        if isinstance(p[2], list):
            p[0] = [(PlayerSpeech.SHERIFF, (0, p[2]))]
        else:
            p[0] = [(PlayerSpeech.SHERIFF, (0, PlayerSpeech.CANCEL))]
    elif len(p) == 4:
        if p[1] == PlayerSpeech.SHERIFF and p[2] == '?':
            p[0] = p[3]
        elif p[2] == PlayerSpeech.SHERIFF:
            p[0] = [(PlayerSpeech.INFORMATION, (None, p[3]))]
        elif p[1] == PlayerSpeech.DO_NOT_VOTE and p[2] == '?':
            p[0] = [] # Do not record questions about voting
        else:
            p[0] = [(PlayerSpeech.DO_NOT_VOTE, (p[2], p[3]))]
    else:
        if p[4] == '|':
            p[0] = [(PlayerSpeech.INFORMATION, (p[5], p[3]))]
        else:
            decision = int("{0}{1}".format(p[3],p[4]))
            p[0] = [(PlayerSpeech.SET, (p[1], decision))]


def p_sheriff_list(p):
    """
    sheriff_list : sheriff_in_list_position
    sheriff_list : sheriff_in_list_position sheriff_list
    """
    p[0] = [(PlayerSpeech.SHERIFF, p[1])]
    if len(p) > 2:
        p[0].extend(p[2])

def p_sheriff_in_list_position(p):
    """
    sheriff_in_list_position : OPEN_BRACE DIGIT DDOT position_list CLOSE_BRACE
    sheriff_in_list_position : OPEN_BRACE DIGIT DDOT CANCEL CLOSE_BRACE
    """
    p[0] = (p[2], p[4].lower() if isinstance(p[4], str) else p[4])


yacc.yacc()


def parse(speech):
    sheriff_dont_say_checks = re.compile('(^| )\$([-\+]+)($| )')
    processed = speech
    while sheriff_dont_say_checks.search(processed):
        processed = sheriff_dont_say_checks.sub('\g<1>($\g<2>)\g<3>',
                                                processed)
    processed = re.sub(r'(^| )\$x($| )', '\g<1>($x)\g<2>', processed)
    processed = re.sub(r'(^| )\z($| )', '\g<1>z0\g<2>', processed)
    return yacc.parse(processed)

