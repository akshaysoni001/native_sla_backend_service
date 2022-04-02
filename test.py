# import datetime
#
# from werkzeug.security import check_password_hash, generate_password_hash
#
# from app import db
# from app.models.models import *
# from sqlalchemy import cast, String, or_,and_
# from sqlalchemy.types import Unicode
# from sqlalchemy.dialects.mssql import try_cast
# # user_data = db.session.query(SlaUserManagement, SlaUserRole).outerjoin(SlaUserRole, SlaUserManagement.id==SlaUserRole.id).filter(
# #     SlaUserManagement.user_id == "akshason").first()
# # print(user_data[0].user_id)
# # print(user_data[1].role)
# #
# # user_data = db.session.query(SlaUserManagement.id,
# #                              SlaUserRole.account).outerjoin(SlaUserRole, SlaUserManagement.user_id==SlaUserRole.user_id).filter(
# #     SlaUserManagement.user_id == "akshay", SlaUserRole.account=="Claro Chile").first()
# #
# # # x = db.session.query(SlaUserManagement.user_id, SlaUserRole.account).outerjoin(SlaUserRole, SlaUserManagement.id==SlaUserRole.id)
# # # .filter(SlaUserManagement.user_id == "akshay", SlaUserRole.account="Claro Chile").first()
# # print(user_data)
# # # print(x)
# # # print(user_data)
# # x = db.session.query(SlaPendingRequests.dynamic_information).filter_by(user_id="sonson", activity="update_sla").first()
# # y={ status :  0 ,  target :  100 ,  account :  vil ,  penalty :  True ,  user_id :  akshason ,  sla_type :  None ,  frequency :  MONTHLY ,  indicator :   ,  weightage :  3 ,  level_type :  CRITICAL ,  sla_number :  18 ,  table_name :  sla_data_manager_daily ,  justification :  test ,  sla_description :  APPLICATIONS AVAILABILITY ,  circle_level_sla :  False ,  sla_cal_condition :  None }
# # # z={ status :  0 ,  target :  100 ,  account :  vil ,  penalty :  True ,  user_id :  akshason ,  sla_type :  None ,  frequency :  MONTHLY ,  indicator :  ... (88 characters truncated) ... ata_manager_daily ,  justification :  test ,  sla_description :  APPLICATIONS AVAILABILITY ,  circle_level_sla :  False ,  sla_cal_condition :  None }
# # print(x[0])
# # print(y)
# # if x[0] == y:
# #     print(True)
# # pending_request = db.session.query(SlaPendingRequests).filter(
# #     SlaPendingRequests.dynamic_information[0] == x
# # ).first()
# # print(pending_request.dynamic_information)
#
#
# # x = ( sla_id= , 100,  account=VIL ,  application=RATER ,  sla_number=2 ,  sla_description=PROCESSED CDRS AS A PERCENTAGE OF TOTAL CDRS (NUMBER OF SUCCESSFULLY PROCESSED CDRS AS A PERCENTAGE OF TOTAL CDRS) FOR EACH CYCLE. ,  frequency=MONTHLY ,  level_type=CRITICAL ,  sla_type=None ,  target=100 ,  weightage=2 ,  penalty=True ,  circle_level_sla=False ,  table_name=sla_data_manager_daily ,  sla_cal_condition=None ,  status=0 ,  user_id=sonson ,  indicator= )
# # obj = SlaConfigDetails(sla_id=1000, account=  'VIL' , application='RATER',sla_number= '2' ,sla_description=  'PROCESSED CDRS AS A PERCENTAGE OF TOTAL CDRS (NUMBER OF SUCCESSFULLY PROCESSED CDRS AS A PERCENTAGE OF TOTAL CDRS) FOR EACH CYCLE.' ,  frequency='MONTHLY ',  level_type='CRITICAL' ,  sla_type='None' ,  target='100' ,  weightage='2' , penalty=   True , circle_level_sla= False ,  table_name='sla_data_manager_daily' ,  sla_cal_condition='None' ,  status=0 ,  user_id='sonson', indicator='')
# # print(obj)
# # db.session.add(obj)
# # db.session.commit()
# # print("Done")
# # from dateutil.parser import parse
# # from sqlalchemy import and_
# # slas = db.session.query(SlaConfigDetails.sla_number, SlaConfigDetails.sla_description).filter_by(account='VIL',
# #                                                                                                  status=0).filter(and_(SlaConfigDetails.sys_creation_date >= parse('18 February 2022'))).all()
# # # sys_creation_date=parse('18 February 2022')).all()
# # print(parse('08 February 2022'))
# # print(slas)
# # dt = datetime.strptime('08 February 2022', 'DD Mon YYYY')
# # print(dt)
#
# #
# # obj=SlaUserManagement(
# #                 user_name='Soni',
# #                 user_id='Soniiii',
# #                 email_id='soni@abc',
# #                 password="abc"
# #             )
# # print("before")
# # db.session.add(obj)
# # db.session.commit()
# # print("done")
#
# #TODO: Mail Sender and Message Genrator  ==> Done
# # & optimization and set_parameter and Schema Validation ==>
#
# # TODO: last working on dashboard
#
# # mail_user = db.session.query(SlaUserManagement.user_name,SlaUserManagement.email_id).filter_by(user_id='akshason').first()
# # print(mail_user.user_name,mail_user.email_id)
# # usr = db.session.query(SlaUserManagement).\
# #             filter_by(user_id='akshay').first()
# # result = check_password_hash(usr.password, '3441om8m')
# # if not result:
# #     print("Invalid Old Password")
# # # hash_pass = generate_password_hash("Rama#1234")
# # # print(hash_pass)
# # # usr.password = 'Soni'
# # # db.session.commit()
# #
# #
# # user_data = db.session.query(SlaUserManagement.id,
# #                                          SlaUserManagement.user_name,
# #                                          SlaUserManagement.user_id,
# #                                          SlaUserManagement.email_id,
# #                                          SlaUserManagement.status,
# #                                          SlaUserManagement.password,
# #                                          SlaUserManagement.attempt,
# #                                          SlaUserManagement.reset_ind,
# #                                          SlaUserRole.account,
# #                                          SlaUserRole.role).outerjoin(SlaUserRole,
# #                                                                      SlaUserManagement.user_id == SlaUserRole.user_id).\
# #                 filter(
# #                 SlaUserManagement.user_id == "akshason", SlaUserRole.account == "vil").first()
# #
# # print(user_data)
# # user_obj = db.session.query(SlaUserManagement).filter_by(user_id="akshason").first()
# # print(user_obj)
# from app.utils.config import GetSlaData
# # from datetime import date
# # from sqlalchemy import func
# #
# # today = date.today()
# # sla_data = db.session.query(SlaDataModel).filter(func.date(SlaDataModel.sla_date) == date.today()).all()
# #
# # for i in sla_data:
# #     print(i.sla_number)
# #
# #
# # row[i][0] ==123
# # row[i] = 1000
#
#
# # user_data = db.session.query(SlaUserManagement.id,
# #                                          SlaUserManagement.user_name,
# #                                          SlaUserManagement.user_id,
# #                                          SlaUserManagement.email_id,
# #                                          SlaUserManagement.status,
# #                                          SlaUserManagement.password,
# #                                          SlaUserManagement.attempt,
# #                                          SlaUserManagement.reset_ind,
# #                                          SlaUserRole.account,
# #                                          SlaUserRole.role).outerjoin(SlaUserRole,
# #                                                                      SlaUserManagement.user_id == SlaUserRole.user_id).\
# #                 filter(
# #                 SlaUserManagement.user_id == " admin", SlaUserRole.account == "vil").first()
# #
# # x = db.session.query(SlaUserManagement).filter_by(user_id=" admin").first()
# # print(x.user_id)
# # print(user_data)
#
#
# # obj = db.session.query(SlaUserManagement.email_id, SlaUserManagement.user_name)\
# #     .outerjoin(SlaUserRole, SlaUserManagement.user_id==SlaUserRole.user_id)\
# #     .filter(SlaUserRole.role=="approver", SlaUserRole.account=="vil",SlaUserManagement.deleted==False).first()
# #
# # print(obj.email_id)
# #
# #
# # # print(generate_password_hash("admin"))
# # # print(check_password_hash('admin','pbkdf2:sha256:150000$bkeMYIk2$a502b9fb94215abdef209f7d34b479d8eda90f84e137166630ee0c8ccdc7236c'))
# #
# # # sla_obj = db.session.query(SlaConfigDetails).filter_by(
# # #                 account='vil', application="aam", sla_number=2)
# # # sla_obj.deleted = True
# # x="SELECT SYS_CREATION_DATE, ACTIVITY_ID, ACCOUNT, USER_ID, ACTIVITY, DYNAMIC_INFORMATION, JUSTIFICATION, STATUS FROM SLA_PENDING_APPROVAL WHERE USER_ID='{user.user_id}' AND ACCOUNT='VIL'\
# #                                 UNION\
# #                                 SELECT SYS_CREATION_DATE , ACTIVITY_ID, ACCOUNT, USER_ID, ACTIVITY, DYNAMIC_INFORMATION, JUSTIFICATION, STATUS FROM SLA_PENDING_APPROVAL C WHERE C.STATUS='P'\
# #                                 AND EXISTS (SELECT  A.* FROM SLA_USER_MANAGEMENT A, SLA_USER_ROLE B WHERE A.ID = B.ID AND ROLE='approver' AND A.USER_ID='{user.user_id}'\
# #                                 AND C.DYNAMIC_INFORMATION LIKE '%' || b.ACCOUNT || '%') ORDER BY SYS_CREATION_DATE DESC"
# # print(x.lower())
# #
# # "select sys_creation_date, activity_id, account, user_id, activity, dynamic_information, justification, status from sla_pending_approval where user_id='{user.user_id}' and account='vil' union select sys_creation_date , activity_id, account, user_id, activity, dynamic_information, justification, status from sla_pending_approval c where c.status='p' and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and role='approver' and a.user_id='{user.user_id}' and c.dynamic_information like '%' || b.account || '%') order by sys_creation_date desc"
#
# # obj = db.session.query(SlaPendingRequests).union(SlaUserRole, SlaPendingRequests.account==SlaUserRole.account)\
# #                 .filter(SlaUserRole.account == "vil").filter(or_(SlaUserRole.role=="approver", SlaPendingRequests.user_id=='admin')).all()
# # print(obj)
#
# all_request = db.session.query(SlaPendingRequests).outerjoin(SlaUserRole, SlaPendingRequests.account==SlaUserRole.account)\
#                 .filter(SlaUserRole.account == 'vil').filter(or_(db.session.query(SlaUserRole.role).filter_by(
#                 user_id = 'admin').first().role == "approver", SlaPendingRequests.user_id=='admin')).all()
# role = db.session.query(SlaUserRole.role).filter_by(user_id = 'admin').first()
# print(all_request)
#
# print(role.role)

