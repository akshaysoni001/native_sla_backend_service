

class MessageService:
    def __init__(self, user_name, type, request, remark=None, password=None):
        self.user_name = user_name
        self.type = type
        self.request = request
        self.remark = remark
        self.password = password
        self.message = None
        self.notification_message = None

    def _request_raised(self):
        message = f"""
        Hi, {self.user_name}
        Your request for {self.request} has been received and shared with respective team for approval.
        we will notify you soon.
        
        Thanks & Regards,
        Native SLA Support Team
        """

        notification_message = self._request_notification()
        self.message = message
        self.notification_message = notification_message

    def _approval_mail(self):
        message = f"""
        Hi, {self.user_name}
        Your request for {self.request} has been approved.
        
        Thanks & Regards,
        Native SLA Support Team
        """
        if self.request == "registration":
            self.notification_message = self._registration_details()

        self.message = message

    def _rejection_mail(self):
        message = f"""
        Hi, {self.user_name}
        Your request for {self.request} has been rejected.
        
        Rejection_reason = {self.remark}
        
        Thanks & Regards,
        Native SLA Support Team
        """
        self.message = message

    def _registration_details(self):
        message = f"""
        Hi, {self.user_name}
        Thanks for signing with us, Please find your login credentials below:
        
        username = {self.user_name}
        password = {self.password}
        
        Thanks & Regards,
        Native SLA Support Team
        """

        return message

    def _password_reset(self):
        message = f"""
        Hi, {self.user_name},
        Please find your new password for user {self.user_name}
        
        login password : {self.password}
        
        Thanks & Regards,
        Native SLA Support Team
        """

        self.message = message

    def _request_notification(self):
        message = f"""
        Hi, 
        we have received request for {self.request}. Please check and take action.
        
        Thanks & Regards,
        Native SLA Support Team
        """

        return message

    def get_message(self):
        if self.type == "approve":
            self._approval_mail()
        elif self.type == "reject":
            self._rejection_mail()
        elif self.type == "request_raised":
            self._request_raised()
        elif self.type == "password_reset":
            self._password_reset()

        return self.message, self.notification_message
