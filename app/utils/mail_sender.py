from app import mail, app
from app.utils.message_genrator import MessageService
from flask_mail import Message
from threading import Thread


class MailService:
    def __init__(self, type, request, receipent_email, user_name, approver_mail="", remark="", password=None):
        self.type = type
        self.request = request
        self.receipent = receipent_email
        self.approver = approver_mail
        self.user_name = user_name
        self.remark = remark
        self.password = password
        self.mail_body = None
        self.notification_mail_body = None
        self.usr_mail = None
        self.notify_mail = None

    def _get_mail_body(self):
        message = MessageService(user_name=self.user_name, type=self.type, request=self.request,
                                 password=self.password, remark=self.remark)
        self.mail_body, self.notification_mail_body = message.get_message()

    def _created_thread_for_mail(self):
        p1 = Thread(target=self._async_send_mail, args=[self.usr_mail])
        p1.start()
        if self.notify_mail:
            p2 = Thread(target=self._async_send_mail, args=[self.notify_mail])
            p2.start()

    def _async_send_mail(self, msg):
        with app.app_context():
            mail.send(msg)

    def send_mail(self):
        self._get_mail_body()
        # send user mail
        print("#############User Email###########")
        print(self.mail_body)
        self.usr_mail = Message("Vista Notification", recipients=self.receipent.split())
        self.usr_mail.body = self.mail_body

        if self.notification_mail_body:
            print("#######Notification Email#######")
            print(self.notification_mail_body)
            if self.approver and self.type == "request_raised":
                self.notify_mail = Message("Vista Notification", recipients=self.approver.split())
                self.notify_mail.body = self.notification_mail_body
                # mail.send(notify_mail)
            if self.request == "registration" and self.type == "approve":
                self.notify_mail = Message("Vista Login Details", recipients=self.receipent.split())
                self.notify_mail.body = self.notification_mail_body
                # mail.send(notify_mail)

        self._created_thread_for_mail()
