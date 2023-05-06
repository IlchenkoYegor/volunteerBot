import os

import psycopg2

from app import config
from datetime import date


class BaseHandler(object):

    def __init__(self):
        # local
        params = config.config()
        self.conn = psycopg2.connect(**params)

    #       remote
    #        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')

    async def insert_or_update_user_info(self, lon, lat, chat_id, city: str):
        print(self, lon, lat, chat_id, city)
        sql = 'insert into chat_location(user_id, latitude, longitude, city_name,has_poll_invitation) values(%s, %s, %s, %s, false) on conflict (user_id) do update set latitude = %s, longitude = %s, city_name = %s'
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, ([chat_id, lat, lon, city, lat, lon, city]))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            cursor.close()
            s = "city " + city + " is not found"
            raise Exception(s)
        cursor.close()

    async def insert_or_update_participating(self, chat_id):
        sql = "insert into user_vote(vote_id, date_of_answer, user_id) values(default, default, %s)"
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, [chat_id])
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            cursor.close()
            raise Exception
        cursor.close()

    async def get_time_of_city(self, chat_id):
        sql = 'select time from time_of_aid where city_id = (select city_name from chat_location where user_id = %s)'
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, [chat_id])
            res = cursor.fetchone()
            print(res[0])
        except Exception:
            self.conn.rollback()
            cursor.close()
            raise Exception
        cursor.close()
        return res[0]

    def __del__(self):
        self.conn.close()
