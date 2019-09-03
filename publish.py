from shared_vars import *
import asyncio
import aiormq
import json

async def on_message(message):
  print(f'[AIORMQ] Received message {message.body}')
  await asyncio.sleep(2) 
  print('[AIORMQ] An async operation completed')

async def main():
  data       = { 'data': 0 }
  connection = await aiormq.connect(URL)
  channel    = await connection.channel()

  """
  event_ex   = await channel.exchange_declare(
    exchange = 'events',
    exchange_type = 'fanout')

  anon_q = await channel.queue_declare(
    durable = True,
    auto_delete = True)
  """

  a_q = await channel.queue_declare(QUEUE_NAME)
  consume_ok = await channel.basic_consume(
    a_q.queue,
    on_message, # CB does not *need* to be an async method
    no_ack = True)

  async def on_interval():
    while True:
      data['data'] += 1
      await asyncio.sleep(1)
      print(f'[AIORMQ] Sending "{data}"')
      await channel.basic_publish(
        bytes(json.dumps(data), 'utf-8'),
        routing_key=QUEUE_NAME)

  loop = asyncio.get_event_loop()
  task = loop.create_task(on_interval())

  def stop_interval():
    print('[AIORMQ] Stopping task...')
    task.cancel()

  loop.call_later(10, stop_interval)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
