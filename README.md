# AMPQ Consumer / Producer library examples

## aiormq

_TLDR:_ Use _aiormq_ for `async / await` on Python 3.5+.

The _aiormq_ library is a pure Python AMQP asynchronous client library. The
client apis closely resemble _pika_. Its preferred over _pika_ on Python 3.5+
because it is designed with async/await support and _pika_ only supports async
via callbacks.

## pika

Pika is basically the only decent client library for Python period. It also
might be a Pokémon reference.

## References

- [See aiormq on github](https://github.com/mosquito/aiormq/)
- [See pika on github](https://github.com/pika/pika)
- [Pika tornado adapter](https://pika.readthedocs.io/en/stable/examples/tornado_consumer.html)
