from app import api
from app.views.views import VistaLoginView, VistaHomeView, Logout, ContactView, AccountSlaView, ServiceView, \
    SlaDownloadView, RequestsView, AccessControlView, SlaDashboardView

api.add_resource(SlaDashboardView, '/dashboard')
# api.add_resource(SlaGetView, 'api/sla/<int:sla_id>/')
api.add_resource(SlaDownloadView, '/api/download_sla/<string:account>')
api.add_resource(VistaLoginView, '/api//login')
api.add_resource(VistaHomeView, '/api/home')
api.add_resource(RequestsView, '/api/raise_requests/<string:user>/<string:account>')
api.add_resource(AccessControlView, '/api/access_control')
# api.add_resource(FailedSlaView, '/failed')
api.add_resource(AccountSlaView, '/api/account/<string:account>')
api.add_resource(ServiceView, '/api/requests/<string:user>/<string:account>')
# api.add_resource(ConfigView, '/config')
api.add_resource(ContactView, '/api/contact/<string:user>/<string:account>')
api.add_resource(Logout, '/logout')
