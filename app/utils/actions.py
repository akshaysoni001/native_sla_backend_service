import json
from werkzeug.security import generate_password_hash
from app import db
from app.constant.constant import action_map
from app.models.models import SlaConfigDetails, SlaUserRole, SlaPendingRequests, SlaUserManagement
from app.utils.mail_sender import MailService
from app.utils.utils import password_genrator


class ActionMap:
    def __init__(self, activity_id, raised_user_id, activity, raised_account, info, remark, action):
        self.activity = activity
        self.activity_id = activity_id
        self.raised_user_id = raised_user_id
        self.raised_account = raised_account
        self.info = json.loads(info)
        self.remark = remark
        self.action = action
        self.message = None
        self.status = None
        self.password = None

    def _approve(self):
        # Working but need to check data types
        if self.activity == "add_sla":
            obj = SlaConfigDetails(
                account=self.info["account"],
                application=self.info["application"],
                sla_number=self.info["sla_number"],
                sla_description=self.info["sla_description"],
                sla_type=self.info["sla_type"],
                target=self.info["target"],
                penalty=self.info["penalty"],
                )

            db.session.add(obj)
        elif self.activity == "update_sla":
            sla_obj = db.session.query(SlaConfigDetails).filter_by(
                account=self.info["account"], application=self.info["application"], sla_number=self.info["sla_number"],
                deleted=False).one()

            # sla_obj.sla_number = self.info["sla_number"],
            print(self.info["sla_type"], type(self.info["sla_type"]))
            print(sla_obj.sla_type, type(sla_obj.sla_type))
            sla_obj.sla_number = self.info["sla_number"]
            sla_obj.sla_description = self.info["sla_description"]
            # sla_obj.sla_type = self.info["sla_type"],
            sla_obj.target = self.info["target"]
            sla_obj.penalty = self.info["penalty"]

        elif self.activity == "delete_sla":
            sla_obj = db.session.query(SlaConfigDetails).filter_by(
                account=self.info["account"], application=self.info["application"], sla_number=self.info["sla_number"],
                deleted=False).first()
            sla_obj.deleted = True

        elif self.activity == "Add Account":
            user_role_obj = SlaUserRole(user_id=self.raised_user_id, account=self.info["service"])
            db.session.add(user_role_obj)

        elif self.activity == "User_Rights":
            user_config_obj = db.session.query(SlaUserRole).filter_by(user_id=self.raised_user_id,
                                                                      account=self.raised_account, deleted=False).first()
            user_config_obj.role = "Lead"

        elif self.activity == "registration":
            password = password_genrator()
            user_obj = action_map[self.activity](
                user_name=self.info["name"],
                user_id=self.info["user_id"],
                email_id=self.info["email_id"],
                password=generate_password_hash(password)
            )
            user_config = SlaUserRole(user_id=self.info["user_id"], account=self.info["account"])
            self.password = password
            db.session.add(user_obj)
            db.session.add(user_config)
        else:
            self.message = "Invalid Request"
            return self.message

        if self.message is None:
            self.status = 'Approved'
            self.message = "Request approved. "

    def _reject(self):
        self.status = 'Rejected'
        self.message = "Request rejected. "
        return self.message

    def _update_request(self):
        pending_request = db.session.query(SlaPendingRequests).filter_by(
            activity_id=self.activity_id
        ).first()
        pending_request.status = self.status
        pending_request.remark = self.remark
        db.session.commit()

    def _send_mail(self):

        self._get_mailing_details()
        mail = MailService(type=self.action, request=self.activity, user_name=self.username,
                           receipent_email=self.user_email, password=self.password, remark=self.remark)
        mail.send_mail()

    def _get_mailing_details(self):
        usr = db.session.query(SlaUserManagement.user_name, SlaUserManagement.email_id).\
            filter_by(user_id=self.raised_user_id).first()
        if usr:
            self.username = usr.user_name
            self.user_email = usr.email_id
        else:
            self.username = self.info["user_id"]
            self.user_email = self.info["email_id"]

    def take_action(self):
        if self.action == "approve":
            self._approve()
        elif self.action == "reject":
            self._reject()
        else:
            self.message = "Invalid Request"

        if self.message == "Invalid Request":
            return self.message

        self._update_request()
        self._send_mail()
        return self.message
