from PIL import Image, ImageOps, ImageDraw
import numpy as np

def calculate_avgColor(img):
    img_matrix = np.array(img)
    avgColor = np.mean(img_matrix, axis=(0,1)).astype('uint8')
    return avgColor

def weighted_average(hist):
    total = sum(hist)
    error = value = 0

    if total > 0:
        value = sum(i * x for i, x in enumerate(hist)) / total
        error = sum(x * (value - i) ** 2 for i, x in enumerate(hist)) / total
        error = error ** 0.5

    return error

def get_detail(hist):
    red_detail = weighted_average(hist[:256])
    green_detail = weighted_average(hist[256:512])
    blue_detail = weighted_average(hist[512:768])

    detail_intensity = red_detail * 0.2989 + green_detail * 0.5870 + blue_detail * 0.1140

    return detail_intensity

class Region:
    def __init__(self, img, coords):
        self.img = img.crop(coords)
        self.img_matrix = np.array(img)
        self.img_width, self.img_height = self.img.size
        self.coords = coords

        hist = self.img.histogram()
        self.detail = get_detail(hist)
        self.avg_color = calculate_avgColor(self.img)

        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def branch(self):
        left, top, width, height = self.coords
        middle_x = int(left + (width - left) / 2)
        middle_y = int(top + (height - top) / 2)

        if(self.detail > DETAIL and width - left >= 5 and height - top >= 5):
            self.nw = Region(img, (left, top, middle_x, middle_y))
            self.ne = Region(img, (middle_x, top, width, middle_y))
            self.sw = Region(img, (left, middle_y, middle_x, height))
            self.se = Region(img, (middle_x, middle_y, width, height))

            self.nw.branch()
            self.ne.branch()
            self.sw.branch()
            self.se.branch()

    def create_image(self):
        image = Image.new('RGB', (self.img_width, self.img_height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.img_width, self.img_height), (0, 0, 0))

        self.get_leaf_nodes(self)

        for quadrant in leaves:
                draw.rectangle(quadrant.coords, (quadrant.avg_color[0], quadrant.avg_color[1], quadrant.avg_color[2]))

        return image
    
    def get_leaf_nodes(self, root):
        start = root
        if(start == None):
            return
        elif(start.nw  == None and start.ne  == None and start.sw  == None and start.se == None):
            leaves.append(start)
            return
        else:
            if(start.nw != None):
                start.nw.get_leaf_nodes(start.nw)            
            if(start.ne != None):
                start.ne.get_leaf_nodes(start.ne)        
            if(start.sw != None):
                start.sw.get_leaf_nodes(start.sw)        
            if(start.se != None):
                start.se.get_leaf_nodes(start.se)            

img = Image.open('./image.jpg')
img = ImageOps.exif_transpose(img)          
img = img.resize((600, 600))
img.show()
DETAIL = 5

root = Region(img, img.getbbox())
root.branch()
leaves = []

compressed_image = root.create_image()
compressed_image.show()



