import pika
import json
from faker import Faker
from models import Contact
from mongoengine import connect
import random

connect(host="mongodb+srv://usermodule-8:5671234@ruslana.l69lrsa.mongodb.net/hw_module_8?retryWrites=true&w=majority")

fake = Faker()

def send_to_queue(contact_id, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    message = json.dumps({"contact_id": str(contact_id)})
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    print(f"Sent message to {queue_name} for contact {contact_id}")
    connection.close()

def main():
    num_contacts = 10
    for _ in range(num_contacts):
        preferred = random.choice(["email", "sms"])
        contact = Contact(
            fullname=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            notes=fake.sentence(),
            preferred_method=preferred
        ).save()
        queue = "email_queue" if preferred == "email" else "sms_queue"
        send_to_queue(contact.id, queue)

if __name__ == "__main__":
    main()