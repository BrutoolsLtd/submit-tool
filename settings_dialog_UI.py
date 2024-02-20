################################################################################
# TME FX Trishul Media Entertainment [Jun 2021]
################################################################################ 
""" Window user interface to set database location, project root folder and 
mayapy.exe

@author Esteban Ortega <brutools@gmail.com>
"""
import sys

from PySide2 import QtWidgets
from PySide2 import QtCore


class SettingsDialogUI(QtWidgets.QDialog):
    """ Settings dialog window to set location of db, project root folder 
    and mayapy.exe.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Set locations')
        self.setMinimumSize(300, 180)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        settings_widget_layout = QtWidgets.QVBoxLayout()
        self.setLayout(settings_widget_layout)

        self.server_location_label = QtWidgets.QLabel('Server root folder:')
        self.server_root_folder_button = QtWidgets.QPushButton('Server project root folder')
        self.local_location_label = QtWidgets.QLabel('Local root folder:')
        self.local_root_folder_button = QtWidgets.QPushButton('Local project root folder')

        settings_widget_layout.addWidget(self.server_location_label)
        settings_widget_layout.addWidget(self.server_root_folder_button)
        settings_widget_layout.addWidget(self.local_location_label)
        settings_widget_layout.addWidget(self.local_root_folder_button)

        self.settings_widget_buttonBox = QtWidgets.QDialogButtonBox( 
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        
        self.settings_widget_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        settings_widget_layout.addWidget(self.settings_widget_buttonBox)

        # Connect cancel signal
        # self.settings_widget_buttonBox.rejected.connect(self.close)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SettingsDialogUI()
    w.show()
    app.exec_()
