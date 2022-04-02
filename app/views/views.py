from flask_api import status
from flask_login import current_user
from app.utils.auth import login_user, login_required, logout_user
from app.utils.actions import ActionMap
from app.utils.json_generator import JsonGenerator
from app.utils.requests import RequestRaised, ResetPassword, ChangePassword
from app.utils.response_generator import ResponseGenerator
from flask_restful import Resource
from flask import make_response
from app.models.models import SlaUserManagement, SlaUserQuery, SlaConfigDetails
from app.utils.config import SlaConfigDetail, GetSlaDetails, GetSlaData
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
            config_detail = SlaConfigDetail()
            config_details = config_detail.get_config_details()
            payload = [config_details]
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK)\
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()

    def post(self):
        config_detail = SlaConfigDetail()
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
                    print(111)
                    return ResponseGenerator(data=payload, status_code=status.HTTP_201_CREATED) \
                        .make_success_response()
                else:
                    print(112)
                    return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                        .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class VistaHomeView(Resource):


    def get(self):
        user = session["user"]
        try:
            user_obj = User(user_id=user.user_id, account=user.account)
            user_accounts = user_obj.get_user_accounts()
            session["user_accounts"] = user_accounts
            return ResponseGenerator('Vil_Sla_Homepage.html') \
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))

    
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
    @authorize
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
    @authorize
    def get(self, account):
        try:
            sla_obj = GetSlaDetails(account=account)
            sla_details = sla_obj.get_sla_details()
            if not sla_details:
                message = "No Sla is configured. "
                return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
                    .make_success_response()

            payload = []
            for sla in sla_details:
                data = {
                    "id": sla.id,
                    "creation_date": sla.sys_creation_date,
                    "account": sla.account,
                    "application": sla.application,
                    "sla_number": sla.sla_number,
                    "sla_description": sla.sla_description,
                    "frequency": sla.frequency,
                    "level_type": sla.level_type,
                    "sla_type": sla.sla_type,
                    "target": sla.target,
                    "weightage": sla.weightage,
                    "penalty": sla.penalty,
                    "circle_level_sla": sla.circle_level_sla,
                    "table_name": sla.table_name,
                    "sla_cal_condition": sla.sla_cal_condition,
                    "status": sla.status,
                    "user_id": sla.user_id,
                    "indicator": sla.indicator

                }
                payload.append(data)
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class ServiceView(Resource):
    @authorize
    def get(self, user, account):
        try:
            # all_request = db.session.query(SlaPendingRequests).outerjoin(SlaUserRole,
            # SlaPendingRequests.user_id==SlaUserRole.user_id)\
            #     .filter(SlaUserRole.account == user.account).filter(or_(db.session.query(SlaUserRole.role).filter_by(
            #     user_id = user.user_id).first().role == "approver", SlaPendingRequests.user_id==user.user_id)).all()
            # print(all_request)
            query = f"""select sys_creation_date, activity_id, account, user_id, activity, dynamic_information,
            justification, status from sla_pending_approval where user_id='{user}'
            and account='{account}' union select sys_creation_date , activity_id, account, user_id, activity,
            dynamic_information, justification, status from sla_pending_approval c where c.status='Pending'
             and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and
             role='approver' and a.user_id='{user}' and c.dynamic_information like '%' || b.account || '%')
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
                    # "justification": req.justification,
                    "remark": req.justification,
                    "status": req.status
                }
                payload.append(data)
                print(payload)
            return ResponseGenerator(data=payload, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()

    @authorize
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
    @authorize
    def get(self, account):
        try:
            slas = db.session.query(SlaConfigDetails.sla_number, SlaConfigDetails.sla_description).\
                filter_by(account=account, status=0).all()
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

    @authorize
    def post(self, account):
        # data = request.form
        message = "SLA download successful. "
        return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
            .make_success_response()


class AccessControlView(Resource):
    def get(self):
        config_detail = SlaConfigDetail()
        config_details = config_detail.get_config_details()
        return ResponseGenerator(data=config_details, status_code=status.HTTP_200_OK) \
            .make_success_response()


class RequestsView(Resource):
    @authorize
    def post(self):
        try:
            data = request.json
            user_info = data["user"]
            user, account = user_info["user_id"], user_info["account"]
            json_obj = JsonGenerator(form_data=data, user=user, account=account)
            json_data, request_type = json_obj.generate_json()
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
        data = request.json
        obj = ChangePassword(user_id=data["user_id"], old_password=data["old_password"],
                                 new_password=data["new_password"])
        message = obj.change_password()
        if not obj.result:
            return ResponseGenerator(message=message, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()
        return ResponseGenerator(message=message, status_code=status.HTTP_200_OK) \
            .make_success_response()



class SignUpView(Resource):
    def post(self):
        try:
            data = request.json
            user, account = data["id"], data["account"]
            json_obj = JsonGenerator(form_data=data, user=user, account=account)
            json_data, request_type = json_obj.generate_json()
            if not json_obj.redirect:
                raise_request = RequestRaised(user, account, json_data, request_type)
                json_obj.message = raise_request.handle_request()
            return ResponseGenerator(message=json_obj.message, status_code=status.HTTP_200_OK) \
                .make_success_response()
        except Exception as e:
            return ResponseGenerator(message=e, status_code=status.HTTP_400_BAD_REQUEST) \
                .make_error_response()


class ResetPasswordView(Resource):
    def post(self):
        data = request.json
        pass_obj = ResetPassword(data["id"])
        pass_obj.reset_password()
        if pass_obj.result:
            return ResponseGenerator(message=pass_obj.message, status_code=status.HTTP_200_OK) \
                .make_success_response()
        return ResponseGenerator(message=pass_obj.message, status_code=status.HTTP_400_BAD_REQUEST) \
            .make_error_response()

        # return make_response(redirect('/login'))

class Logout(Resource):
    @authorize
    def get(self):
        try:
            logout_user()
            flash("Logout Successful. ")
            return make_response(redirect('/login'))
        except Exception as e:
            return make_response(render_template('404.html', error=e))


class SlaDashboardView(Resource):
    
    def get(self):
        today = date.today()
        sla_obj = GetSlaData(today)
        sla_data = sla_obj.get_sla_details()
        for i in sla_data:
            print(i)
        return make_response(render_template("Vil_Sla_Dashboard.html", r=sla_data, dashboard_header=["Hello"]))

    
    def post(self):
        pass
