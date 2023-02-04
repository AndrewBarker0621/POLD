import numpy as np
import os
import cv2

def xywh2xyxy(lp):
    fileList = os.listdir(lp)
    for fileName in fileList:
        fileLabel = open(lp + fileName, "r+")
        imgName = fileName.split(".")[0] + ".jpg"
        print("pic_name: {}".format(imgName))
        imagePath = "/Users/rzen0142/Downloads/pi/picture/" + imgName
        print("pic_address: {}".format(imagePath))
        img = cv2.imread(imagePath)
        h_img, w_img = img.shape[:2]
        print("width:{}\t height:{}".format(w_img, h_img))
        
        with open(fileLabel.name, 'r+', encoding='utf-8') as f:
            bbox = np.zeros([len(f.readlines()),5])
        
        with open(fileLabel.name, 'r+', encoding='utf-8') as f:
            row = 0
            for line in f.readlines():
                info = line[:-1].split(',')
                kind = info[0].split(" ")[0]
                if (int(kind) == 2) | (int(kind) == 5) | (int(kind) == 7):
                    bbox[row,0] = int(kind)   # object type
                    cenX = float(info[0].split(" ")[1])
                    cenY = float(info[0].split(" ")[2])
                    wide = float(info[0].split(" ")[3])
                    high = float(info[0].split(" ")[4].split()[0])
                    # anti-normalization
                    x_t = cenX * w_img
                    y_t = cenY * h_img
                    w_t = wide * w_img
                    h_t = high * h_img
                    # save into bbox
                    bbox[row,1] = x_t - w_t / 2    # x_lefttop
                    bbox[row,2] = y_t - h_t / 2    # y_leftbottom
                    bbox[row,3] = x_t + w_t / 2    # x_righttop
                    bbox[row,4] = y_t + h_t / 2    # y_rightbottom
                    row = row + 1
                else:
                    continue
        bbox = bbox[[not np.all(bbox[i] == 0) for i in range(bbox.shape[0])], :]
        newDetPath = "/Users/rzen0142/Downloads/pi/ground_truth/" + imgName
        for i in range(len(bbox)):
            cv2.rectangle(img, (int(bbox[i,1]), int(bbox[i,2])), (int(bbox[i,3]), int(bbox[i,4])), (0, 255, 0), 2)
            cv2.imwrite(newDetPath, img)

if __name__ == "__main__":
    
    label_path = '/Users/rzen0142/Downloads/pi/label/'
    xywh2xyxy(label_path)