from app import api
from app.views.views import VistaLoginView, VistaHomeView, Logout, ContactView, AccountSlaView, ServiceView, \
    SlaDownloadView, RequestsView, AccessControlView, AboutView, SlaDashboardView

api.add_resource(SlaDashboardView, '/dashboard')
# api.add_resource(SlaGetView, 'api/sla/<int:sla_id>/')
api.add_resource(SlaDownloadView, '/download_sla')
api.add_resource(VistaLoginView, '/login')
api.add_resource(VistaHomeView, '/home')
api.add_resource(RequestsView, '/raise_requests')
api.add_resource(AccessControlView, '/access_control')
# api.add_resource(FailedSlaView, '/failed')
api.add_resource(AccountSlaView, '/account')
api.add_resource(ServiceView, '/services')
# api.add_resource(ConfigView, '/config')
api.add_resource(ContactView, '/contact')
api.add_resource(AboutView, '/about')
api.add_resource(Logout, '/logout')
