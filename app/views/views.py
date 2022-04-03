from flask_api import status
from flask_login import current_user
from app.utils.auth import login_user, login_required, logout_user
from app.utils.actions import ActionMap
from app.utils.json_generator import JsonGenerator
from app.utils.requests import RequestRaised, ResetPassword, ChangePassword
from app.utils.response_generator import ResponseGenerator
from flask_restful import Resource
from flask import make_response
from app.models.models import SlaUserManagement, SlaUserQuery, SlaGlobalConfiguration, SlaConfigDetails, SlaDataModel, \
    SlaUserRole
from app.utils.config import GlobalConfiguration, GetSlaDetails, GetSlaData
from app import render_template, db, request, redirect, logging, flash
from datetime import date, datetime, timedelta
from app.utils.authorize import authorize
import jwt
from app.utils.config import User
from app import app, session


# 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404


class VistaLoginView(Resource):
    def get(self):
        try:
            config_detail = GlobalConfiguration()
            config_details = config_detail.get_config_details()
            payload = [config_details]
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK)\
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()

    def post(self):
        config_detail = GlobalConfiguration()
        config_details = config_detail.get_config_details()
        try:
            usr = request.json
            user_obj = db.session.query(SlaUserManagement).filter_by(user_id=usr["username"]).first()
            validation_ojb = User(user_id=usr["username"], account=usr["account"],
                                  password=usr["password"], user_obj=user_obj)
            message, result, pass_change_required = validation_ojb.validate_user()
            if not result:
                return ResponseGenerator(message=message, status_code=status.HTTP_400_BAD_REQUEST) \
                    .make_error_response()
            else:
                user_data = validation_ojb.get_user_data()
                payload = []
                token = jwt.encode({
                    'user_id': user_data.user_id,
                    'user_name': user_data.user_name,
                    'account': user_data.account,
                    'email': user_data.email_id,
                    'roles': user_data.role,
                    'expiration': str(datetime.utcnow() + timedelta(seconds=50))
                }, app.config['SECRET_KEY'])
                user = {
                    'user_id': user_data.user_id,
                    'user_name': user_data.user_name,
                    'account': user_data.account,
                    'email': user_data.email_id,
                    'roles': user_data.role,
                }
                payload.append(token.decode('utf-8'))
                payload.append(user)
                if pass_change_required:
                    return ResponseGenerator(data=payload, status_code=status.HTTP_201_CREATED) \
                        .make_success_response()
                else:
                    return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                        .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class VistaHomeView(Resource):
    def get(self, user, account):
        try:
            application_list = db.session.query(SlaGlobalConfiguration.value).filter_by(account=account,
                                                                                        type="account",
                                                                                        sub_type="applications").all()
            slas = db.session.query(SlaConfigDetails.sla_number).filter_by(account=account).all()
            sla_met = db.session.query(SlaDataModel.sla_number).filter_by(account=account, sla_met=True).all();
            sla_breached = db.session.query(SlaDataModel.sla_number).filter_by(account=account, sla_met=False).all();
            sla_data = db.session.query(SlaDataModel).filter_by(account=account).all();
            sla_owner = db.session.query(SlaUserManagement.user_name, SlaUserRole.account).outerjoin(SlaUserRole,
                                                                                                     SlaUserManagement.user_id == SlaUserRole.user_id).filter(
                SlaUserRole.account == account, SlaUserRole.role == "manager").all();
            applications = [value for (value,) in application_list]
            slas = [value for (value,) in slas]
            sla_met = [value for (value,) in sla_met]
            sla_breached = [value for (value,) in sla_breached]
            sla_owners = [{'user_name': value, 'account': value1} for (value, value1) in sla_owner]
            #
            apps = []
            for app in applications[0].split(','):
                app = {'color': "green",
                            'icon': "fas fa-mobile",
                            'subtitle': "Design",
                            'title': app}
                apps.append(app)
            all_sla=[]
            for sla in sla_data:
                dic = {'id':sla.id,
                                    'account':sla.account,
                                    'application':sla.application,
                                    'sla_number':sla.sla_number,
                                    'sla_percentage':sla.sla_percentage,
                                    'sla_type':sla.sla_type}
                all_sla.append(dic)
            payload = {'applications': apps,
                       'slas': slas,
                       'sla_met': sla_met,
                       'sla_breached': sla_breached,
                       'sla_data': all_sla,
                        'sla_owners': sla_owners
                       }
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                .make_success_response()

        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


    
    def post(self):
        user = session["user"]
        try:
            data = request.form
            new_account = data["new_account"]
            if user["account"] == new_account:
                message = f"You are already logged in with account {user['account']}"
                return ResponseGenerator('Vil_Sla_Homepage.html', message=message) \
                    .make_success_response()

            new_user_config = User(user_id=user.user_id, account=new_account)
            updated_user_data = new_user_config.get_user_data()
            session["user"] = updated_user_data
            message = f"account switched to {new_account}"
            return ResponseGenerator('Vil_Sla_Homepage.html', message=message) \
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))
#


