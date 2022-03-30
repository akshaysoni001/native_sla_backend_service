from flask import make_response, flash, render_template
from flask_restful import Resource
from app.utils.requests import ChangePassword, ResetPassword
from app import session
from flask_login import current_user


class JsonGenerator(Resource):
    def __init__(self, form_data, user=None, account=None):
        self.data = form_data
        self.user = user
        self.account = account
        self.request_type = None
        self.json_dict = None
        self.message = None
        self.redirect = False

    def delete_sla(self):
        self.json_dict = {
            'user_id': self.user,
            'application': self.data["application"],
            'account': self.account,
            'sla_number': self.data["sla_number"],
            'sla_description': self.data["sla_description"],
            'sla_type': self.data["sla_type"],
            'justification': self.data["remark"]

        }
        self.request_type = "delete_sla"

    def update_sla(self):
        self.json_dict = {
            'user_id': self.user,
            'application': self.data["application"],
            'account': self.account,
            'sla_number': self.data["sla_number"],
            'sla_description': self.data["sla_description"],
            'frequency': self.data["frequency"],
            'level_type': self.data["level_type"],
            'sla_type': self.data["sla_type"],
            'target': self.data["target"],
            'weightage': self.data["weightage"],
            'penalty': self.data["penalty"],
            'circle_level_sla': self.data["circle_level_sla"],
            'table_name': self.data["table_name"],
            'sla_cal_condition': self.data["sla_cal_condition"],
            'indicator': self.data["indicator"],
            'status': self.data["status"],
            'justification': self.data["remark"]
        }
        if self.data["request"] == "add":
            self.request_type = "add_sla"
        else:
            self.request_type = "update_sla"
    
    def registration(self):
        self.json_dict = {
            "account": self.data["account"],
            "name": self.data["name"],
            "user_id": self.data["username"],
            "email_id": self.data["email"],
            "justification": self.data["remark"]
        }
        self.request_type = "registration"

    def access(self):
        self.json_dict = {
            "request_for": self.data["service"],
            "service": self.data.get("account", "rights"),
            "justification": self.data["remark"],
            "check": self.data["check"]
        }
        if self.json_dict["request_for"] == "add_account":
            self.request_type = "Add Account"
        else:
            self.request_type = "User_Rights"
    
    def reset_password(self):
        print("reset")
        pass_obj = ResetPassword(self.data["username"])
        self.message = pass_obj.reset_password()
        flash(self.message)
        self.redirect = True
        # return make_response(redirect('/login'))
    
    def change_password(self):
        obj = ChangePassword(user_id=self.user.user_id, old_password=self.data["oldpassword"],
                             new_password=self.data["newpassword"])
        self.message = obj.change_password()
        flash(self.message)
        self.redirect = True

    def generate_json(self):
        if self.data["request"] == "delete":
            self.delete_sla()
        elif self.data["request"] == "update" or self.data["request"] == "add":
            self.update_sla()
        elif self.data["request"] == "access":
            self.access()
        elif self.data["request"] == "signup":
            self.registration()
        elif self.data["request"] == "reset_password":
            self.reset_password()
        elif self.data["request"] == "change_password":
            self.change_password()
        else:
            self.message = "Invalid Request"
            return make_response(render_template('404.html', error=self.message))
        return self.json_dict, self.request_type
