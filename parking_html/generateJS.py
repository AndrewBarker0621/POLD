import json
import time

from mysql import Mysql

if __name__ == '__main__':
    while True:
        try: 
            db = Mysql()
            plan = db.getPlan()
            title = ['id', 'tl_x', 'tl_y', 'tr_x', 'tr_y', 'br_x', 'br_y', 'bl_x', 'bl_y', 'width', 'height', 'status']

            plan_info = {}
            json_data = json.loads(json.dumps(plan_info))

            json_txt = {
                'parking': []
            }

            json_data['data'] = json_txt

            plan_js = []
            for parking in plan:
                parking_info = {}
                i = 0
                while i < len(title):
                    parking_info[title[i]] = parking[i]
                    i = i + 1
                plan_js.append(parking_info)

            json_txt['parking'] = plan_js
            
            with open("./templates/data.json", "w") as f: 
                json.dump(plan_js, f)
            time.sleep(0.2)
        except:
            time.sleep(1)
            db = Mysql()
            plan = db.getPlan()
            title = ['id', 'tl_x', 'tl_y', 'tr_x', 'tr_y', 'br_x', 'br_y', 'bl_x', 'bl_y', 'width', 'height', 'status']

            plan_info = {}
            json_data = json.loads(json.dumps(plan_info))

            json_txt = {
                'parking': []
            }

            json_data['data'] = json_txt

            plan_js = []
            for parking in plan:
                parking_info = {}
                i = 0
                while i < len(title):
                    parking_info[title[i]] = parking[i]
                    i = i + 1
                plan_js.append(parking_info)

            json_txt['parking'] = plan_js
            
            with open("./templates/data.json", "w") as f: 
                json.dump(plan_js, f)
            time.sleep(0.2)