# from app import db
# query = f"""select sys_creation_date, activity_id, account, user_id, activity, dynamic_information,
# justification, status from sla_pending_approval where user_id='admin'
# and account='vil' union select sys_creation_date , activity_id, account, user_id, activity,
# dynamic_information, justification, status from sla_pending_approval c where c.status='p'
#  and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and
#  role='approver' and a.user_id='admin' and c.dynamic_information like '%' || b.account || '%')
#  order by sys_creation_date desc
# """
# all_request = db.session.execute(query).all()
# print(all_request)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.models import SlaConfigDetails, SlaPendingRequests
from app import db
#
# sla_details = db.session.query(SlaConfigDetails).filter_by(status=0,
#                                                                        account='vil', deleted=False).all()
# print(sla_details)
# for sla in sla_details:
#     print(sla.id)

# query = f"""select sys_creation_date, activity_id, account, user_id, activity, dynamic_information,
#             justification, status from sla_pending_approval where user_id='admin'
#             and account='vil' union select sys_creation_date , activity_id, account, user_id, activity,
#             dynamic_information, justification, status from sla_pending_approval c where c.status='p'
#              and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and
#              role='approver' and a.user_id='admin' and c.dynamic_information like '%' || b.account || '%')
#              order by sys_creation_date desc
#             """
#
# all_request = db.session.execute(query).all()
# print(all_request)

