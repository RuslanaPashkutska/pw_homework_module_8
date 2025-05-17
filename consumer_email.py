import pika
import json
from models import Contact
from mongoengine import connect


connect(host="mongodb+srv://usermodule-8:5671234@ruslana.l69lrsa.mongodb.net/hw_module_8?retryWrites=true&w=majority")

def send_email_stub(contact):
    print(f"Sending EMAIL to {contact.email}...[stub]")

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

        send_email_stub(contact)
        contact.update(set__sent=True)
        print(f"Marked contact {contact.fullname} as sent by email")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="email_queue", durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="email_queue", on_message_callback=callback)
        print("Waiting for EMAIL messages. To exit press CTRL+C")
        channel.start_consuming()


if __name__ == '__main__':
    main()