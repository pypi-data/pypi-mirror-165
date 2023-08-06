import os
import pathlib
import time

import cv2
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QPushButton, QLabel, QGridLayout
from ids_peak import ids_peak
from ids_peak_ipl import ids_peak_ipl
from napari._qt.qthreading import thread_worker
from qt_material import apply_stylesheet

import os
import pathlib

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QComboBox, QSpinBox


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


class LiveIDS(QWidget):

    def __init__(self, napari_viewer):
        super(LiveIDS, self).__init__()

        # Attributes to compute fps
        self.start = time.time()
        self.end = 0

        self.exp_time_value = 50
        self.initui()
        self.viewer = napari_viewer

        # initialize ids_peak library
        ids_peak.Library.Initialize()

        self.init = True
        self.device = None
        self.nodemap_remote_device = None
        self.datastream = None
        self.acquisition_timer = QTimer()
        self.frame = 0
        self.live = False
        self.worker = None
        self.picture = []

        self.display()
        self.connect_actions()

    def display(self):
        """
        Define style for the Qdock_widget camera
        """
        self.setFixedSize(250, 340)

    def connect_actions(self):
        """
        Events
        """
        self.connect_cam_button.clicked.connect(self._on_connect_clicked)
        self.select_cam_combobox.currentIndexChanged.connect(self._on_select_cam)
        self.rec_button.clicked.connect(self._on_click_live)
        # self.photo_button.clicked.connect(self._on_photo)
        self.exp_time_box.valueChanged.connect(self._on_exp_changed)

    def _on_exp_changed(self):
        """
        Change the exposure time
        """
        self.exp_time_value = self.exp_time_box.value()
        self.nodemap_remote_device.FindNode("ExposureTime").SetValue(self.exp_time_value * 1000)

    def stop_acquisition(self):
        """
        Stop acquisition timer and stop acquisition on camera
        """
        self.worker.quit()
        self.live = False
        # Try to stop acquisition
        try:
            # Stop acquisition timer and camera acquisition
            self.acquisition_timer.stop()
            remote_nodemap = self.device.RemoteDevice().NodeMaps()[0]
            remote_nodemap.FindNode("AcquisitionStop").Execute()

            # Stop and flush datastream
            self.datastream.KillWait()
            self.datastream.StopAcquisition(ids_peak.AcquisitionStopMode_Default)
            self.datastream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)
            self.datastream = None

            # Unlock parameters after acquisition stop
            if self.nodemap_remote_device is not None:
                try:
                    self.nodemap_remote_device.FindNode("TLParamsLocked").SetValue(0)
                except Exception as e:
                    QMessageBox.information(self, "Exception", str(e), QMessageBox.Ok)

        except Exception as e:
            QMessageBox.information(self, "Exception", str(e), QMessageBox.Ok)

    def confirmation_message_box(self, filename):
        """
        Confirmation box to run the model or not
        """
        msg = QMessageBox()

        # Remember the program chosen by the user
        msg.setText("The capture was successfully recorded as \n" + filename)
        msg.setWindowTitle("Confirmation - Capture")
        msg.setStandardButtons(QMessageBox.Ok)

        val = msg.exec_()
        if val == QMessageBox.Ok:
            self.start_acquisition()

    def trigger_buttons(self, photo_boolean):
        """
        Enable one button and disalbe other
        :param photo_boolean: Type of program use, if it is not "Photo", it is "Video"
        """
        self.rec_button.setEnabled(photo_boolean)

        # Cursor decoration
        if photo_boolean:
            self.rec_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def _on_click_live(self):
        """
        When the user clicks on the button "Live - view", the behaviour of the program change if the
        formulary is opened
        """

        self.setStyleSheet(
            open(os.path.join(pathlib.Path(__file__).parent.resolve(),
                              "styles/widget_live.css")).read())

        self.start_acquisition()

    def start_acquisition(self):
        """
        set up some parameters of the camera to take video further
        """
        self.trigger_buttons(False)
        self.remove_layer("Image")

        if self.datastream is None:
            self.open_device()

        # Configure exposure time
        self.nodemap_remote_device.FindNode("ExposureTime").SetValue(self.exp_time_value * 1000)
        max_fps = self.nodemap_remote_device.FindNode("AcquisitionFrameRate").Maximum()
        # fix max fps
        target_fps = min(max_fps, 30)
        self.nodemap_remote_device.FindNode("AcquisitionFrameRate").SetValue(target_fps)

        # Setup the clock of the thread which displays the video
        self.aquisition_period = 1 / target_fps

        try:
            # Lock critical features to prevent them from changing during acquisition
            self.nodemap_remote_device.FindNode("TLParamsLocked").SetValue(1)

            # Start acquisition on camera
            self.datastream.StartAcquisition()
            self.nodemap_remote_device.FindNode("AcquisitionStart").Execute()
            self.nodemap_remote_device.FindNode("AcquisitionStart").WaitUntilDone()

            print("max fps ", max_fps)

        except Exception as e:
            print("Exception: " + str(e))
            return False

        self.live = True

        if self.worker is None:
            self.worker = self.on_acquisition_timer()
            self.worker.yielded.connect(self.update_display)
            self.worker.start()

        return True

    @staticmethod
    def get_image(buffer):
        """
        Get picture from the buffer and convert it to numpy picture
        :param buffer: current buffer data
        :return: numpy RGB 3 channels picture
        """
        # Create IDS peak IPL image from buffer
        ipl_image = ids_peak_ipl.Image_CreateFromSizeAndBuffer(
            buffer.PixelFormat(),
            buffer.BasePtr(),
            buffer.Size(),
            buffer.Width(),
            buffer.Height()
        )
        # Convert picture in RGB and transform this picture in array with 3 channels
        converted_ipl_image = ipl_image.ConvertTo(ids_peak_ipl.PixelFormatName_RGB8)
        return converted_ipl_image.get_numpy_3D()

    def remove_layer(self, layer_name):
        """
        Remove layer if it exists
        :param layer_name: Name of the layer
        """
        if layer_name in self.viewer.layers:
            self.viewer.layers.remove(layer_name)

    @thread_worker
    def on_acquisition_timer(self):
        """
        Get image from the buffer and transmit it
        :return: yield RGB picture
        """
        while self.viewer.window.qt_viewer:
            buffer = self.datastream.WaitForFinishedBuffer(5000)

            image_rgb = self.get_image(buffer)

            self.datastream.QueueBuffer(buffer)

            yield image_rgb

            # Take time between two sends of pictures
            time.sleep(self.aquisition_period)

    def update_display(self, image):
        """
        Update the display replacing the old with the new picture in the "Video" layer
        :param image: RGB picture
        """

        # Add new layer if "Video" layer does not exist else overwrite on it
        if self.frame == 0:
            self.viewer.add_image(image, name="Video", blending='additive', rgb=True)
        else:
            self.viewer.layers["Video"].data = image
        self.frame += 1

        self.viewer.layers.selection.active = self.viewer.layers["lines"]

    @staticmethod
    def remove_controls(grid):
        """
        Remove the gridLayout of the control layer
        :param grid: specify which grid we have to remove
        """
        for i in range(grid.count()):
            widget = grid.itemAt(i).widget()
            if not isinstance(widget, type(None)):
                widget.close()

    def _on_select_cam(self, index):
        """
        Connect the camera selected in the drop-down menu
        :param index: index of the item selected in the drop-down menu
        """
        # create a device manager object
        device_manager = ids_peak.DeviceManager.Instance()

        # update the device manager
        device_manager.Update()

        selected_device = index
        self.device = device_manager.Devices()[selected_device].OpenDevice(
            ids_peak.DeviceAccessType_Control
        )
        # get the remote device node map
        self.nodemap_remote_device = self.device.RemoteDevice().NodeMaps()[0]

        self.camera_label.setText("Connected to : " + self.device.ModelName())
        # Set visible some widgets
        self.visible_widgets(3)

        self.open_device()

    def visible_widgets(self, start_index):
        """
        Set visible some widget which were invisible
        :param start_index: index of item in grid from which we make visible the widgets
        """
        for i in range(start_index, self.layout.count()):
            self.layout.itemAt(i).widget().setVisible(True)

    def open_device(self):
        """
        Open the device
        """
        # Open standard data stream
        datastreams = self.device.DataStreams()
        if datastreams.empty():
            QMessageBox.critical(self, "Error", "Device has no DataStream!", QMessageBox.Ok)
            self.device = None

        self.datastream = datastreams[0].OpenDataStream()

        if self.device is not None:
            # Get nodemap of the remote device for all accesses to the genicam
            # nodemap tree
            self.nodemap_remote_device = self.device.RemoteDevice().NodeMaps()[0]
        else:
            QMessageBox.critical(self, "Error", "Device has no DataStream!", QMessageBox.Ok)

        # To prepare for untriggered continuous image acquisition, load the default user set if available and
        # wait until execution is finished
        try:
            self.nodemap_remote_device.FindNode("UserSetSelector").SetCurrentEntry("Default")
            self.nodemap_remote_device.FindNode("UserSetLoad").Execute()
            self.nodemap_remote_device.FindNode("UserSetLoad").WaitUntilDone()
        except ids_peak.Exception:
            # Userset is not available
            print("No userset")
            pass

        # Get the payload size for correct buffer allocation
        payload_size = self.nodemap_remote_device.FindNode("PayloadSize").Value()

        # Get minimum number of buffers that must be announced
        buffer_count_max = self.datastream.NumBuffersAnnouncedMinRequired()

        # Allocate and announce image buffers and queue them
        for i in range(buffer_count_max):
            buffer = self.datastream.AllocAndAnnounceBuffer(payload_size)
            self.datastream.QueueBuffer(buffer)

    def show_error_box(self):
        """
        Show QMessageBox when there are not IDS camera plugged
        """
        msg = QMessageBox()
        # msg.setWindowIcon(self.icon)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("There is not any IDS camera plugged")
        msg.setInformativeText("Please plug a camera and retry")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def list_ids_cameras(self):
        """
        List all the IDS devices in a drop-down menu
        """
        # create a device manager object
        device_manager = ids_peak.DeviceManager.Instance()

        # update the device manager
        device_manager.Update()

        # exit program if no device was found
        if device_manager.Devices().empty():
            self.show_error_box()
        else:
            self.select_cam_combobox.setVisible(True)

        # list all available devices
        for device in device_manager.Devices():
            self.select_cam_combobox.addItem(device.ModelName())

    def _on_connect_clicked(self):
        """
        Signal when user clicks on "Connect camera"
        """
        self.connect_cam_button.setEnabled(False)
        self.list_ids_cameras()


    def initui(self):
        self.layout = QGridLayout()

        self.logo = QLabel()
        pixmap = QPixmap(os.path.join(pathlib.Path(__file__).parent.resolve(), r"../Logo/logo_ids.jpg"))
        pixmap = pixmap.scaled(QSize(220, 220), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignHCenter)
        self.logo.setStyleSheet("QLabel{margin-bottom:20px;}")

        self.connect_cam_button = QPushButton("Connect camera")

        self.select_cam_combobox = QComboBox()
        self.select_cam_combobox.setVisible(False)

        self.camera_label = QLabel()

        self.rec_button = QPushButton("Live - view")
        self.rec_button.setObjectName("recButton")
        self.rec_button.setVisible(False)

        self.exp_time_label = QLabel("Exposure time (ms)")
        self.exp_time_label.setVisible(False)
        self.exp_time_box = QSpinBox()
        self.exp_time_box.setMinimum(1)
        self.exp_time_box.setMaximum(300)
        self.exp_time_box.setValue(self.exp_time_value)
        self.exp_time_box.setVisible(False)

        self.counter_fps_label = QLabel("FPS : ")
        self.counter_fps_label.setVisible(False)

        self.layout.addWidget(self.logo, 0, 0, 1, 2)
        self.layout.addWidget(self.connect_cam_button, 1, 0, 1, 2, Qt.AlignTop)
        self.layout.addWidget(self.select_cam_combobox, 2, 0, 1, 2, Qt.AlignTop)
        self.layout.addWidget(self.camera_label, 3, 0, 1, 2, Qt.AlignTop)
        self.layout.addWidget(self.exp_time_label, 4, 0, 1, 1, Qt.AlignTop)
        self.layout.addWidget(self.exp_time_box, 4, 1, 1, 1, Qt.AlignTop)
        self.layout.addWidget(self.rec_button, 7, 0, 1, -1, Qt.AlignBottom)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
