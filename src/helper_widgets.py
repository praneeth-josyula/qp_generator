import os.path
import json
from global_vars import GlobalVars
from PyQt5 import QtWidgets, QtCore
from ui_definitions import Ui_NewQPDialog


class NewQPWidget(QtWidgets.QDialog, Ui_NewQPDialog):

    def __init__(self, extension = '.qp'):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._initialize_defaults()
        self.gv = GlobalVars()
        self.new_file = ''
        self.extension = extension

        # Connecting the signals and slots
        self.create_qp_push_button.clicked.connect(self.create_qp_clicked)
        self.cancel_push_button.clicked.connect(self.cancel_qp_clicked)
        self.qp_path_tool_button.clicked.connect(self.qp_path_clicked)
        self.qp_filename_line_edit.textChanged.connect(self.filename_line_edit_changed)
        self.qp_path_line_edit.textChanged.connect(self.path_line_edit_changed)

    #    Slots:
    def filename_line_edit_changed(self):
        self.qp_filename = self.qp_filename_line_edit.text()

    def path_line_edit_changed(self):
        self.qp_path = self.qp_path_line_edit.text()

    def create_qp_clicked(self):
        # Checking to see if the values are valid
        if not (self.qp_path_line_edit.text()) or not (self.qp_filename_line_edit.text()):
            QtWidgets.QMessageBox.critical(self, 'Error Creating', 'The input fields are invalid',
                                           QtWidgets.QMessageBox.Ok)
            return
        if not (self.get_file_extension(self.qp_filename_line_edit.text()) == self.extension):
            self.qp_filename = self.qp_filename + self.extension
        self.setEnabled(False)
        # Creating a new instance of GeneratorMainWindow, after creating and loading the file
        if os.name == 'posix':
            self.new_file = QtCore.QDir(self.qp_path + '/' + self.qp_filename).path()
        elif os.name == 'nt':
            self.new_file = QtCore.QDir(self.qp_path + '\\' + self.qp_filename).path()
        print("Creating new qp file " + self.new_file)
        q_file = QtCore.QFile(self.new_file)
        if not q_file.open(QtCore.QFile.ReadWrite):
            QtWidgets.QMessageBox.critical(self, 'Error Creating', 'Unable to create the file !',
                                           QtWidgets.QMessageBox.Ok)
            return
        q_file.close()
        self.new_qp_full_path = self.new_file
        file = open(self.new_file, "w", encoding="utf-8")
        if self.extension == '.qp':
            json.dump(self.gv.default_qp_values, file)

        elif self.extension == '.qpd':
            json.dump(self.gv.default_qpd_values, file)
        file.close()
        self.done(1)

    def cancel_qp_clicked(self):
        self.close()

    def qp_path_clicked(self):
        self.qp_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose path', self.qp_path,
                                                                  QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        self.qp_path_line_edit.setText(self.qp_path)

    #   Class methods:

    def _initialize_defaults(self):
        self.qp_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
        self.qp_path_line_edit.setText(self.qp_path)
        self.qp_filename = 'untitled.qp'
        self.qp_filename_line_edit.setText(self.qp_filename)

    def get_file_extension(self, file):
        return os.path.splitext(file)[1]


class OpenQPWidget(QtWidgets.QFileDialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.open_file = self.getOpenFileName(self, 'Open Question paper', str(QtCore.QStandardPaths.DocumentsLocation),
                             'Question Paper (*.qp)')[0]
        if not self.open_file:
            return

