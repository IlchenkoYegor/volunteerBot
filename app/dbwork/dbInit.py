from app.dbwork import db2Working
from create_bot import config

#ibmdb2
# db_handler = db2Working.BaseHandler(config.get("db", "database_ip"),
#                                     config.get("db", "database_port"),
#                                     config.get("db", "database_db2_name"),
#                                     config.get("db", "database_db2_login"),
#                                     config.get("db", "database_db2_password"))

db_handler = db2Working.BaseHandler()