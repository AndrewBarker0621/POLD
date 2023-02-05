import time

from create_parking_2D_mysql import DBS

#if __name__ == '__main__':
#    upload = DBS('coordinates.yml')
#    upload.create()

#    while True:
#        with open("coor.txt", "r") as f:
#            ls = []
#            for line in f.readlines():
#                line = line.strip('\n')
#                strls = line.split(", ")

#                i = 0
#                intls = []
#                while i < len(strls):
#                    intls.append(int(strls[i]))
#                    i = i + 1

#                ls.append(intls)

#       print(ls)

#        if upload.empty():
#            upload.insert(ls)
#            print('insert')

#        else:
#            upload.update(ls)
#            print('update')

#        time.sleep(5)