# slas = db.session.query(SlaConfigDetails.sla_number, SlaConfigDetails.sla_description).\
#             filter_by(account='vil', status=0).all()
#
# for sla in slas:
#     print(sla[1])
# x= generate_password_hash('admin')
# result = check_password_hash(x, 'adin')
# print(result)
# import jwt
# from flask import jsonify
# from datetime import datetime, timedelta
# token = jwt.encode({
#     'user':'admin',
#     # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
#     'expiration': str(datetime.utcnow() + timedelta(seconds=60))
# },
#     'hello')
#
# print(token)
# print(token.decode('utf-8'))

# query = """select sys_creation_date, activity_id, account, user_id, activity, dynamic_information,
#             justification, status from sla_pending_approval where user_id='admin'
#             and account='vil' union select sys_creation_date , activity_id, account, user_id, activity,
#             dynamic_information, justification, status from sla_pending_approval c where c.status='p'
#              and exists (select  a.* from sla_user_management a, sla_user_role b where a.id = b.id and
#              role='approver' and a.user_id='admin' and c.dynamic_information like '%' || b.account || '%')
#              order by sys_creation_date desc"""
# all_request = db.session.execute(query).all()
# print(all_request)

pending_request = db.session.query(SlaPendingRequests).filter_by(
            activity_id=12
        ).first()
print(pending_request)

