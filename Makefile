all:
	@python src/simplebot.py

clean:
	@find src -name '*.pyc' -exec rm -f '{}' \;

