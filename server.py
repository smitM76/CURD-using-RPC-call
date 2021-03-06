"""server implementation,
    listen for rpc call and return the response as per request
    refere rabbitmq rpc documentation for basic server implementation
"""
import pika
import queries as Q
import json
import logging
from LOGCONFIG.dict_config import config

logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

"""for externel rabbitmq service
       url = 'url'  # I have used https://www.cloudamqp.com/
       params = pika.URLParameters(url)
       # self.connection = pika.BlockingConnection(params) insted of
       # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
"""
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    """loading data recieved from rpc client
    """
    data = json.loads(str(body)[2:-1])
    print('Recieved -> {}'.format(data))

    # Display what request we got
    logger.info('Recieved -> {}'.format(data))

    # Inthis section as per client request calling the coresponding method which return desired output
    if data['method'] == 'GET':
        response = Q.display_data()
    elif data['method'] == 'POST':
        response = Q.insert_data(data['username'], data['comment'])

    elif data['method'] == 'PUT':
        response = Q.update_data(data['id'], data['username'], data['comment'])

    elif data['method'] == 'DELETE':
        response = Q.delete_data(data['id'])

    else:
        response = "wrong api"

    # sending response back to client
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

# works like loop keep listning for requestss
channel.basic_consume(on_request, queue='rpc_queue')
print(" [x] Awaiting RPC requests")
channel.start_consuming()
