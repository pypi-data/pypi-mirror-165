from notif.channels.abstract_channel import AbstractChannel


class SMSMessageSender(AbstractChannel):

    def __init__(self, phone_number, message):
        self.phone_number = phone_number
        self.message = message

    def notif_type(self):
        return 'SEND_SMS_MESSAGE'

    def json(self):
        return {
            'phone_number': self.phone_number,
            'message': self.message,
        }

    def attachments(self):
        return []
