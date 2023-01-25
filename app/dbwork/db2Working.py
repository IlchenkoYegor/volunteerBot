import os

import psycopg2

from app import config
from datetime import date


class BaseHandler(object):
    #ibm db2
    # def __init__(self, host,port,name , username, passw):
    #     self.conn = ibm_db_dbi.connect('DATABASE={};'
    #                  'HOSTNAME={};'  # 127.0.0.1 or localhost works if it's local
    #                  'PORT={};'
    #                  'PROTOCOL=TCPIP;'
    #                  'UID={};'
    #                  'PWD={};'.format(name,host,port,username,passw), '', '')


    #postgre
    def __init__(self):
        #local
        params = config.config()
        self.conn = psycopg2.connect(**params)
 #       remote
#        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')

    async def insert_or_update_user_info(self, lon, lat, chat_id, city: str):
        #sql = 'select * from location_info';
        print(self, lon, lat, chat_id, city)
        sql = 'insert into chat_location(user_id, latitude, longitude, city_name) values(%s, %s, %s, %s) on conflict (user_id) do update set latitude = %s, longitude = %s, city_name = %s'
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, ([chat_id, lat, lon, city, lat, lon, city]))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            cursor.close()
            s = "city "+city +" is not found"
            raise Exception(s)
        cursor.close()

    async def insert_or_update_participating(self, chat_id):
        sql = 'insert into user_vote(vote_id, date_of_answer, user_id) values(default, default, 454034980)'
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, [chat_id])
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            cursor.close()
            raise Exception
        cursor.close()

    def __del__(self):
        self.conn.close()

# Explicitly bind parameters
