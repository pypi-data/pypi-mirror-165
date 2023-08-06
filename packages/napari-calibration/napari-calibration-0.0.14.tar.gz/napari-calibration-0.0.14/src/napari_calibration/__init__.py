__version__ = "0.0.1"

from napari.utils.notifications import show_info

from .Image_widget import ImageForm
from .calibration_widget import CalibrationForm


def show_hello_message():
    show_info('Hello, world!')
