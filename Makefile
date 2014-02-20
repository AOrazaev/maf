SET_PYTHONPATH := PYTHONPATH=$(PWD)

.PHONY: test clean

test::
	$(SET_PYTHONPATH) python util/collection.py
	$(SET_PYTHONPATH) python util/strings.py
	$(SET_PYTHONPATH) python speech_parser/speech_parser_test.py
	$(SET_PYTHONPATH) python votes_parser/votes_parser.py
	$(SET_PYTHONPATH) python game/game.py

clean::
	echo "Cleaning project"
	find . -name '*.pyc' -delete
	find . -name 'parser.out' -delete
	find . -name 'parsetab.py' -delete
