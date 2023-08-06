import os
import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet

from .constant import OUTPUT_FOLDER


def compute_distance(line, hbinning: int, vbinning: int, hdecimation: int, vdecimation: int):
    [[x1, y1], [x2, y2]] = line

    if hbinning == 1 and vbinning == 1 and vdecimation == 1 and hdecimation == 1:
        width = px_distance(x1, x2, y1, y2)
    elif hbinning != 1 or vbinning != 1:
        width = px_distance(x1, x1 + (np.abs(x2 - x1) / hbinning), y1, y1 + (np.abs(y2 - y1) / vbinning))
    elif hdecimation != 1 or vdecimation != 1:
        width = px_distance(x1, x1 + (np.abs(x2 - x1) / hdecimation), y1, y1 + (np.abs(y2 - y1) / vdecimation))
    return width


def px_distance(x1, x2, y1, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def confirm_save(filename):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("Your napari_calibration is saved as :\n" + filename)
    msg.setWindowTitle("Success")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()


class CalibrationForm(QWidget):
    # constructor
    def __init__(self, viewer=None):
        super().__init__()

        # apply_stylesheet(self, theme='dark_teal.xml')
        # Qt form
        grid_layout = QGridLayout()
        self.create_formgroupbox()

        self.filename_box = QLineEdit()
        label = QLabel("Output file")
        self.save_btn = QPushButton("Save")
        self.save_btn.setEnabled(False)
        self.points_box = QLineEdit()

        grid_layout.setAlignment(Qt.AlignTop)
        grid_layout.setVerticalSpacing(30)
        grid_layout.addWidget(label, 0, 0, 1, 1)
        grid_layout.addWidget(self.filename_box, 0, 1, 1, 1)

        grid_layout.setVerticalSpacing(30)

        grid_layout.addWidget(QLabel("Real distance (mm)"), 1, 0, 2, 1)
        grid_layout.addWidget(self.points_box, 1, 1, 2, 1)

        grid_layout.setVerticalSpacing(30)

        grid_layout.addWidget(self.formGroupBox, 3, 0, 1, 5)

        grid_layout.addWidget(self.save_btn, 8, 0, 3, 3)

        self.setLayout(grid_layout)

        self.viewer = viewer
        # self.lines = lines
        self.display()

        self.connect_actions()
        self.cb_desactivation()

    def display(self):
        self.setWindowTitle("Form")

    def connect_actions(self):
        """
        Events
        """
        if self.viewer is not None:
            self.viewer.layers['lines'].events.set_data.connect(self.possible_save)
            self.viewer.layers['lines'].events.data.connect(self.enable_add_line)

        self.filename_box.textChanged.connect(self.possible_save)
        self.points_box.textChanged.connect(self.possible_save)
        self.save_btn.clicked.connect(self.file_already_exists)

        self.hbinning.currentTextChanged.connect(self.cb_desactivation)
        self.vbinning.currentTextChanged.connect(self.cb_desactivation)
        self.hdecimation.currentTextChanged.connect(self.cb_desactivation)
        self.vdecimation.currentTextChanged.connect(self.cb_desactivation)

    def enable_add_line(self, e=None):
        layout_layer = self.viewer.window.qt_viewer.controls.widgets[self.viewer.layers["lines"]].grid_layout
        button_grid = layout_layer.itemAt(0)
        add_line_button = button_grid.itemAt(7).widget()

        print(len(self.viewer.layers['lines'].data))

        if len(self.viewer.layers['lines'].data) < 1:
            add_line_button.setEnabled(True)

        else:
            add_line_button.setEnabled(False)

    def possible_save(self, e=None):

        if self.filename_box.text() != "" and len(
                self.viewer.layers['lines'].data) != 0 and self.points_box.text() != "":
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)

    def file_already_exists(self):
        calibration_folder = OUTPUT_FOLDER
        if not os.path.exists(calibration_folder):
            os.makedirs(calibration_folder)

        filename = self.filename_box.text() + ".txt"
        if filename in os.listdir(calibration_folder):
            self.confirm_replace(filename)

        else:
            self.write_file()

    def write_file(self):
        line = self.viewer.layers['lines'].data[-1]

        nb_px = compute_distance(line,
                                 hbinning=int(self.hbinning.currentText()),
                                 vbinning=int(self.vbinning.currentText()),
                                 hdecimation=int(self.hdecimation.currentText()),
                                 vdecimation=int(self.vdecimation.currentText()))

        calibration_folder = OUTPUT_FOLDER

        filename = os.path.join(calibration_folder, self.filename_box.text() + ".txt")
        try:
            with open(filename, 'w') as f:
                f.write("Millimeters : " + self.points_box.text() + "\n")
                f.write("Pixels : " + str(nb_px))
            confirm_save(filename)
        except:
            print("error in save")

    def confirm_replace(self, filename):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("A file with the name : " + filename + " already exists. Do you want to replace this file ?")
        msg.setWindowTitle("Confirmation - replace")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        retval = msg.exec_()

        if retval == QMessageBox.Yes:
            self.write_file()

    def create_formgroupbox(self):
        self.formGroupBox = QGroupBox("Camera options")
        layout = QFormLayout()

        self.hbinning = QComboBox()
        self.hbinning.addItems(["1", "2"])
        self.vbinning = QComboBox()
        self.vbinning.addItems(["1", "2"])
        self.hdecimation = QComboBox()
        self.hdecimation.addItems(["1", "2", "4", "8"])
        self.vdecimation = QComboBox()
        self.vdecimation.addItems(["1", "2", "4", "8"])

        layout.addRow(QLabel("Horizontal Binning :"), self.hbinning)
        layout.addRow(QLabel("Vertical Binning :"), self.vbinning)
        layout.addRow(QLabel("Horizontal Decimation:"), self.hdecimation)
        layout.addRow(QLabel("Vertical Decimation:"), self.vdecimation)
        self.formGroupBox.setLayout(layout)

    def cb_desactivation(self):
        if int(self.hbinning.currentText()) != 1:
            self.hdecimation.setEnabled(False)
            self.vdecimation.setEnabled(False)

        elif int(self.vbinning.currentText()) != 1:
            self.hdecimation.setEnabled(False)
            self.vdecimation.setEnabled(False)

        else:
            self.hdecimation.setEnabled(True)
            self.vdecimation.setEnabled(True)

        if int(self.hdecimation.currentText()) != 1:
            self.hbinning.setEnabled(False)
            self.vbinning.setEnabled(False)

        elif int(self.vdecimation.currentText()) != 1:
            self.hbinning.setEnabled(False)
            self.vbinning.setEnabled(False)

        else:
            self.hbinning.setEnabled(True)
            self.vbinning.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')

    window = CalibrationForm()
    window.show()
    window.setWindowTitle('src form')

    sys.exit(app.exec_())
