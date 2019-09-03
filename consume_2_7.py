import pika
from shared_vars import *
from time import sleep

# Defaults to connect with guest:guest on port 5672 on the default VHOST "/"
connection = pika.BlockingConnection(pika.URLParameters(URL))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

def callback(ch, method, properties, body):
  # Do stuff put data in our "database" here, once its saved in our database
  # we can *ack* the message and tell the broker its successfully consumed.
  print("[PIKA] Received %r" % body)
  # If a synchronous thing happens here we still get messages - we just wont
  # process them - so its a good idea to ACK after all the work is complete.
  # because we do not want to ack something then have the program crash.
  sleep(4)
  print("[PIKA] Work done...")
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

print('[PIKA] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
