"""This module works as client, make rpc call to server.py
   this client can request for GET,POST,PUT,DELETE
   made use of argparser make it easy to understad input or uses
   -h [client.py -h] for help
"""
import pika
import uuid
import json
import logging
from logging.config import dictConfig
import argparse

"""for externel rabbitmq service
url = 'amqp://dszgrpet:Yw5yKoMZqINvp78V63Su7Svw02KyhCcX@dinosaur.rmq.cloudamqp.com/dszgrpet'
params = pika.URLParameters(url)
"""


class Rpc_client(object):
    """establish connection to rabbitmq running locally
       refere rabbitmq documentation for more details 
    """
    """for externel rabbitmq service
       url = 'url'  # I have used https://www.cloudamqp.com/
       params = pika.URLParameters(url)
       # self.connection = pika.BlockingConnection(params) insted of 
       # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    """
    def __init__(self):
        #self.connection = pika.BlockingConnection(params) 
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    """this is the same method you found on rabbitmq rpc tutorial
    """
    def call(self, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(data)) #user input goes here
        while self.response is None:
            self.connection.process_data_events()
        return self.response

#initialising argparser with basic operations

parser = argparse.ArgumentParser()
parser.add_argument('method', help='Select The Method',
                    choices=["GET", "POST", "PUT", "DELETE"])

# handles sub arguments
args, sub_args = parser.parse_known_args()

# setting values as message based on user input
if args.method == 'GET':
    msg = {
        "method": "GET"
    }

elif args.method == 'POST':
    parser = argparse.ArgumentParser()
    """adding following arguments runtime or when POST is input,
     to avoid complexity and the confusion of add argument with main options,
     these both are compulsory argument,
     preventing user to input null values 'LOL'
    """
    parser.add_argument('username', help='username', type=str)
    parser.add_argument('comment', help='comment', type=str)

    args = parser.parse_args(sub_args)
    u_name = args.username
    u_comment = args.comment

    # setting the payload with user input
    msg = {
        "method": "POST",
        "username": u_name,
        "comment": u_comment
    }

elif args.method == 'PUT':
    parser = argparse.ArgumentParser()
    """adding following arguments runtime or when PUT is input,
     to avoid complexity and the confusion of add argument with main options,
     making id as compulsory argument and --username and --comment as optional
     arguments
    """

    parser.add_argument('id', help='id', type=int)
    parser.add_argument('--username', help='username', type=str)
    parser.add_argument('--comment', help='comment', type=str)

    args = parser.parse_args(sub_args)
    u_id = args.id
    u_name = args.username
    u_comment = args.comment

    # setting the payload with user input
    msg = {
        "method": "PUT",
        "id": u_id,
        "username": u_name,
        "comment": u_comment
    }

elif args.method == "DELETE":
    """adding compulsory sub argument id
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id', type=int)
    args = parser.parse_args(sub_args)
    u_id = args.id

    # setting the payload with user input
    msg = {
        "method": "DELETE",
        "id": u_id
    }
else:
    print("Invalid option")

rpc = Rpc_client()
print(" [x] Requesting ")
# passing the user input as json
response = rpc.call(json.dumps(msg))
print(" [.] Got %r" % response)
