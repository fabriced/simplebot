all:
	@python src/main.py

clean:
	@find src -name '*.pyc' -exec rm -f '{}' \;

