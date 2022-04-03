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
        self.result = True

    def delete_sla(self):
        self.json_dict = {
            'user_id': self.user,
            'application': self.data["application"],
            'account': self.data["account"],
            'sla_number': self.data["sla_number"],
            'sla_description': self.data["sla_description"],
            'sla_type': self.data["sla_type"],
            'reason': self.data["reason"]
        }
        self.request_type = "delete_sla"

    def update_sla(self):
        self.json_dict = {
            'user_id': self.user,
            'application': self.data["application"],
            'account': self.data["account"],
            'sla_number': self.data["sla_number"],
            'sla_description': self.data["sla_description"],
            'sla_type': self.data["sla_type"],
            'target': self.data["target"],
            'penalty': self.data["penalty"],
            'reason': self.data["reason"]
        }
        if self.data["request"] == "add":
            self.request_type = "add_sla"
        else:
            self.request_type = "update_sla"
    
    def registration(self):
        self.json_dict = {
            "account": self.data["account"],
            "name": self.data["name"],
            "user_id": self.data["id"],
            "email_id": self.data["email"],
            "reason": self.data["remark"]
        }
        self.request_type = "registration"

    def access(self):
        self.json_dict = {
            "request_for": self.data["service"],
            "service": self.data.get("account", "rights"),
            "reason": self.data["reason"]
        }
        if self.json_dict["request_for"] == "add_account":
            self.request_type = "Add Account"
        else:
            self.request_type = "User_Rights"

    def generate_json(self):
        if self.data["request"] == "delete":
            self.delete_sla()
        elif self.data["request"] == "update" or self.data["request"] == "add":
            self.update_sla()
        elif self.data["request"] == "access":
            self.access()
        elif self.data["request"] == "signup":
            self.registration()
        else:
            self.message = "Invalid Request"
            self.result = True
        return self.json_dict, self.request_type
