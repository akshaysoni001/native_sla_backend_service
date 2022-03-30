from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.models import SlaUserManagement, SlaPendingRequests, SlaUserRole
from app.utils.mail_sender import MailService
from flask_login import current_user, logout_user

from app.utils.utils import password_genrator


class RequestRaised:
    def __init__(self, user_id, user_account, new_data, request_type, message=None):
        self.user_id = user_id
        self.user_account = user_account
        self.new_data = new_data
        self.activity = request_type
        self.message = message
        self.approver_email = None

    def _send_mail(self):
        self._get_mailing_details()
        mail = MailService(type='request_raised', request=self.activity, user_name=self.username,
                           receipent_email=self.user_email, approver_mail=self.approver_email)
        mail.send_mail()

    def _get_mailing_details(self):
        mail_user = db.session.query(SlaUserManagement.user_name, SlaUserManagement.email_id).\
                filter_by(user_id=self.user_id, deleted=False).first()
        self.username = mail_user.user_name
        self.user_email = mail_user.email_id

        obj = db.session.query(SlaUserManagement.email_id, SlaUserManagement.user_name) \
            .outerjoin(SlaUserRole, SlaUserManagement.user_id == SlaUserRole.user_id) \
            .filter(SlaUserRole.role == "approver", SlaUserRole.account == self.user_account,
                    SlaUserManagement.deleted == False).first()
        if obj:
            self.approver_email = obj.email_id

    def _get_pending_details(self):
        pass

    def _get_user_details(self):
        pass

    def handle_request(self):
        pending_request = db.session.query(SlaPendingRequests).filter_by(
            user_id=self.user_id, dynamic_information=self.new_data, activity=self.activity).first()

        if pending_request:
            self.message = "Request is already present"
            return self.message
        else:
            obj = SlaPendingRequests(account=self.user_account, user_id=self.user_id,
                                     activity=self.activity, info=self.new_data,
                                     justification=self.new_data["justification"])

            db.session.add(obj)
            db.session.commit()
            self.message = "Request  raised"

        self._send_mail()
        return self.message


class ResetPassword:
    def __init__(self, user_id):
        self.message = None
        self.user_id = user_id

    def reset_password(self):
        usr = db.session.query(SlaUserManagement).filter_by(user_id=self.user_id, deleted=False).first()

        if not usr:
            self.message = "user not found."
            return self.message
        password = password_genrator()
        usr.password = generate_password_hash(password)
        usr.reset_ind = 1
        usr.attempt = 0
        db.session.commit()
        mail = MailService(type='password_reset', request="PasswordReset", user_name=usr.user_name,
                           receipent_email=usr.email_id, password=password)
        mail.send_mail()
        self.message = "New pass word has been sent on mail, kindly check and login. "
        return self.message


class ChangePassword:
    def __init__(self, user_id, old_password, new_password):
        self.message = None
        self.user_id = user_id
        self.old_password = old_password
        self.new_password = new_password

    def change_password(self):
        usr = db.session.query(SlaUserManagement).\
            filter_by(user_id=self.user_id, deleted=False).first()
        result = check_password_hash(usr.password, self.old_password)
        if not result:
            self.message = "Invalid Old Password"
            return "Invalid Old Password"
        usr.password = generate_password_hash(self.new_password)
        usr.reset_ind = 0
        db.session.commit()
        logout_user()
        self.message = "Password changed successfully. "
        return self.message
