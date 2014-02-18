

.PHONY: test
test::
	python speech_parser/speech_parser_test.py
	python votes_parser/votes_parser.py