class ContactView(Resource):
    # @authorize
    def post(self):
        try:
            data = request.json
            # Validate Data
            user_info = data["user"]
            user, account = user_info["user_id"], user_info["account"]
            insert_data = SlaUserQuery(account=account, user_name=data["name"],
                                       user_id=user, mobile_no=data["phoneNumber"],
                                       email_id=data["email"], service=data["select"], message=data["message"])
            db.session.add(insert_data)
            db.session.commit()
            message = "Thanks for your feedback."
            return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            logging.error("error@contact", e)
            db.session.rollback()
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_success_response()


class AccountSlaView(Resource):
    # @authorize
    def get(self, account):
        try:
            sla_obj = GetSlaDetails(account=account)
            sla_details = sla_obj.get_sla_details()
            if not sla_details:
                message = "No Sla is configured. "
                return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
                    .make_success_response()
            application_list = db.session.query(SlaGlobalConfiguration.value).filter_by(account=account,
                                                                                        type="account",
                                                                                        sub_type="applications").all()
            applications = [value for (value,) in application_list]
            payload = [applications[0].split(',')]
            # payload = []
            for sla in sla_details:
                data = {
                    "id": sla.id,
                    "creation_date": sla.sys_creation_date,
                    "account": sla.account,
                    "application": sla.application,
                    "sla_number": sla.sla_number,
                    "sla_description": sla.sla_description,
                    "sla_type": sla.sla_type,
                    "target": sla.target,
                    "penalty": sla.penalty
                }
                payload.append(data)
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class ServiceView(Resource):
    # @authorize
    def get(self, user, account):
        try:
            # all_request = db.session.query(SlaPendingRequests).outerjoin(SlaUserRole,
            # SlaPendingRequests.user_id==SlaUserRole.user_id)\
            #     .filter(SlaUserRole.account == user.account).filter(or_(db.session.query(SlaUserRole.role).filter_by(
            #     user_id = user.user_id).first().role == "approver", SlaPendingRequests.user_id==user.user_id)).all()
            # print(all_request)
            query = f"""select sys_creation_date, activity_id, account, user_id, activity, dynamic_information,
            reason, remark, status from sla_pending_approval where user_id='{user}'
            and account='{account}' union select sys_creation_date , activity_id, account, user_id, activity,
            dynamic_information, reason, remark, status from sla_pending_approval c where c.status='pending'
             and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and
             role='manager' and a.user_id='{user}' and c.dynamic_information like '%' || b.account || '%')
             order by sys_creation_date desc
            """
            all_request = db.session.execute(query).all()
            payload = []
            for req in all_request:
                data = {
                    "account": req.account,
                    "user_id": req.user_id,
                    "activity": req.activity,
                    "activity_id": req.activity_id,
                    "dynamic_information": req.dynamic_information,
                    "reason": req.reason,
                    "remark": req.remark,
                    "status": req.status
                }
                payload.append(data)
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()

    # @authorize
    def post(self, user, account):
        try:
            data = request.json
            raised_request = ActionMap(
                raised_user_id=data["user_id"],
                activity=data["activity"],
                activity_id=data["activity_id"],
                raised_account=data["account"],
                info=data["dynamic_information"],
                remark=data["remark"],
                action=data["action"]
            )
            message = raised_request.take_action()
            return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()
            # return "Invalid Request"


