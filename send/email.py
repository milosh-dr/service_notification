# Timestamp 4:36:45

import smtplib, os, json
from email.message import EmailMessage


def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message['mp3_fid']
        sender_address = os.environ.get('$SENDER_ADDRESS')
        sender_password = os.environ.get('$SENDER_PASSWORD')
        receiver_address = message['username']

        msg = EmailMessage()
        msg.set_content(f'Mp3 file_id {mp3_fid} is ready for download!')
        msg['Subject'] = 'Mp3 download'
        msg['From'] = sender_address
        msg['To'] = receiver_address

        session = smtplib.SMTP_SSL('smtp.wp.pl', 465)
        # session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, receiver_address)
        session.quit()
        print('Mail sent!')
    except Exception as err:
        print(err)
        return err