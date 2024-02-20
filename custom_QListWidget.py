################################################################################
# TME FX Trishul Media Entertainment [Aug 2021]
################################################################################ 
""" Module custom QListWidget implementation to enable drag and drop
functionality.

@author Esteban Ortega <brutools@gmail.com>
"""

from PySide2 import QtWidgets, QtCore

class CustomListBoxWidget(QtWidgets.QListWidget):
    """ Custom listBox widget enabling drag and drop functionality.
    """

    dropped = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setAcceptDrops(True)
        self.resize(600, 600)


    def dragEnterEvent(self, event):
        """ Handler is called when a drag is in progress and the mouse enters
        this widget.
        """
        if event.mimeData().hasUrls:
            event.accept()

        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """ Handler is called when a draq is in progress, and when any of the
        following conditions occur:
        - Cursor enters this widget.
        - Cursos moves within this widget.
        - A modifier key is pressed on the keyboard while this widget has
        the focus.
        """

        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

        else:
            event.ignore()
    
    def dropEvent(self, event):
        """ Handler is called when drop event to unpack dropped data
        in a proper way for the widget.
        """

        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            paths = []    

            for url in event.mimeData().urls():
                
                if url.isLocalFile():
                    full_path = url.toLocalFile()

                    paths.append(full_path)

            self.dropped.emit(paths)
        
        else:
            event.ignore()

        return

    def keyPressEvent(self, event):
        """ Overriding key delete press event.
        """

        if event.key() == QtCore.Qt.Key_Delete:            
            row = self.currentRow()
            self.takeItem(row)

        else:
            super().keyPressEvent(event)

        return
