################################################################################
# TME FX Trishul Media Entertainment [Aug 2021]
################################################################################ 
""" Module user interface to submit / transfer files, from local to server.

@author Esteban Ortega <brutools@gmail.com>
"""

import json
import os
import sys

import subprocess

import resources

from PySide2 import QtCore, QtWidgets, QtGui

from submit_dialog_UI import SubmitDialogUI

class SubmitDialogCore(SubmitDialogUI):
    """ Adding functionality to submit dialog UI.
    """

    ## Store path to userSettings json
    # type: str
    _LOCATION_SETTINGS_JSON = "%HOMEPATH%/userSettings/locationSettings.json"

    ## Store the key for dictionary
    # type: str
    _KEY_SERVER_PATH = 'server_root_path'

    ## Store the key for dictionary
    # type: str
    _KEY_LOCAL_PATH = 'local_root_path'

    ## Store the base label text for labels in settings window.
    # type: str
    _PATH_LABEL = 'Current {} root path:\n{}'

    def __init__(self):
        super().__init__()

        self.setMinimumSize(400, 300)

        ########################################################################
        # Get root locations from json and set variables.
        # self.settings_json, self.local_path, self.server_path
        ########################################################################
        self.get_settings_json()

        ########################################################################
        # Connect signals
        ########################################################################
        self.submit_buttons.clicked.connect(self.on_button_clicked)
        self.list_widget.dropped.connect(self.on_drop_event)

        ########################################################################
        # Connect action signals
        ########################################################################
        self.set_directories_action.triggered.connect(self.on_set_locations_clicked)

        ########################################################################
        # Connect setting dialog signals
        ########################################################################
        self.settings_dialog.server_root_folder_button.clicked.connect(self.on_server_button_clicked)
        self.settings_dialog.local_root_folder_button.clicked.connect(self.on_local_button_clicked)

        self.settings_dialog.settings_widget_buttonBox.rejected.connect(self.on_cancel_button_clicked)
        self.settings_dialog.settings_widget_buttonBox.accepted.connect(self.on_ok_clicked)

    def on_ok_clicked(self):
        """ Executes when set locations Ok button is clicked.
        """

        settings_file = os.path.expandvars(self._LOCATION_SETTINGS_JSON)
        settings_file = os.path.join('C:', settings_file)
        settings_file_reformat = settings_file.replace('\\', '/')
        settings_dir = os.path.dirname(settings_file_reformat)

        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        settings_locations = {self._KEY_SERVER_PATH: self.server_path,
                              self._KEY_LOCAL_PATH: self.local_path  }

        with open(settings_file_reformat, 'w') as settings:
            json.dump(settings_locations, settings)
        
        self.show_info_msg('Settings_created!')

        self.settings_dialog.close()

        return
    
    def on_cancel_button_clicked(self):
        """ Executes when cancel button is clicked.
        """

        self.settings_dialog.close()
        self.close()

        return

    def on_local_button_clicked(self):
        """ Excecutes when local root folder button is clicked.
        """

        dialog_directory_widget = QtWidgets.QFileDialog()
        selected_path = dialog_directory_widget.getExistingDirectory(self, 
                                                                     'Select local root folder',
                                                                     "",
                                                                     QtWidgets.QFileDialog.Option.ShowDirsOnly)

        self.new_local_path = selected_path.replace('\\', '/')

        if self.new_local_path:
            self.local_path = self.new_local_path 
            local_label = self._PATH_LABEL.format('local', self.local_path)
            self.settings_dialog.local_location_label.setText(local_label)


        if self.server_path and self.local_path:
            self.settings_dialog.settings_widget_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.settings_dialog.settings_widget_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        return

    def on_server_button_clicked(self):
        """ Excecutes when sever root folder button is clicked.
        """

        dialog_directory_widget = QtWidgets.QFileDialog()
        selected_path = dialog_directory_widget.getExistingDirectory(self, 
                                                                     'Select server root folder',
                                                                     "",
                                                                     QtWidgets.QFileDialog.Option.ShowDirsOnly)

        self.new_server_path = selected_path.replace('\\', '/')

        if self.new_server_path:
            self.server_path = self.new_server_path 
            server_label = self._PATH_LABEL.format('server', self.server_path)
            self.settings_dialog.server_location_label.setText(server_label)


        if self.server_path and self.local_path:
            self.settings_dialog.settings_widget_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.settings_dialog.settings_widget_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        return

    def on_set_locations_clicked(self):
        """ Executes when set location menu is clicked.
        """

        if self.settings_json:
            server_path = self.server_path
            local_path = self.local_path
                        
        else:
            server_path = 'Not Set'
            local_path = 'Not Set'
        
        server_label = self._PATH_LABEL.format('server', server_path)
        self.settings_dialog.server_location_label.setText(server_label)

        local_label = self._PATH_LABEL.format('local', local_path)
        self.settings_dialog.local_location_label.setText(local_label)

        self.settings_dialog.show()

    def get_settings_json(self):
        """ Gets setting json if settings json file exists, None otherwise.
        Return:
            Dictionary {'local_root_path': '/Local/ADI_project/', 'server_root_path': '/server/ADI_project/'}
        """

        location_path = os.path.expandvars(self._LOCATION_SETTINGS_JSON)
        location_path = os.path.join('C:', location_path)
        location_path_reformat = location_path.replace('\\', '/')

        try: 
            with open(location_path_reformat, 'r') as settings:
                self.settings_json = json.load(settings)
                self.server_path = self.settings_json.get(self._KEY_SERVER_PATH, None)
                self.local_path = self.settings_json.get(self._KEY_LOCAL_PATH, None)

                return

        except FileNotFoundError:
            
            self.settings_json = None
            self.server_path = None
            self.local_path = None

            server_label = self._PATH_LABEL.format('server', 'Not Set')
            self.settings_dialog.server_location_label.setText(server_label)

            local_label = self._PATH_LABEL.format('local', 'Not Set')
            self.settings_dialog.local_location_label.setText(local_label)

            self.settings_dialog.show()

            return

    def on_drop_event(self, event):
        """ Triggers when something drop event happens.
        """

        for path in event:

            widgetItem = QtWidgets.QListWidgetItem()
            in_structure = True
            file_name = os.path.basename(path)

            if os.path.isfile(path):
                icon = QtGui.QIcon(":/icons/File_icon.png")
           
            else:
                icon = QtGui.QIcon(":/icons/Folder_icon.png")            

            if not self.check_adi_root_folder(path):
                widgetItem.setBackgroundColor(QtGui.QColor(255, 68, 0))
                in_structure = False

            widgetItem.setText(file_name)
            widgetItem.setData(5, (in_structure, path))
            widgetItem.setIcon(icon)
            
            self.list_widget.addItem(widgetItem)
        
        valid_items = self.get_valid_paths_item_from_listWidget()

        if not valid_items:
            self.submit_buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        else:
            self.submit_buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

        return

    def check_adi_root_folder(self, source_path):
        """ Checks if self.destination_path is part of the root folder.
        Args:
            source_path: String representing the stored path in item.
        """

        # root_folder = os.path.expandvars('%ADI_ROOT_FOLDER%')
        root_folder = self.local_path
        root_folder_reformat = root_folder.replace('\\', '/')
        
        source_root_folder = source_path[:len(root_folder)]

        if root_folder_reformat == source_root_folder:
            return True
        
        return False

    def on_button_clicked(self, signal):
        """ Triggers when a button is clicked.
        """

        if signal.text() == 'Cancel':
            self.close()
            return
        else:
            self.on_submit_button_clicked()
    
    def get_valid_paths_item_from_listWidget(self):
        """ Gets the valid items in QListWidget.
        Return:
            List of tuples (strings representing the full path to files, QListWidgetItem)
        """

        valid_item_paths = []

        for index_item in range(self.list_widget.count()):
            item = self.list_widget.item(index_item)

            in_structure, full_path = item.data(5)

            if in_structure:
                valid_item_paths.append((full_path, item))
            continue
            
        return valid_item_paths

    def on_submit_button_clicked(self):
        """ Executes steps whe submit buttons is clicked.
        """

        for element in self.get_valid_paths_item_from_listWidget():

            full_path, item = element
            status = None

            if os.path.isdir(full_path):

                for path, dirs, files in os.walk(full_path):
                    
                    if not files:
                        continue

                    for file in files:
                        full_path = os.path.join(path, file)

                        destination_path = self.compose_destination_path(full_path)

                        status = self.copy_files_folder(full_path, destination_path)

            else:
                destination_path = self.compose_destination_path(full_path)
                status = self.copy_files_folder(full_path, destination_path)

            if status == 0:
                item.setBackgroundColor(QtGui.QColor('lightGreen'))

            elif status is None:
                item.setBackgroundColor(QtGui.QColor('lightGray'))

            else:
                self.show_info_msg('Error occured with status {}'.format(status))

                return

        self.show_info_msg('Files copied!')

        return
        
    def copy_files_folder(self, source_path, destination_path):
        """ Copy files and folders into server.
        Args:
            source_path: String representing the full path name with
            file name if any.
            destination_path: String representing the full path name.
        """

        source_path = source_path.replace('/', '\\')
        destination_path = destination_path.replace('/', '\\')
        status = None

        if os.path.exists(destination_path):
            msg = 'File:\n{}\n already exists!, do you want to overwrite it?'.format(destination_path)
            answer = self.show_decision_msg(msg)

            if answer == QtWidgets.QMessageBox.Cancel:
                return       

        destination_dir_name = os.path.dirname(destination_path)

        if not os.path.exists(destination_dir_name):
            os.makedirs(destination_dir_name)

        status = subprocess.call('copy {} {}'.format(source_path, destination_path), shell=True)

        return status

    def compose_destination_path(self, full_path):
        """ Compose the destination directory based on passed full path.
        Args:
            full_path: String representing the full path of the source file.
        """

        # server_root_path = os.path.expandvars('%ADI_LOCAL_ROOT_FOLDER%')
        server_root_path = self.server_path
        server_root_path_reformat = os.path.normpath(server_root_path)
        full_path_root = full_path[:len(server_root_path)]
        full_path_root_reformat = os.path.normpath(full_path_root)

        if server_root_path_reformat == full_path_root_reformat:

            self.show_info_msg('Same root folder.')

            return
        
        ## from provided path, remove the part of the source path
        server_root_path_reformat = server_root_path_reformat.replace('\\', '/')
        full_path_no_root = full_path[len(self.local_path) + 1:]
        destination_path = os.path.join(server_root_path_reformat, full_path_no_root)
        destination_path_reformat = os.path.normpath(destination_path)
        destination_path_reformat = destination_path_reformat.replace('\\', '/')
        
        return destination_path_reformat

    def show_info_msg(self, msg):
        """ Creates a generic msg box with ok button.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 
                                                 'Information',
                                                 msg, 
                                                 QtWidgets.QMessageBox.Ok)

    def show_decision_msg(self, msg):
        """ Creates a generic msg box with ok button and cancel button.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 'Confirm action',
            msg, QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SubmitDialogCore()
    w.show()
    app.exec_()
