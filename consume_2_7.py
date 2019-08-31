import pika
from shared_vars import *

# Defaults to connect with guest:guest on port 5672 on the default VHOST "/"
connection = pika.BlockingConnection(pika.URLParameters(URL))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

def callback(ch, method, properties, body):
  # Do stuff put data in our "database" here, once its saved in our database
  # we can *ack* the message and tell the broker its successfully consumed.
  print(" [x] Received %r" % body)
  ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(
  queue=QUEUE_NAME,
  # auto_ack=True causes message ack before the callback is invoked.
  # This is not ideal for prod-systems consuming from enduring & persistant
  # queues because the message may be lost if an application error occurs.
  # A preferable method is to manually ack with channel.basic_ack(...) in the
  # on_message_callback. A decorator to provide that behavior is ideal.
  auto_ack=False,
  on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
print('Blocked above this line - this wont print...')
