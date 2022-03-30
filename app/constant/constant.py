from app.models.models import SlaConfigDetails, SlaUserManagement, SlaUserRole
action_map = {
    "delete_sla": SlaConfigDetails,
    "add_sla": SlaConfigDetails,
    "update_sla": SlaConfigDetails,
    "registration": SlaUserManagement,
    "add_account": SlaUserRole,
    "access_control": SlaUserRole
}

mail_workflow = {
        "approve": "approval_mail",
        "reject": "rejection_mail",
        "registration": "registration_details",
        "request_raised": "self._request_raised",
        "password_reset": "password_reset"
}
