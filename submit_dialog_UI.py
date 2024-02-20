################################################################################
# TME FX Trishul Media Entertainment [Aug 2021]
################################################################################ 
""" Module user interface to submit / transfer files, from local to server.

@author Esteban Ortega <brutools@gmail.com>
"""

import sys

from PySide2 import QtWidgets

from custom_QListWidget import CustomListBoxWidget
from settings_dialog_UI import SettingsDialogUI

class SubmitDialogUI(QtWidgets.QMainWindow):
    """ Main window for submit UI app.
    """

    def __init__(self):
        super(SubmitDialogUI, self).__init__()

        self.setWindowTitle('Submit files')

        central_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(central_widget)

        ########################################################################
        # Create mune bar, menu and actions.
        ########################################################################
        self.create_actions()
        self.create_menu_bar()

        ########################################################################
        # Create settings UI
        ########################################################################
        self.settings_dialog = SettingsDialogUI()

        ########################################################################
        # Submit layout / widgets
        ########################################################################
        submit_widget = QtWidgets.QWidget()
        submit_widget_layout = QtWidgets.QVBoxLayout()
        submit_widget.setLayout(submit_widget_layout)

        self.list_widget = CustomListBoxWidget()

        submit_widget_layout.addWidget(self.list_widget)

        ########################################################################
        # Button box
        ########################################################################
        self.submit_buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
        QtWidgets.QDialogButtonBox.Cancel)
        self.submit_buttons.button(QtWidgets.QDialogButtonBox.Ok).setText('Submit')
        self.submit_buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        submit_widget_layout.addWidget(self.submit_buttons)

        ########################################################################
        # Adding Tabs
        ########################################################################
        central_widget.addTab(submit_widget, 'Submit To Server')

        ########################################################################
        # Connect action signals
        ########################################################################
        # self.set_directories_action.triggered.connect(self.settings_dialog.show)


    def create_actions(self):
        """ Create all required actions for the menues to use.
        Return:
            None value.
        """

        # Action for settings menu.
        ########################################################################
        self.set_directories_action = QtWidgets.QAction('&Set_locations...', self)

        return

    def create_menu_bar(self):
        """ Create a menun bar and menus.
        Return:
            None value.
        """

        # Settings menu bar
        ########################################################################
        main_menu_bar = self.menuBar()
        settings_menu = main_menu_bar.addMenu('&Settings')
        settings_menu.addAction(self.set_directories_action)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SubmitDialogUI()
    w.show()
    app.exec_()
