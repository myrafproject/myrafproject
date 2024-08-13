from logging import getLogger
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QDialog, QVBoxLayout, QListWidget, QDialogButtonBox

from myraflib import Fits

SCHEMA = custom_colors = {"primary": "#D0BCFF"}


class MultiSelectDialog(QDialog):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.selected_items = []

        self.setWindowTitle('Select Items')

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget(self)
        self.list_widget.addItems(items)
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def accept(self):
        self.selected_items = [item.text() for item in self.list_widget.selectedItems()]
        super().accept()


class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __hash__(self):
        return id(self)


class GUIFunctions:
    def __init__(self, logger=None):

        if logger is None:
            self.logger = getLogger(__file__)
        else:
            self.logger = logger

    def error(self, parent, text):
        QMessageBox.critical(parent, "MYRaf", text)

    def warning(self, parent, text):
        QMessageBox.warning(parent, "MYRaf", text)

    def get_file(self, parent, caption, file_type=None):
        try:
            if file_type is not None:
                file_type_to_use = file_type
            else:
                file_type_to_use = "fits, fit, fts (*.fits *.fit *.fts)"

            file, _ = QtWidgets.QFileDialog.getOpenFileName(parent, caption, '', file_type_to_use)
            return file
        except Exception as e:
            self.logger.error(e)
            return ""

    def get_files(self, parent, caption, file_type=None):
        try:
            if file_type is not None:
                file_type_to_use = file_type
            else:
                file_type_to_use = "fits, fit, fts (*.fits *.fit *.fts)"

            files, _ = QtWidgets.QFileDialog.getOpenFileNames(parent, caption, '', file_type_to_use)
            return files
        except Exception as e:
            self.logger.error(e)
            return []

    def get_directory(self, parent, caption):
        try:
            directory = QtWidgets.QFileDialog.getExistingDirectory(parent, caption)
            return directory
        except Exception as e:
            self.logger.error(e)
            return ""

    def save_file(self, parent, caption, file_type_to_use):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(parent, caption, filter=file_type_to_use)

        return file

    def add_to_files(self, parent, images_to_add, device, grp="Group"):
        if len(images_to_add) == 0:
            return

        try:
            progress = QtWidgets.QProgressDialog("Adding files...", "Abort", 0, len(images_to_add), parent)

            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
            progress.setWindowTitle('MYRaf: Please Wait')
            progress.setAutoClose(True)

            group_layer = CustomQTreeWidgetItem(device, [grp])
            for iteration, file in enumerate(images_to_add):
                fits = Fits(Path(file))
                progress.setLabelText(f"Adding {fits.path.name}")

                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                group_layer.setFirstColumnSpanned(True)

                file_name_layer = CustomQTreeWidgetItem(group_layer, [fits.path.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", fits.path.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                statistics = fits.stats
                for key, value in statistics.items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            progress.close()

        except Exception as e:
            self.logger.error(e)

    def get_selected_files(self, tree_widget):
        selected_items_dict = {}

        def traverse_item(item: QTreeWidgetItem):
            if item.isSelected():
                selected_items_dict[item] = []
                child_count = item.childCount()
                for i in range(child_count):
                    child = item.child(i)
                    selected_items_dict[item].append(child)
            else:
                child_selected = []
                child_count = item.childCount()
                for i in range(child_count):
                    child = item.child(i)
                    if child.isSelected():
                        child_selected.append(child)
                if child_selected:
                    selected_items_dict[item] = child_selected

        root_count = tree_widget.topLevelItemCount()
        for i in range(root_count):
            root = tree_widget.topLevelItem(i)
            traverse_item(root)

        return selected_items_dict

    def remove_from_files(self, tree_widget):
        selected_items_dict = self.get_selected_files(tree_widget)
        for parent, children in selected_items_dict.items():
            for child in children:
                parent.removeChild(child)

            if parent.childCount() == 0:
                tree_widget.takeTopLevelItem(tree_widget.indexOfTopLevelItem(parent))

    def get_number(self, parent, caption, text, min_val=0, max_val=100, step_val=1, default=0):
        number, ok = QtWidgets.QInputDialog.getInt(
            parent, caption, text, min=min_val, max=max_val, step=step_val, value=default
        )
        return number, ok

    def get_text(self, parent, caption, text, default=None):
        text, ok = QtWidgets.QInputDialog.getText(parent, caption, text, text=default)
        return text, ok

    def get_item(self, parent, caption, label, items):
        item, ok = QtWidgets.QInputDialog.getItem(parent, caption, label, items)
        return item, ok

    def ask(self, parent, caption, question):
        answer = QtWidgets.QMessageBox.question(parent, caption, question,
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)

        return answer == QtWidgets.QMessageBox.Yes

    def add_to_combo(self, combo_widget, items):
        combo_widget.addItems(items)

    def clear_table(self, table_widget):
        while table_widget.rowCount() > 0:
            table_widget.removeRow(0)

    def get_from_table(self, table_widget):
        number_of_rows = table_widget.rowCount()
        number_of_columns = table_widget.columnCount()
        ret = []
        if number_of_rows > 0 and number_of_columns > 0:
            for i in range(number_of_rows):
                row = []
                for j in range(number_of_columns):
                    row.append(table_widget.item(i, j).text())

                ret.append(row)

            return ret

        return []

    def get_from_table_selected(self, table_widget):
        ret = []
        for i in table_widget.selectionModel().selectedRows():
            row = []
            for j in range(table_widget.columnCount()):
                row.append(table_widget.item(i.row(), j).text())
            ret.append(row)

        return ret

    def add_to_table(self, table_widget, data):
        for line in data:
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)
            for it, value in enumerate(line):
                table_widget.setItem(row_position, it, QtWidgets.QTableWidgetItem(str(value)))

    def add_to_list(self, list_widget, data):
        it = list_widget.count() - 1
        for x in data:
            it = it + 1
            item = QtWidgets.QListWidgetItem()
            list_widget.addItem(item)
            item = list_widget.item(it)
            item.setText(x)

    def get_from_list(self, list_widget):
        return [
            list_widget.item(x).text()
            for x in range(list_widget.count())
        ]

    def get_from_list_selected(self, list_widget):
        return [
            x.text()
            for x in list_widget.selectedItems()
        ]

    def remove_from_list(self, list_widget):
        for x in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(x))
