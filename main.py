import sys
import cv2
import math
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow



from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1125, 595)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(0, 0, 200, 200))
        self.labelCamera.setObjectName("labelCamera")
        self.labelCapture = QtWidgets.QLabel(self.centralwidget)
        self.labelCapture.setGeometry(QtCore.QRect(200, 0, 400, 400))
        self.labelCapture.setObjectName("labelCapture")
        self.btnOpenCamera = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenCamera.setGeometry(QtCore.QRect(80, 490, 75, 23))
        self.btnOpenCamera.setObjectName("btnOpenCamera")
        self.btnCapture = QtWidgets.QPushButton(self.centralwidget)
        self.btnCapture.setGeometry(QtCore.QRect(200, 490, 75, 23))
        self.btnCapture.setObjectName("btnCapture")
        self.btnReadImage= QtWidgets.QPushButton(self.centralwidget)
        self.btnReadImage.setGeometry(QtCore.QRect(330, 490, 75, 23))
        self.btnReadImage.setObjectName("btnReadImage\n""")
        self.btnGray = QtWidgets.QPushButton(self.centralwidget)
        self.btnGray.setGeometry(QtCore.QRect(460, 490, 75, 23))
        self.btnGray.setObjectName("btnGray")
        self.btnThreshold = QtWidgets.QPushButton(self.centralwidget)
        self.btnThreshold.setGeometry(QtCore.QRect(570, 490, 75, 23))
        self.btnThreshold.setObjectName("btnThreshold")
        self.labelResult = QtWidgets.QLabel(self.centralwidget)
        self.labelResult.setGeometry(QtCore.QRect(600, 0, 400, 400))
        self.labelResult.setObjectName("labelResult")
        self.btnCalculate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalculate.setGeometry(QtCore.QRect(680, 490, 75, 23))
        self.btnCalculate.setObjectName("btnCalculate")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 420, 131, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.btnRectangle = QtWidgets.QPushButton(self.centralwidget)
        self.btnRectangle.setGeometry(QtCore.QRect(870, 490, 75, 23))
        self.btnRectangle.setObjectName("btnRectangle")
        self.btnDenoise = QtWidgets.QPushButton(self.centralwidget)
        self.btnDenoise.setGeometry(QtCore.QRect(770, 490, 75, 23))
        self.btnDenoise.setObjectName("btnDenoise")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 380, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btnOpenCamera.clicked.connect(MainWindow.btnOpenCamera_Clicked)
        self.btnCapture.clicked.connect(MainWindow.btnCapture_Clicked)
        self.btnReadImage.clicked.connect(MainWindow.btnReadImage_Clicked)
        self.btnGray.clicked.connect(MainWindow.btnGray_Clicked)
        self.btnThreshold.clicked.connect(MainWindow.btnThreshold_Clicked)
        self.btnCalculate.clicked.connect(MainWindow.btnCalculate_Clicked)
        self.btnDenoise.clicked.connect(MainWindow.btnDenoise_Clicked)
        self.btnRectangle.clicked.connect(MainWindow.btnRectangle_Clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelCamera.setText(_translate("MainWindow", "摄像头"))
        self.labelCapture.setText(_translate("MainWindow", "捕获图"))
        self.btnOpenCamera.setText(_translate("MainWindow", "摄像头"))
        self.btnCapture.setText(_translate("MainWindow", "捕获图片"))
        self.btnReadImage.setText(_translate("MainWindow", "打开图片"))
        self.btnGray.setText(_translate("MainWindow", "灰度化"))
        self.btnThreshold.setText(_translate("MainWindow", "阈值分割"))
        self.labelResult.setText(_translate("MainWindow", "结果图"))
        self.btnCalculate.setText(_translate("MainWindow", "绿叶形心"))
        self.btnRectangle.setText(_translate("MainWindow", "计算面积"))
        self.btnDenoise.setText(_translate("MainWindow", "方块角度"))


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camera = cv2.VideoCapture(1)
        self.is_camera_opened = False  # 摄像头有没有打开标记

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.btnOpenCamera.setText("关闭摄像头")
            self._timer.start()
        else:
            self.btnOpenCamera.setText("打开摄像头")
            self._timer.stop()

    def btnCapture_Clicked(self):
        '''
        捕获图片
        '''
        # 摄像头未打开，不执行任何操作
        if not self.is_camera_opened:
            return

        self.captured = self.frame
        # 后面这几行代码几乎都一样，可以尝试封装成一个函数
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnReadImage_Clicked(self):
        '''
        从本地读取图片 文件路径不能有中文
        '''
        # 打开文件选取对话框
        filename, _ = QFileDialog.getOpenFileName(self, '打开图片')
        if filename:
            self.captured = cv2.imread(str(filename))
            self.frame = cv2.imread(str(filename))
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
            self.captured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)

            rows, cols, channels = self.captured.shape
            bytesPerLine = channels * cols
            QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
            self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnGray_Clicked(self):
        '''
        灰度化
        '''
        # 如果没有捕获图片，则不执行操作
        if not hasattr(self, "captured"):
            return
        self.cpatured = cv2.cvtColor(self.captured, cv2.COLOR_RGB2GRAY)
        rows, columns = self.cpatured.shape
        bytesPerLine = columns
        # 灰度图是单通道，所以需要用Format_Indexed8
        QImg = QImage(self.cpatured.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnThreshold_Clicked(self):
        '''
        Otsu自动阈值分割
        '''
        #self.textBrowser.setText("dadad")
        if not hasattr(self, "captured"):
            return

        _, self.cpatured = cv2.threshold(
            self.cpatured, 0, 250,  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        rows, columns = self.cpatured.shape
        bytesPerLine = columns
        # 阈值分割图也是单通道，也需要用Format_Indexed8
        QImg = QImage(self.cpatured.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        #self.wxy.setText("%d", 11)

    def btnRectangle_Clicked(self):
        img = self.frame
        m=0
        n=0
        for i in range(1, img.shape[0]):

            for j in range(1, img.shape[1]):
                # b = 2*img.item(i, j, 1) - img.item(i, j, 0) - img.item(i, j, 2)
                a = 5

                if (img.item(i, j, 0) > 40) and (img.item(i, j,0) < 70 ) and (img.item(i, j, 1) > 40) and (img.item(i, j,1) < 70 ) and (img.item(i, j, 2) > 40) and (img.item(i, j,2) < 70 ) :
                    for k in range(0, 3):
                        img.itemset((i, j, k), 0)
                        n = n + 1
                if (img.item(i, j, 1) - img.item(i, j, 0) > a) and (img.item(i, j, 1) - img.item(i, j, 2) > a):
                    for k in range(0, 3):
                        img.itemset((i, j, k), 0)
                        m = m + 1
                else:
                    for k in range(0, 3):
                        img.itemset((i, j, k), 255)
        s = m/n*25
        self.lineEdit.setText("%d" % s )
        img = cv2.blur(img, (3, 3))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img, 5)
        img = cv2.blur(img, (3, 3))
        ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        img = cv2.bilateralFilter(img, 5, 75, 75)
        img = cv2.medianBlur(img, 5)
        img = cv2.Canny(img, 100, 200)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self.frame = img

        img_rows, img_cols, channels = img.shape
        bytesPerLine = channels * img_cols
        QImg = QImage(img.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    #计算形心，及角度
    def btnDenoise_Clicked(self):
        img = self.frame

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



        a = 0
        b = 0
        for i in range(1, len(contours)):
            cnt = contours[i]
            M = cv2.moments(cnt)
            c = int(M['m00'])
            if c > a:
                a = c
                b = i
        cv2.drawContours(img, contours, b, (0, 0, 255), 3)
        cnt = contours[b]
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(img, (cx, cy), 2, (0, 255, 0), -1)
        (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)

        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
        cv2.circle(img, (leftmost[0], leftmost[1]), 6, (255, 25, 0), -1)
        cv2.circle(img, (rightmost[0], rightmost[1]), 6, (255, 25, 0), -1)
        cv2.circle(img, (topmost[0], topmost[1]), 6, (255, 25, 0), -1)
        cv2.circle(img, (bottommost[0], bottommost[1]), 6, (255, 25, 0), -1)

        y1 = int((leftmost[1] + topmost[1])/2)
        y2 = int((rightmost[1] + bottommost[1]) / 2)
        x1 = int((leftmost[0] + topmost[0]) / 2)
        x2 = int((rightmost[0] + bottommost[0]) / 2)
        #self.lineEdit.setText("%s" % type(leftmost[1]))



        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 5)


        #
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

        dy = y1-y2

        dx = x1-x2

        temp = math.sqrt(dx * dx + dy * dy)

        angle_cos = dx / temp
        angle = math.acos(angle_cos) * 180 / 3.14

        if dy < 0:
            angle = -angle
        self.lineEdit.setText("%s" % angle)

        img_rows, img_cols, channels = img.shape
        bytesPerLine = channels * img_cols
        QImg = QImage(img.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        '''
        a = 1
        img = self.frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #a = self.lineEdit.text()
        #self.textBrowser.setText(a)
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])
        img = cv2.inRange(img, lower_blue, upper_blue)


        #self.textBrowser.setText("%d,%d,a" % a/1000 % a)
        #a = self.textBrowser.text()

        # 提取颜色
        #img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # ret,thresh = cv.threshold(gray,255,255,60)
        # ret,thresh1 = cv.threshold(gray,127,255,cv.THRESH_BINARY)

        img_rows, img_cols, channels = img.shape
        bytesPerLine = channels * img_cols
        QImg = QImage(img.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #den = cv2.fastNlMeansDenoisingColor(img, None, 10, 10, 7, 21)
        #img_rows, img_cols, channels = denoise.shape
        #bytesPerLine = channels * img_cols
        #QImg = QImage(denoise.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        #self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
        #    self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        '''

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片
        '''
        ret, self.frame = self.camera.read()
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnCalculate_Clicked(self):


        img = self.frame

        m = 0
        for i in range(1, img.shape[0]):

            for j in range(1, img.shape[1]):
                # b = 2*img.item(i, j, 1) - img.item(i, j, 0) - img.item(i, j, 2)
                a = 5
                #绿色bgr
                if (img.item(i, j, 1) - img.item(i, j, 0) > a) and (img.item(i, j, 1) - img.item(i, j, 2) > a):

                    for k in range(0, 3):
                        img.itemset((i, j, k), 0)
                        m = m + 1
                else:
                    for k in range(0, 3):
                        img.itemset((i, j, k), 255)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #a = max(contours)

        area = []
        a = 0
        b = 0
        for i in range(1,len(contours)):
            cnt = contours[i]
            M = cv2.moments(cnt)
            c = int(M['m00'])
            if c > a:
                a = c
                b = i
        cv2.drawContours(img, contours, b, (0, 0, 255), 3)
        cnt = contours[b]
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(img,(cx,cy), 2, (0,255,0), -1)
        (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)
        self.lineEdit.setText("%s" % angle)



        img_rows, img_cols, channels = img.shape
        bytesPerLine = channels * img_cols
        QImg = QImage(img.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
