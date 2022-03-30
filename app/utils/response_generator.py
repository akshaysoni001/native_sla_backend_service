from flask import make_response, render_template, flash, Response


class ResponseGenerator(Response):
    def __init__(self, html, message=None, config_details="", user_details="", user_accounts="",
                 requested_service='', sla_number_with_description='', sla_config_details_with_values='',
                 reset_ind=''):
        self.html = html
        self.message = message
        self.config_details = config_details
        self.user_details = user_details
        self.user_accounts = user_accounts
        self.requested_service = requested_service
        self.sla_number_with_description = sla_number_with_description
        self.sla_config_details_with_values = sla_config_details_with_values
        self.reset_ind = reset_ind

    def make_success_response(self):
        if self.message:
            flash(self.message, "message")
        return make_response(render_template(self.html, config_details=self.config_details,
                                             user_details=self.user_details, user_accounts=self.user_accounts,
                                             requested_service=self.requested_service,
                                             sla_number_with_description=self.sla_number_with_description,
                                             sla_config_details_with_values=self.sla_config_details_with_values,
                                             reset_ind=self.reset_ind))

    def make_error_response(self):
        if self.message:
            flash(self.message, "error")
        return make_response(render_template(self.html, config_details=self.config_details,
                                             user_details=self.user_details, user_accounts=self.user_accounts,
                                             requested_service=self.requested_service,
                                             sla_number_with_description=self.sla_number_with_description,
                                             sla_config_details_with_values=self.sla_config_details_with_values,
                                             reset_ind=self.reset_ind))
