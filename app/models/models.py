from app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.mssql import JSON


class Sla(db.Model):
    __tablename__ = "sla"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(64))
    f5_min = db.Column(db.Integer())
    t20_min = db.Column(db.Integer())
    s60_min = db.Column(db.Integer())

    def __init__(self, type, f5_min, t20_min, s60_min):
        self.type = type
        self.F5_MIN = f5_min
        self.T20_MIN = t20_min
        self.S60_MIN = s60_min


class SlaConfigDetails(db.Model):
    __tablename__ = "sla_config_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    account = db.Column(db.String(64))
    application = db.Column(db.String(64))
    sla_number = db.Column(db.Integer)
    sla_description = db.Column(db.String(200))
    frequency = db.Column(db.String(64))
    level_type = db.Column(db.String(64))
    sla_type = db.Column(db.String(64))
    target = db.Column(db.Integer)
    weightage = db.Column(db.Integer)
    penalty = db.Column(db.Boolean)
    circle_level_sla = db.Column(db.Boolean)
    table_name = db.Column(db.String(64))
    sla_cal_condition = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(64))
    indicator = db.Column(db.String(64))
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, account, application, sla_number, sla_description, frequency,
                 level_type, sla_type, target, weightage, penalty,
                 circle_level_sla,  table_name, sla_cal_condition, status, user_id, indicator):
        self.account = account
        self.application = application
        self.sla_number = sla_number
        self.sla_description = sla_description
        self.frequency = frequency
        self.level_type = level_type
        self.sla_type = sla_type
        self.target = target
        self.weightage = weightage
        self.penalty = penalty
        self.circle_level_sla = circle_level_sla
        self.table_name = table_name
        self.sla_cal_condition = sla_cal_condition
        self.status = status
        self.user_id = user_id
        self.indicator = indicator


class SlaConfigParam(db.Model):
    __tablename__ = "sla_config_param"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activity_id = db.Column(db.Integer)
    param_type = db.Column(db.String(64))
    param_account = db.Column(db.String(64))
    param_name = db.Column(db.String(64))
    param_value = db.Column(db.String(64))
    status = db.Column(db.Integer)

    def __init__(self, activity_id, param_type, param_account, param_name, param_value, status):
        
        self.activity_id = activity_id
        self.param_type = param_type
        self.param_account = param_account
        self.param_name = param_name
        self.param_value = param_value
        self.status = status


class SlaUserManagement(UserMixin, db.Model):
    __tablename__ = "sla_user_management"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String(64))
    user_name = db.Column(db.String(64))
    email_id = db.Column(db.String(64))
    password = db.Column(db.String(2000))
    status = db.Column(db.Integer, default=0)
    attempt = db.Column(db.Integer, default=0)
    reset_ind = db.Column(db.String(64), default=1)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, user_name, user_id, email_id, password, status=0,
                 attempt=0, reset_ind=1):
        self.user_name = user_name
        self.user_id = user_id
        self.email_id = email_id
        self.password = password
        self.status = status
        self.attempt = attempt
        self.reset_ind = reset_ind


class SlaUserRole(db.Model):
    __tablename__ = "sla_user_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(64))
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    account = db.Column(db.String(64))
    role = db.Column(db.String(64))
    status = db.Column(db.String(64))
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, account, role='read', status=0):
        self.user_id = user_id
        self.account = account
        self.role = role
        self.status = status


class SlaUserQuery(db.Model):
    __tablename__ = "sla_user_query"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    account = db.Column(db.String(64))
    name = db.Column(db.String(64))
    user_id = db.Column(db.String(64))
    mobile_number = db.Column(db.BigInteger)
    email_id = db.Column(db.String(64))
    service = db.Column(db.String(64))
    message = db.Column(db.String(400))

    def __init__(self, account, user_name, user_id, mobile_no, email_id, service, message):
        self.account = account
        self.name = user_name
        self.user_id = user_id
        self.mobile_number = mobile_no
        self.email_id = email_id
        self.service = service
        self.message = message


class SlaPendingRequests(db.Model):
    __tablename__ = "sla_pending_approval"
    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    account = db.Column(db.String(64))
    user_id = db.Column(db.String(64))
    activity = db.Column(db.String(64))
    dynamic_information = db.Column(JSON)
    justification = db.Column(db.String(400))
    remark = db.Column(db.String(64))
    status = db.Column(db.String(2), default='P')

    def __init__(self, account, user_id, activity, info, justification, remark=' ', status='P'):
        self.account = account
        self.user_id = user_id
        self.activity = activity
        self.dynamic_information = info
        self.justification = justification
        self.remark = remark
        self.status = status


class SlaDataModel(db.Model):
    __tablename__ = "sla_data_manager"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    sys_update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    account = db.Column(db.String(64))
    sla_date = db.Column(db.Date)
    sla_number = db.Column(db.Integer)
    sla_type = db.Column(db.String(64))
    total_request = db.Column(db.Integer)
    within_sla_reqeust = db.Column(db.Integer)
    sla_percentage = db.Column(db.Float)
    sla_met = db.Column(db.Boolean)

    def __init__(self, account, sla_date, sla_number, sla_type, total_reqeust,
                 within_sla_reqeust, sla_percentage, sla_met):
        self.account = account
        self.sla_date = sla_date
        self.sla_number = sla_number
        self.sla_type = sla_type
        self.total_request = total_reqeust
        self.within_sla_reqeust = within_sla_reqeust
        self.sla_percentage = sla_percentage
        self.sla_met = sla_met
