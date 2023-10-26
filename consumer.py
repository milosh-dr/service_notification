import pika, sys, os, time
from send import email


def main():
    # rabbit / host to be changed if run in the cluster
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(channel, method, properties, body):
        err = email.notification(body)
        if err:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume('mp3', on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL + C ...')

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)