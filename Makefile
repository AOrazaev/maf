SET_PYTHONPATH := PYTHONPATH=$(PWD)

.PHONY: test
test::
	$(SET_PYTHONPATH) python speech_parser/speech_parser_test.py
	$(SET_PYTHONPATH) python votes_parser/votes_parser.py
