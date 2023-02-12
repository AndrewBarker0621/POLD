from PIL import ImageDraw, Image, ImageFont
import matplotlib.pyplot as plt


class GenerateImg:

    def __init__(self, item, width, height):
        self.item = item
        self.im = Image.new('RGB', (height, width), 'white')

    def drawCorner(self, cornerList):

        for park in cornerList:
            imageDraw = ImageDraw.Draw(self.im)

            if park[-1] == 1:
                color = 'red'
            else:
                color = 'green'

            ft = ImageFont.truetype("static/arial.ttf", size=14, index=0)
            imageDraw.polygon(park[1:9], outline=color)
            imageDraw.text((park[1] + (abs(park[5] - park[1]) / 2), park[2] + (abs(park[4] - park[2]) / 2)), str(park[0]), font=ft, fill=color, )

    def centralDraw(self, positionList):
        # centreX, centreY, width, length, rotation
        p1 = [positionList[0] - positionList[2], positionList[1] - positionList[3]]
        p2 = [positionList[0] + positionList[2], positionList[1] - positionList[3]]
        p3 = [positionList[0] + positionList[2], positionList[1] + positionList[3]]
        p4 = [positionList[0] - positionList[2], positionList[1] + positionList[3]]

        return [p1, p2, p3, p4]

    def save(self, filename):
        plt.figure(filename)
        plt.imshow(self.im)
        plt.axis('off')
        plt.savefig(filename, dpi=150)
        plt.show()
