from sqlalchemy import and_
from werkzeug.security import check_password_hash

from app.models.models import SlaConfigParam, SlaConfigDetails, SlaDataModel, SlaUserManagement, SlaUserRole
from app import db, session
from dateutil.parser import parse
from sqlalchemy import func
from datetime import date


class SlaConfigDetail:

    def __init__(self):
        pass

    def _get_sla_config(self):
        all_account = db.session.query(SlaConfigParam.param_value).filter_by(
            param_type="account", param_name="extension").all()
        query_sender_email = db.session.query(SlaConfigParam.param_value).filter_by(
            param_type="email", param_name="sender").first()
        query_recipent_email = db.session.query(SlaConfigParam.param_value).filter_by(
            param_type="email", param_name="recipent").first()
        supported_domains = db.session.query(SlaConfigParam.param_value).filter_by(
            param_type="email", param_account="all", param_name="domain").all()
        config = {
            "all_account":  [value for (value,) in all_account],
            "sender_email": query_sender_email,
            "recipent_email": query_recipent_email,
            "supported_domains": supported_domains
        }
        return config

    def get_config_details(self):
        sla_config = self._get_sla_config()
        return sla_config


class GetSlaDetails:
    def __init__(self, account=None, start_date=None, end_date=None, sla_number=None):
        self.account = account
        self.from_date = start_date
        self.to_date = end_date
        self.sla_number = sla_number

    def _get_sla_details(self):
        if self.from_date and self.to_date and self.sla_number:
            sla_details = db.session.query(SlaConfigDetails).filter_by(status=0, account=self.account,
                                                                       sla_number=self.sla_number).filter(
                and_(SlaConfigDetails.sys_creation_date <= parse(self.to_date), SlaConfigDetails.sys_creation_date
                     >= parse(self.from_date)), deleted=False).all()
        else:
            sla_details = db.session.query(SlaConfigDetails).filter_by(status=0,
                                                                       account=self.account, deleted=False).all()
        return sla_details

    def get_sla_details(self):
        sla_details = self._get_sla_details()
        return sla_details


class GetSlaData:
    def __init__(self, date):
        self.date = date

    def _get_details(self):
        # sla_data = db.session.query(SlaDataModel).filter_by(account=user.account,
        #                                                     sla_date=parse(self.date)).all()
        sla_data = db.session.query(SlaDataModel).filter(func.date(SlaDataModel.sla_date) == date.today()).all()
        return sla_data

    def get_sla_details(self):
        sla_details = self._get_details()
        return sla_details


class User:
    def __init__(self, user_id, account, password=None, user_obj=None):
        self.user_id = user_id
        self.account = account
        self.password = password
        self.user_obj = user_obj
        self.message = None
        self.result = False
        self.pass_change_required = False

    def validate_user(self):
        if not self.user_obj:
            self.message = f"User with user_id {self.user_id} does not exist."
            return self.message, self.result, self.pass_change_required
        result = check_password_hash(self.user_obj.password, self.password)
        if not result:
            self.message = "Invalid Password"
            self.user_obj.attempt += 1
            db.session.commit()
            return self.message, self.result, self.pass_change_required

        user_accounts = self.get_user_accounts()

        if self.account not in user_accounts:
            self.message = f"You don't have rights to access account {self.account}."
            return self.message, self.result, self.pass_change_required

        if self.user_obj.attempt > 2:
            self.message = "Max attempt reached, account locked, please reset password."
            self.result = False
            return self.message, self.result, self.pass_change_required

        self.result = True

        if int(self.user_obj.reset_ind) == 1:
            self.pass_change_required = True
            return self.message, self.result, self.pass_change_required

        return self.message, self.result, self.pass_change_required

    def get_user_data(self):
        user_data = db.session.query(SlaUserManagement.id,
                                     SlaUserManagement.user_name,
                                     SlaUserManagement.user_id,
                                     SlaUserManagement.email_id,
                                     SlaUserManagement.status,
                                     SlaUserManagement.password,
                                     SlaUserManagement.attempt,
                                     SlaUserManagement.reset_ind,
                                     SlaUserRole.account,
                                     SlaUserRole.role).outerjoin(SlaUserRole,
                                                                 SlaUserManagement.user_id == SlaUserRole.user_id).\
            filter(
            SlaUserManagement.user_id == self.user_id, SlaUserRole.account == self.account,
            SlaUserManagement.deleted == False).first()
        return user_data

    def get_user_accounts(self):
        user_accounts = db.session.query(SlaUserRole.account).filter_by(user_id=self.user_id, deleted=False).all()
        user_accounts = [account[0] for account in user_accounts]
        return user_accounts
