import sys

import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton, QLabel, QGridLayout
from qt_material import apply_stylesheet

from .Video.widget import LiveIDS


class ImageForm(QWidget):
    def __init__(self, viewer=None, parent=None):
        super(QWidget, self).__init__(parent)
        self.viewer = viewer

        apply_stylesheet(self, theme='dark_teal.xml')

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tab1 = PhotoForm(viewer=self.viewer)
        self.tab2 = LiveIDS(napari_viewer=self.viewer)
        # self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Photo")
        self.tabs.addTab(self.tab2, "Video")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.connect_actions()

    def connect_actions(self):
        self.tabs.currentChanged.connect(self.on_change_mode)

    def on_change_mode(self, index):
        # Go to photo mode

        if index == 0:
            if self.tab2.live:
                self.tab2.stop_acquisition()
                self.tab2.rec_button.setEnabled(True)

                if "Video" in self.viewer.layers:
                    self.viewer.layers["Video"].visible = False

                if "image" in self.viewer.layers:
                    self.viewer.layers["image"].visible = True

        if index == 1:
            if "Video" in self.viewer.layers:
                self.viewer.layers["Video"].visible = True

            if "image" in self.viewer.layers:
                self.viewer.layers["image"].visible = False



class PhotoForm(QWidget):
    def __init__(self, viewer=None, parent=None):
        super(QWidget, self).__init__(parent)
        self.viewer = viewer

        apply_stylesheet(self, theme='dark_teal.xml')

        # Create first tab
        self.layout = QGridLayout(self)
        # self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.choose_label = QLabel("Choose a picture")
        self.browse_btn = QPushButton("Browse")
        self.confirm_label = QLabel("")
        self.layout.addWidget(self.choose_label, 0, 0, 1, 1)
        self.layout.addWidget(self.browse_btn, 0, 1, 1, 1)
        self.layout.addWidget(self.confirm_label, 1, 0, -1, 1)

        self.setLayout(self.layout)

        self.connect_actions()

    def connect_actions(self):
        self.browse_btn.clicked.connect(self.getfiles)

    def getfiles(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.png')
        if filename != "":
            self.confirm_label.setText("Opened : " + filename.split("/")[-1])

            img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
            if "image" not in self.viewer.layers:
                self.viewer.add_image(img, name="image")
            else:
                self.viewer.layers["image"].data = img

            # Put lines in 1st plan
            self.viewer.layers.move(self.viewer.layers.index("lines"), -1)

            self.viewer.layers.selection.active = self.viewer.layers["lines"]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')

    window = ImageForm()
    window.show()
    window.setWindowTitle('src form')

    sys.exit(app.exec_())