class SlaDownloadView(Resource):
    # # @authorize
    def get(self, account):
        try:
            slas = db.session.query(SlaConfigDetails.sla_number, SlaConfigDetails.sla_description).\
                filter_by(account=account, deleted=False).all()
            if not slas:
                message = "No Sla is configured. "
                return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
                    .make_success_response()
            payload = []
            for sla in slas:
                data = f"{sla[0]}: {sla[1]}"
                payload.append(data)
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()

    # @authorize
    def post(self, account):
        # data = request.form
        message = "SLA download successful. "
        return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
            .make_success_response()


class AccessControlView(Resource):
    def get(self):
        config_detail = GlobalConfiguration()
        config_details = config_detail.get_config_details()
        return ResponseGenerator(data=config_details, status_code=status.HTTP_200_OK) \
            .make_success_response()


class RequestsView(Resource):
    # @authorize
    def post(self):
        try:
            data = request.json
            user_info = data["user"]
            user, account = user_info["user_id"], user_info["account"]
            json_obj = JsonGenerator(form_data=data, user=user, account=account)
            json_data, request_type = json_obj.generate_json()
            if not json_obj.result:
                return ResponseGenerator(message=json_obj.message, status_code=status.HTTP_400_BAD_REQUEST) \
                    .make_error_response()
            if json_obj.redirect:
                return ResponseGenerator(message=json_obj.message, status_code=status.HTTP_205_RESET_CONTENT) \
                    .make_success_response()
            raise_request = RequestRaised(user, account, json_data, request_type)
            json_obj.message = raise_request.handle_request()
            return ResponseGenerator(message=json_obj.message, status_code=status.HTTP_200_OK) \
                .make_success_response()

        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class PasswordChange(Resource):
    def post(self):
        try:
            data = request.json
            obj = ChangePassword(user_id=data["user_id"], old_password=data["old_password"],
                                     new_password=data["new_password"])
            message = obj.change_password()
            if not obj.result:
                return ResponseGenerator(message=message, status_code=status.HTTP_400_BAD_REQUEST) \
                    .make_error_response()
            return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()

class SignUpView(Resource):
    def post(self):
        try:
            data = request.json
            user, account = data["id"], data["account"]
            json_obj = JsonGenerator(form_data=data, user=user, account=account)
            json_data, request_type = json_obj.generate_json()
            if not json_obj.redirect:
                raise_request = RequestRaised(user_id=user, user_account=account,
                                              new_data=json_data, request_type=request_type)
                json_obj.message = raise_request.handle_request()
            return ResponseGenerator(message=json_obj.message, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class ResetPasswordView(Resource):
    def post(self):
        try:
            data = request.json
            pass_obj = ResetPassword(data["id"])
            pass_obj.reset_password()
            if pass_obj.result:
                return ResponseGenerator(message=pass_obj.message, status_code=status.HTTP_200_OK) \
                    .make_success_response()
            return ResponseGenerator(message=pass_obj.message, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()
        # return make_response(redirect('/login'))


class SlaDashboardView(Resource):
    
    def get(self):
        today = date.today()
        sla_obj = GetSlaData(today)
        sla_data = sla_obj.get_sla_details()
        return make_response(render_template("Vil_Sla_Dashboard.html", r=sla_data, dashboard_header=["Hello"]))

    
    def post(self):
        pass
