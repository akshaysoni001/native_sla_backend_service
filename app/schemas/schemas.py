from marshmallow import Schema, fields


class SlaUserManagementSchema(Schema):
    user_id = fields.String(required=True)
    user_name = fields.String(required=True)
    email_id = fields.Url(required=True)
    password = fields.String(required=True)
    status = fields.Boolean(required=False)
    reset_ind = fields.Boolean(required=False)
    attempt = fields.Boolean(required=False)


user_schema = SlaUserManagementSchema()


class SlaUserRoleSchema(SlaUserManagementSchema):
    account = fields.String(required=True)
    role = fields.String(required=True)


user_role_schema = SlaUserRoleSchema()


class SlaPendingRequestsSchema(Schema):
    account = fields.String(required=True)
    user_id = fields.String(required=True)
    activity = fields.String(required=True)
    info = fields.String(required=True)
    justification = fields.String(required=True)
    remark = fields.String(required=False)
    status = fields.Boolean(required=False)


pending_request_schema = SlaPendingRequestsSchema()


class SlaUserQuerySchema(Schema):
    account = fields.String(required=True)
    user_name = fields.String(required=True)
    user_id = fields.String(required=True)
    mobile_no = fields.Number(required=True, Length=10)
    email_id = fields.Url(required=True)
    service, message = fields.String(required=True)


sla_user_query_schema = SlaUserQuerySchema()


class SlaConfigParamSchema:
    activity_id = fields.Integer(required=True)
    param_type = fields.String(required=True)
    param_account = fields.String(required=True)
    param_name = fields.String(required=True)
    param_value = fields.String(required=True)
    status = fields.Integer(required=True)


sla_config_param_schema = SlaConfigParamSchema()


class SlaConfigSchema:
    sla_id = fields.Integer(required=True)
    account = fields.String(required=True)
    application = fields.String(required=True)
    sla_number = fields.Integer(required=True)
    sla_description = fields.String(required=True)
    frequency = fields.String(required=True)
    level_type = fields.String(required=True)
    sla_type = fields.String(required=True)
    target = fields.Integer(required=True)
    weightage = fields.Integer(required=True)
    penalty = fields.Boolean(required=True)
    circle_level_sla = fields.Boolean(required=True)
    table_name = fields.String(required=True)
    sla_cal_condition = fields.String(required=True)
    status = fields.Boolean(required=True)
    user_id = fields.String(required=True)
    indicator = fields.String(required=True)


sla_config_details_schema = SlaConfigSchema()
