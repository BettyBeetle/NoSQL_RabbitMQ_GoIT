import pika
import json
from connect import connect
from model import Contact

connect('email_campaign', alias='email_campaign_alias')

def send_email_stub(contact_id):
    print(f" >>> Sending e-mail to contact with id {contact_id}")
    pass

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue', durable=True)

print(' [...] Waiting for messages. To exit press CTRL+C\n')


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    
    print(f" [x] Received {message}")
   
    contact_id = message['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email_stub(contact_id)
        
        contact.sent_email = True
        contact.save()
        
        print(f" [v] Email to {contact_id} -> confirmed")
   
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f" [v] Done, email sent to contact with id {contact_id} with tag: {method.delivery_tag}\n")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='contacts_queue', on_message_callback=callback)


channel.start_consuming()




