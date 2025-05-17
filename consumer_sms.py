import os
from dotenv import load_dotenv
import pika
import json
from models import Contact
from mongoengine import connect

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
connect(host=mongo_uri)


def send_sms_stub(contact):
    print(f"Sending SMS to {contact.phone}...[stub]")


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        contact_id = data.get("contact_id")
        if not contact_id:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        contact = Contact.objects(id=contact_id).first()
        if not contact:
            print(f"Contact with id {contact_id} not found")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        send_sms_stub(contact)
        contact.update(set__sent=True)
        print(f"Marked contact {contact.fullname} as sent by SMS")
    except Exception as e:
        print(f"Error processing SMS message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="sms_queue", durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="sms_queue", on_message_callback=callback)
        print("Waiting for SMS messages. To exit press CTRL+C")
        channel.start_consuming()


if __name__ == '__main__':
    main()