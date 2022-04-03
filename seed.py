from datetime import date

from app import db
from app.models.models import SlaGlobalConfiguration, SlaUserManagement, SlaUserRole, SlaConfigDetails, \
    SlaPendingRequests, \
    SlaDataModel


def seed_global_configuration():
    db.session.add(SlaGlobalConfiguration(type='account', account='maxico', sub_type='applications',
                                          value='python,flask,django,docker'))
    db.session.add(SlaGlobalConfiguration(type='sla_type', account='maxico', sub_type='sla_download', value='D-1, TILL_DATE, LAST_MONTH, LAST_3MONTHS, LAST_6MONTHS'))
    db.session.add(SlaGlobalConfiguration(type='email',account='all',sub_type='sender',value='akshaysoni460@gmail.com'))
    db.session.add(SlaGlobalConfiguration(type='account',account='usa',sub_type='extension',value='United State'))
    db.session.add(SlaGlobalConfiguration(type='account', account='maxico', sub_type='extension', value='Maxico'))
    db.session.add(SlaGlobalConfiguration(type='account',account='uk',sub_type='extension',value='United Kingdom'))
    db.session.add(SlaGlobalConfiguration(type='email',account='all',sub_type='recipient',value='akshaysoni460@gmail.com'))
    db.session.add(SlaGlobalConfiguration(type='email',account='all',sub_type='domain',value='@abc.com'))



def sla_config_details():
    db.session.add(SlaConfigDetails(account='maxico',application='python', sla_number=11,sla_description='Python Native SLA For Threshold',
                                    sla_type='monthly',target=100,penalty=False))

    db.session.add(SlaConfigDetails(account='maxico', application='python', sla_number=12,
                                    sla_description='Python Native SLA For Threshold',
                                    sla_type='daily', target=100, penalty=False))
    db.session.add(SlaConfigDetails(account='uk', application='docker', sla_number=11,
                                    sla_description='Docker Native SLA For Frequecy(uk)',
                                    sla_type='weekly', target=90, penalty=False))
    db.session.add(SlaConfigDetails(account='usa', application='django', sla_number=91,
                                    sla_description='Django Native SLA For Monitoring(usa)',
                                    sla_type='weekly', target=70, penalty=False))
    db.session.add(SlaConfigDetails(account='usa', application='flask', sla_number=90,
                                    sla_description='Flask Native SLA For Development(usa)',
                                    sla_type='monthly', target=75, penalty=True))


def sla_user_management():
    db.session.add(SlaUserManagement('Admin User','admin', 'admin@abc.com', 'pbkdf2:sha256:150000$R9C4k2s5$c3fcffa2aa15dcfaaf260bb9d693f259b8559e72150fe3c83249799755ea23bf',0,0,0))
    db.session.add(SlaUserManagement('Guest User', 'guest', 'akshaysoni460@gmail.com',
                                     "pbkdf2:sha256:150000$OlqR2npc$4f3264f113f2c62d8610bb0801b830ff0db4f1494bb06b1d5531ce9aa29f0fb0",
                                     0, 0, 0))


def sla_user_role():
    db.session.add(SlaUserRole(user_id="admin",account='maxico',role='manager'))
    db.session.add(SlaUserRole(user_id="guest", account='maxico', role='default'))


def seed_sla_data():
    db.session.add(SlaDataModel(account='maxico',application="python",sla_date=date.today(),sla_number=12,sla_type='monthly',total_reqeust=2000,within_sla_reqeust=1600,sla_percentage=70,sla_met=True))


def remaing():
    db.session.add(SlaGlobalConfiguration(type='account', account='maxico', sub_type='manager',
                                          value='Akshay Soni'))


def seed_data():
    try:
        sla_user_management()
        sla_user_role()
        seed_global_configuration()
        # # sla_pending_request()
        sla_config_details()
        seed_sla_data()
        # remaing()
        db.session.commit()

    except Exception as e:
        # logger.exception(e)
        print("Error: ", e)
        db.session.rollback()


seed_data()
