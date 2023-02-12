from datetime import datetime
import time

from generateImg import GenerateImg
from mysql import Mysql

if __name__ == '__main__':
    # items = [[[40, 80], [80, 80], [60, 150], [20, 150], True], [[100, 80], [140, 80], [120, 150], [80, 150], False]]

    i = 1
    while True:
        db = Mysql()
        plan = db.getPlan()
        generateImg = GenerateImg([], plan[0][9], plan[0][10])
        generateImg.drawCorner(plan)

        generateImg.save("./static/plan1.png")

        time.sleep(1)
        i = i * (-1)

