from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

SCHEMA = custom_colors = {"primary": "#D0BCFF"}


def reload_combo(device, items):
    device.clear()
    device.addItems(items)


def reload_list(device, items):
    reload_combo(device, items)


def get_list(device):
    return [device.item(x).text() for x in range(device.count())]


def error(parent, text):
    QMessageBox.critical(parent, "MYRaf", text)


def save_file(parent, caption, file_type, name):
    file, _ = QtWidgets.QFileDialog.getSaveFileName(parent, caption, name, (file_type),
                                                    None, QtWidgets.QFileDialog.DontUseNativeDialog)

    return file


def get_files(parent, caption, file_type=None):
    if file_type is not None:
        ftype = file_type
    else:
        ftype = "fits, fit, fts (*.fits *.fit *.fts)"

    files = QtWidgets.QFileDialog.getOpenFileNames(parent, caption, '', (ftype), None,
                                                   QtWidgets.QFileDialog.DontUseNativeDialog)
    return files[0]


def ask(parent, caption, question):
    answer = QtWidgets.QMessageBox.question(parent, caption, question,
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                            QtWidgets.QMessageBox.No)

    return answer == QtWidgets.QMessageBox.Yes


def get_text(parent, caption, text, default=None):
    text, ok = QtWidgets.QInputDialog.getText(parent, caption, text, text=default)
    return text


def get_number(parent, caption, text, default=0):
    number, ok = QtWidgets.QInputDialog.getInt(parent, caption, text, min=0, max=100, step=1, value=default)
    return number


def add_to_files(images_to_add, device, grp="Group"):
    try:
        group_layer = QtWidgets.QTreeWidgetItem(device, [grp])
        for file, statistics in images_to_add:
            path = Path(file)
            group_layer.setFirstColumnSpanned(True)

            file_name_layer = QtWidgets.QTreeWidgetItem(group_layer, [path.name])
            file_name_layer.setFirstColumnSpanned(True)

            item = QtWidgets.QTreeWidgetItem(file_name_layer, ["Path", path.resolve().parent.__str__()])
            item.setFlags(QtCore.Qt.ItemIsEnabled)

            for key, value in statistics.items():
                item = QtWidgets.QTreeWidgetItem(file_name_layer, [key, f"{value:.2f}"])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
    except Exception as e:
        print(e)


def tree_toplevel_count(device):
    return len(tree_selected_toplevel_items(device))


def tree_selected_toplevel_items(tree_widget):
    selected_items = []
    top_level_count = tree_widget.topLevelItemCount()
    for i in range(top_level_count):
        item = tree_widget.topLevelItem(i)
        if item.isSelected():
            selected_items.append(item)
    return selected_items


def get_selected_tree(device, selected=False):
    ret = []
    if selected:
        ret = []
        getSelected = device.selectedItems()
        for element in getSelected:
            ret.append(element)
    else:
        iterator = QtWidgets.QTreeWidgetItemIterator(device, QtWidgets.QTreeWidgetItemIterator.HasChildren)
        while iterator.value():
            ret.append(iterator.value())
            iterator += 1

    return ret


def rm_from_tree(device):
    selected = device.selectedItems()
    if selected:
        for item in selected:
            if item.parent() is not None and item.parent().parent() is None:
                parent_item = item.parent()
                parent_item.removeChild(item)


def clear_table(device):
    for i in reversed(range(device.rowCount())):
        device.removeRow(i)


def add_to_table(device, data):
    for line in data:
        row_position = device.rowCount()
        device.insertRow(row_position)
        for it, value in enumerate(line):
            device.setItem(row_position, it, QtWidgets.QTableWidgetItem(str(value)))


def get_table(device):
    number_of_rows = device.rowCount()
    number_of_columns = device.columnCount()
    ret = []
    if number_of_rows > 0 and number_of_columns > 0:
        for i in range(number_of_rows):
            row = []
            for j in range(number_of_columns):
                row.append(device.item(i, j).text())

            ret.append(row)

        return ret
