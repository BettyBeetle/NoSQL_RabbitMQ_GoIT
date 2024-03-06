import pika
import json
from model import Contact
from mongoengine import connect
from connect import connect
from faker import Faker


connect('email_campaign', alias='email_campaign_alias')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue', durable=True)


faker = Faker()
num_of_contacts = 4 

for _ in range(num_of_contacts):
    
    contact = Contact(first_name=faker.first_name(), last_name = faker.last_name(), email=faker.email())
    contact.save()
    message = {
        'contact_id': str(contact.id)   
    } 
    
    channel.basic_publish(
        exchange='',
        routing_key='contacts_queue',
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    print(f" [v] Sent contact {contact.id} to the queue")

connection.close() 

      


 
