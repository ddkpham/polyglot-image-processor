from flask import Flask, request, jsonify
import pika
import uuid
import json
import os 



class DemoRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode('utf-8'))

    def call(self, arg):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        body = json.dumps(arg).encode('utf8')
        
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id),
            body=body)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


rpc = DemoRpcClient()

# Initialize app
app = Flask(__name__)

# Add routes 
@app.route('/', methods=['GET'])
def get():
  response = rpc.call({'string': 'hello darkness my old friend'})
  print(response['length'])
  return jsonify({'msg': 'Hello World', 'length': response['length']})

# Run Server
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)