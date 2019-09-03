PHONY: pika aiormq

all: pika aiormq
pika: .2venv/bin/activate
	. $^; \
	python consume_2_7.py &

aiormq: .3venv/bin/activate
	. $^; \
	python publish.py &

.2venv/bin/activate:
	test -d .2venv || virtualenv .2venv
	. $@; \
	pip install --upgrade pip wheel; \
	pip install pika

.3venv/bin/activate:
	test -d .3venv || python3.7 -m venv .3venv
	. $@; \
	pip install --upgrade pip wheel; \
	pip install aiormq

clean:
	rm -rf .2venv .3venv
