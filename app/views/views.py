from flask_login import current_user
from app.utils.auth import login_user, login_required, logout_user
from app.utils.actions import ActionMap
from app.utils.json_generator import JsonGenerator
from app.utils.requests import RequestRaised
from app.utils.response_generator import ResponseGenerator
from flask_restful import Resource
from flask import make_response
from app.models.models import SlaUserManagement, SlaUserQuery, SlaConfigDetails
from app.utils.config import SlaConfigDetail, GetSlaDetails, GetSlaData
from app import render_template, db, request, redirect, logging, flash
from datetime import date
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
            return ResponseGenerator('Vil_Sla_Login.html', config_details=config_details)\
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))

    def post(self):
        config_detail = SlaConfigDetail()
        config_details = config_detail.get_config_details()
        try:
            usr = request.form
            user_obj = db.session.query(SlaUserManagement).filter_by(user_id=usr["username"]).first()
            validation_ojb = User(user_id=usr["username"], account=usr["account"],
                                  password=usr["password"], user_obj=user_obj)
            message, result, pass_change_required = validation_ojb.validate_user()
            if not result:
                return ResponseGenerator('Vil_Sla_Login.html', message=message, config_details=config_details) \
                    .make_error_response()
            else:
                user_data = validation_ojb.get_user_data()
                login_user(user_obj)
                session["user"] = user_data
                if pass_change_required:
                    return ResponseGenerator('Vil_Sla_Login.html', reset_ind=1, config_details=config_details) \
                        .make_success_response()
                else:
                    return make_response(redirect("/home"))
        except Exception as e:
            return make_response(render_template('404.html', error=e))


class VistaHomeView(Resource):

    @login_required
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

    @login_required
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

    @login_required
    def get(self):
        try:
            return ResponseGenerator('Vil_Sla_Contactpage.html', ) \
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))

    @login_required
    def post(self):
        user = session["user"]
        try:
            
            data = request.form
            # Validate Data
            insert_data = SlaUserQuery(account=user.account, user_name=user.user_name,
                                       user_id=user.user_id, mobile_no=data["mobilenumber"],
                                       email_id=user.email_id, service=data["service"], message=data["message"])
            db.session.add(insert_data)
            db.session.commit()
            message = "Thanks for your feedback."
            return ResponseGenerator('Vil_Sla_Contactpage.html', message=message) \
                .make_success_response()
        except Exception as e:
            logging.error("error@contact", e)
            db.session.rollback()
            return make_response(render_template('404.html', error=e))


class AccountSlaView(Resource):

    @login_required
    def get(self):
        try:
            
            sla_obj = GetSlaDetails()
            sla_details = sla_obj.get_sla_details()
            if not sla_details:
                message = "No Sla is configured. "
                return ResponseGenerator('Vil_Sla_Management_Console.html', message=message) \
                    .make_success_response()
            return ResponseGenerator('Vil_Sla_Management_Console.html',
                                     sla_config_details_with_values=sla_details) \
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))


class ServiceView(Resource):
    @login_required
    def get(self):
        user = session["user"]
        try:
            # all_request = db.session.query(SlaPendingRequests).outerjoin(SlaUserRole,
            # SlaPendingRequests.user_id==SlaUserRole.user_id)\
            #     .filter(SlaUserRole.account == user.account).filter(or_(db.session.query(SlaUserRole.role).filter_by(
            #     user_id = user.user_id).first().role == "approver", SlaPendingRequests.user_id==user.user_id)).all()
            # print(all_request)
            query = f"""select sys_creation_date, activity_id, account, user_id, activity, dynamic_information,
            justification, status from sla_pending_approval where user_id='{user.user_id}'
            and account='vil' union select sys_creation_date , activity_id, account, user_id, activity,
            dynamic_information, justification, status from sla_pending_approval c where c.status='p'
             and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and
             role='approver' and a.user_id='{user.user_id}' and c.dynamic_information like '%' || b.account || '%')
             order by sys_creation_date desc
            """
            all_request = db.session.execute(query).all()
            return ResponseGenerator('Vil_Service_Request_Console.html', requested_service=all_request) \
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))

    @login_required
    def post(self):
        try:
            data = request.form
            raised_request = ActionMap(
                raised_user_id=data["raised_user_id"],
                activity=data["activity"],
                activity_id=data["activity_id"],
                raised_account=data["raised_account"],
                info=data["dynamic_information"],
                remark=data["remarks"],
                action=data["action"]

            )
            message = raised_request.take_action()
            flash(message)
            return redirect('/services')
        except Exception as e:
            return make_response(render_template('404.html', error=e))
            # return "Invalid Request"


class SlaDownloadView(Resource):
    @login_required
    def get(self):
        user = session["user"]
        slas = db.session.query(SlaConfigDetails.sla_number, SlaConfigDetails.sla_description).\
            filter_by(account=user.account, status=0).all()
        if not slas:
            message = "No Sla is configured. "
            return ResponseGenerator('Vil_Sla_Download.html', message=message) \
                .make_success_response()
        return ResponseGenerator('Vil_Sla_Download.html',
                                 sla_number_with_description=slas) \
            .make_success_response()

    @login_required
    def post(self):
        # data = request.form
        flash("SLA download successful. ")
        return redirect('/download_sla')


class AccessControlView(Resource):
    def get(self):
        config_detail = SlaConfigDetail()
        config_details = config_detail.get_config_details()
        return ResponseGenerator('Vil_Sla_Access_Management.html', config_details=config_details, ) \
            .make_success_response()


class RequestsView(Resource):
    def post(self):
        # if current_user.is_authenticated:
        #     user = session["user"]
        try:
            data = request.form
            json_obj = JsonGenerator(form_data=data)
            json_data, request_type = json_obj.generate_json()
            if json_obj.redirect:
                return make_response((redirect('/login')))

            if not current_user.is_authenticated:
                user_account = json_data["account"]
                user_id = json_data["user_id"]
            else:
                user = session["user"]
                user_account = user.account
                user_id = user.user_id
            raise_request = RequestRaised(user_id, user_account, json_data, request_type)
            message = raise_request.handle_request()
            flash(message)
            if current_user.is_authenticated:
                return make_response(redirect("/home"))
            else:
                return make_response((redirect("/login")))

        except Exception as e:
            return make_response(render_template('404.html', error=e))


class Logout(Resource):
    @login_required
    def get(self):
        try:
            logout_user()
            flash("Logout Successful. ")
            return make_response(redirect('/login'))
        except Exception as e:
            return make_response(render_template('404.html', error=e))


class AboutView(Resource):

    @login_required
    def get(self):
        try:
            return ResponseGenerator('Vil_Sla_Aboutpage.html', ) \
                .make_success_response()
        except Exception as e:
            return make_response(render_template('404.html', error=e))


class SlaDashboardView(Resource):
    @login_required
    def get(self):
        today = date.today()
        sla_obj = GetSlaData(today)
        sla_data = sla_obj.get_sla_details()
        for i in sla_data:
            print(i)
        return make_response(render_template("Vil_Sla_Dashboard.html", r=sla_data, dashboard_header=["Hello"]))

    @login_required
    def post(self):
        pass
