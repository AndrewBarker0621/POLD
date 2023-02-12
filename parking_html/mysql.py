import pymysql
from datetime import datetime


class Mysql(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='liparkdb.cvuwuyaiiqgl.ap-southeast-2.rds.amazonaws.com', user='admin',
                                        password='transportlab', database='LiDAR_Parking', charset='utf8')
            print("Succeed")
        except:
            print("Failed")

        self.table_list = []

    def getPlan(self):
        margin = 40
        cursor = self.conn.cursor()

        sql = 'select * from park_2D'
        cursor.execute(sql)
        results = cursor.fetchall()
        self.table_list = []
        for r in results:
            self.table_list.append(list(r))

        sql = 'select * from park_3D'
        cursor.execute(sql)
        result_3D = cursor.fetchall()
        for r_3D in result_3D:
            format_r_3D = list(r_3D)
            format_r_3D[1] = format_r_3D[1] + self.table_list[0][10] + margin
            format_r_3D[3] = format_r_3D[3] + self.table_list[0][10] + margin
            format_r_3D[5] = format_r_3D[5] + self.table_list[0][10] + margin
            format_r_3D[7] = format_r_3D[7] + self.table_list[0][10] + margin
            self.table_list.append(format_r_3D)

        cursor.close()

        return list(self.table_list)

