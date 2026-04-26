#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QHBoxLayout, QMessageBox, QRadioButton, QPushButton, QGroupBox, QButtonGroup,QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN
import os
#правка номер 1
app = QApplication([])
mw = QWidget()
mw.setWindowTitle('Easy Editor')
mw.resize(640, 480)
line1 = QHBoxLayout()
line2 = QHBoxLayout()
line3 = QVBoxLayout()
line4 = QVBoxLayout()

list_images = QListWidget()
btn_dir = QPushButton('Папка')
lb_image = QLabel('Картинка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_intensity = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_reset_filters = QPushButton('Сбросить фильтры')

line3.addWidget(lb_image)

line1.addLayout(line3)
line1.addLayout(line4)
line3.addLayout(line2)
mw.setLayout(line1)

line2.addWidget(btn_left)
line2.addWidget(btn_right)
line2.addWidget(btn_mirror)
line2.addWidget(btn_intensity)
line2.addWidget(btn_bw)
line2.addWidget(btn_save)
line2.addWidget(btn_reset_filters)



line4.addWidget(btn_dir)
line4.addWidget(list_images)


mw.show()


workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extentions):
    result = []
    for filename in files:
        for ext in extentions:
            if filename.endswith(ext):
                result.append(filename)

    return result

def showFilenameList():
    extentions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    if workdir != '':
        filenames = filter(os.listdir(workdir), extentions)
        list_images.clear()
        for filename in filenames:
            list_images.addItem(filename)

btn_dir.clicked.connect(showFilenameList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
        self.original_image = None
    def loadimage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def resetImage(self):
        if self.original_image is None:
            return 
        self.image = self.original_image.copy()
        self.showImage(os.path.join(workdir, self.filename))
        

workimage = ImageProcessor()

def showchosenImage():
    if list_images.currentRow() >= 0:
        filename = list_images.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

list_images.currentRowChanged.connect(showchosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_intensity.clicked.connect(workimage.do_sharpen)
btn_mirror.clicked.connect(workimage.do_flip)
btn_save.clicked.connect(workimage.saveImage)
btn_reset_filters.clicked.connect(workimage.resetImage)

app.exec_()
