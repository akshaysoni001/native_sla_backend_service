from datetime import date

from app import db
from app.models.models import SlaConfigParam, SlaUserManagement, SlaUserRole, SlaConfigDetails, SlaPendingRequests, \
    SlaDataModel


def sla_config_param():
    db.session.add(SlaConfigParam(1, 'sla_type', 'vil', 'sla_download', 'D-1, TILL_DATE, LAST_MONTH, LAST_3MONTHS, LAST_6MONTHS', 0))
    db.session.add(SlaConfigParam(2,'email','all','sender','vistasupportteam@abc.com',0))
    db.session.add(SlaConfigParam(57,'account','CALA','extension','Claro Chile',0))
    db.session.add(SlaConfigParam(86,'account','Opero','extension','vil',0))
    db.session.add(SlaConfigParam(3,'email','all','recipent','akshaysoni460@gmail.com',0))
    db.session.add(SlaConfigParam(99,'email','all','domain','@abc.com',0))



def sla_config_details():
    db.session.add(SlaConfigDetails('vil','RATER', 2,'PROCESSED CDRS AS A PERCENTAGE OF TOTAL CDRS (NUMBER OF SUCCESSFULLY PROCESSED CDRS AS A PERCENTAGE OF TOTAL CDRS) FOR EACH CYCLE.',
                                    'MONTHLY','CRITICAL',None,99.9999,2,True,False,'sla_data_manager_daily',None,False,None,'%'))
    db.session.add(SlaConfigDetails('vil','RATER',41,'TIMELINESS IN RATING/UPLOADING OF CDRS WITHIN DEFINED TIME OF RECEIPT FROM MEDIATION','MONTHLY','CRITICAL','60_MIN',95.79,3,True,False,'sla_data_manager_daily',None,False,None,'%'))
    db.session.add(SlaConfigDetails('vil','INV',61,'SUBSCRIBER BILLING ACCURACY','MONTHLY','CRITICAL',None,99.999,6,True,False,'sla_data_manager_daily',None,False,None,'%'))
    db.session.add(SlaConfigDetails('vil','INV',10,'BILL PROCESSING (PS/PDF HANDOVER - FULL EXTRACT + EBPP+ CONFIRMATION) ','MONTHLY','CRITICAL',None,11,61,True,False,'sla_data_manager_daily',None,False,None,None))
    db.session.add(SlaConfigDetails('vil','CL',11,'TIMELY GENERATION OF DUNNING EXTRACTS','MONTHLY','CRITICAL','09_AM',21,31,True,False,'sla_data_manager_daily',None,False,None,None))
    # db.session.add(SlaConfigDetails(288,'vil','INFRA',18,'APPLICATIONS AVAILABILITY','MONTHLY','CRITICAL',None,99.7,3,True,False,'sla_data_manager_daily',None,False,None,'%'))


def sla_user_management():
    db.session.add(SlaUserManagement('Administration','admin', 'admin@abc.com', 'pbkdf2:sha256:150000$R9C4k2s5$c3fcffa2aa15dcfaaf260bb9d693f259b8559e72150fe3c83249799755ea23bf',0,0,0))


def sla_user_role():
    db.session.add(SlaUserRole("admin",'vil','approver',0))


def sla_pending_request():
    db.session.add(SlaPendingRequests('Vil','akshason','registration','{"account": "vil", "user_name": "Ayushi Tugnawat", "user_id": "akshason", "EMAIL_ID": "akshaysoni460"}','testing','pending','o'))


def seed_sla_data():
    db.session.add(SlaDataModel('VIL',date.today(),12,'09_AM',2,2,10,0))


def seed_data():
    try:
        sla_user_management()
        sla_user_role()
        sla_config_param()
        # # sla_pending_request()
        sla_config_details()
        seed_sla_data()
        db.session.commit()

    except Exception as e:
        # logger.exception(e)
        print("Error: ", e)
        db.session.rollback()


seed_data()
