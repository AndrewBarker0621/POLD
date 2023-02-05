import re
import sys
import pymysql as mysql
import yaml
import pandas as pd
import numpy as np


class DBS:

    def __init__(self, path):

        self.path = path
        self.db = mysql.connect(host='liparkdb.cvuwuyaiiqgl.ap-southeast-2.rds.amazonaws.com', user='admin',
                           password='transportlab', database='LiDAR_Parking', charset='utf8')
        self.cursor = self.db.cursor()

    def clean(self):        
        try:
            self.cursor.execute("delete * from parking_2D")
            self.db.commit()

        except Exception as e:
            print(str(e))
            self.db.rollback()

    def insert(self, list):
        for park in list:
            sql_write = "insert into park_2D(Id, TL_x, TL_y, TR_x, TR_y, BR_x, BR_y, BL_x, BL_y, width, height, status) values('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" % (park[0], park[1], park[2], park[3], park[4], park[5], park[6], park[7], park[8], park[9], park[10], park[11])
            try:
                self.cursor.execute(sql_write)
                self.db.commit() # process
            except Exception as e:
                self.db.rollback() # rollback
                print(str(e))

    def update(self, list):
        for park in list:
            try:
                self.cursor.execute('''
                                UPDATE park_2D
                                SET status = '%d'
                                WHERE Id = '%d'
                                ''' % (park[11], park[0]))

                self.db.commit()

            except Exception as e:
                print(str(e))
                self.db.rollback()

    def empty(self):
        sql = 'select * from park_2D'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        if len(results) == 0:
            return True
        else:
            return False

