from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTimeEdit, QSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import QTime
from data_base_mapping import *
from functools import partial


class PlanningPage(QWidget):
    def __init__(self):
        super().__init__()
        font = self.font()
        font.setPointSize(font.pointSize() + 2)
        self.setFont(font)
        self.break_widgets = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)

        hl1 = QHBoxLayout()
        hl1.addWidget(QLabel("Wybierz linię produkcyjną:"))
        self.combo_line = QComboBox()
        self.combo_line.addItems(["Linia-A", "Linia-B", "Linia-C", "Linia-D"])
        self.combo_line.setCurrentIndex(0)
        hl1.addWidget(self.combo_line)
        self.main_layout.addLayout(hl1)

        hl2 = QHBoxLayout()
        hl2.addWidget(QLabel("Wybierz zmianę:"))
        self.combo_shift = QComboBox()
        self.combo_shift.addItems(["Zmiana-1", "Zmiana-2", "Zmiana-3"])
        self.combo_shift.setCurrentIndex(0)
        hl2.addWidget(self.combo_shift)
        self.main_layout.addLayout(hl2)

        hl_qty = QHBoxLayout()
        hl_qty.addWidget(QLabel("Planowana ilość:"))
        self.spin_quantity = QSpinBox()
        self.spin_quantity.setRange(0, 1000000)
        self.spin_quantity.setValue(0)
        hl_qty.addWidget(self.spin_quantity)
        self.main_layout.addLayout(hl_qty)

        hl_time = QHBoxLayout()
        hl_time.addWidget(QLabel("Czas pracy:"))
        hl_time.addStretch()
        self.time_start = QTimeEdit()
        self.time_start.setDisplayFormat('HH:mm')
        self.time_start.setTime(QTime(6, 0))
        self.time_start.setFixedWidth(100)
        hl_time.addWidget(self.time_start)
        hl_time.addWidget(QLabel("do:"))
        self.time_end = QTimeEdit()
        self.time_end.setDisplayFormat('HH:mm')
        self.time_end.setTime(QTime(14, 10))
        self.time_end.setFixedWidth(100)
        hl_time.addWidget(self.time_end)
        self.main_layout.addLayout(hl_time)

        self.dynamic_layout = QVBoxLayout()
        self.main_layout.addLayout(self.dynamic_layout)

        self.btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Dodaj przerwę")
        self.btn_add.setStyleSheet(
            "background-color: darkgreen; color: white; padding: 4px; font-size: 14px;"
        )
        self.btn_add.clicked.connect(partial(self.add_break, QTime(12, 12)))
        self.btn_remove = QPushButton("Usuń ostatnią przerwę")
        self.btn_remove.setStyleSheet(
            "background-color: darkred; color: white; padding: 4px; font-size: 14px;"
        )
        self.btn_remove.clicked.connect(self.remove_break)
        self.btn_layout.addWidget(self.btn_add)
        self.btn_layout.addWidget(self.btn_remove)
        self.btn_layout.addStretch()
        self.main_layout.addLayout(self.btn_layout)

        self.save_layout = QHBoxLayout()
        self.save_layout.addStretch()
        self.btn_save = QPushButton("Zapisz")
        self.btn_save.setStyleSheet(
            "background-color: green; color: white; padding: 4px; font-size: 14px;"
        )
        self.btn_save.clicked.connect(self.save_record)
        self.save_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(self.save_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Linia', 'Zmiana', 'Czas pracy od-do', 'Przerwy', 'Ilość [szt]',
                                              'Czas pracy [min]', 'Takt-Time [s]', "akcja"])
        self.main_layout.addWidget(self.table)

    def restore_defaults(self, line=0, shift=0, quantity=0, st_time=14, end_time=14):
        """Przywróć domyślne wartości formularza."""
        # line: int
        self.combo_line.setCurrentIndex(line)
        self.combo_shift.setCurrentIndex(shift)
        self.spin_quantity.setValue(quantity)
        self.time_start.setTime(st_time)
        self.time_end.setTime(end_time)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_save.setFixedWidth(int(self.width() * 0.25))

    def add_break(self, br_start=None, br_end=None):
        hl = QHBoxLayout()
        label = QLabel("Czas przerwy:")
        hl.addWidget(label)
        hl.addStretch()
        start = QTimeEdit()
        start.setDisplayFormat('HH:mm')
        start.setFixedWidth(100)
        start.setTime(br_start)
        hl.addWidget(start)
        label_do = QLabel("do:")
        hl.addWidget(label_do)
        end = QTimeEdit()
        end.setDisplayFormat('HH:mm')
        end.setFixedWidth(100)
        end.setTime(br_end)
        hl.addWidget(end)
        self.dynamic_layout.addLayout(hl)
        self.break_widgets.append((hl, [label, start, label_do, end]))

    def remove_break(self):
        if not self.break_widgets:
            return
        hl, widgets = self.break_widgets.pop()
        for w in widgets:
            w.setParent(None)
        while hl.count():
            item = hl.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        hl.deleteLater()

    def save_record(self):
        save_data_dict = {'line': None, 'shift': None, "quantity": None, "working_time_range": None, "brakes": None}

        line_idx = self.combo_line.currentIndex()
        shift_idx = self.combo_shift.currentIndex()
        quantity = self.spin_quantity.value()
        start_time = self.time_start.time().toPyTime()
        end_time = self.time_end.time().toPyTime()
        save_data_dict['line'] = line_idx
        save_data_dict['shift'] = shift_idx
        save_data_dict['quantity'] = quantity

        if start_time >= end_time:
            QMessageBox.warning(self, 'Błąd', 'Nieprawidłowy czas pracy.')
            return
        else:
            save_data_dict['working_time_range'] = [start_time, end_time]

        last_end = start_time
        if self.break_widgets:
            for _, widgets in self.break_widgets:
                st_t = widgets[1].time().toPyTime()
                en_t = widgets[3].time().toPyTime()
                if not (last_end <= st_t < en_t <= end_time):
                    QMessageBox.warning(self, 'Błąd', 'Przerwy poza zakresem.')
                    return
                else:
                    last_end = en_t
                    if save_data_dict['brakes'] is None:
                        save_data_dict['brakes'] = [[st_t, en_t]]
                    else:
                        save_data_dict['brakes'].append([st_t, en_t])

                    data = DataBaseTransfer(line=0, shift=0, save_data_dict=save_data_dict)
                    print(data.save_data_dict)

        else:
            data = DataBaseTransfer(line=0, shift=0, save_data_dict=save_data_dict)
            print(data.save_data_dict)

    def load_data(self):
        data_dictionary = DataBaseTransfer(line=0, shift=0).read_data()
        line_tuple = ("Linia-A", "Linia-B", "Linia-C", "Linia-D")
        shift_tuple = ("Zmiana-1", "Zmiana-2", "Zmiana-3")

        for i in range(len(data_dictionary)):
            btn_defaults = QPushButton("Edytuj")
            btn_defaults.setStyleSheet("padding: 4px; font-size: 14px;")
            btn_defaults.clicked.connect(partial(self.restore_defaults, data_dictionary[i]['line'],
                                                 data_dictionary[i]['shift'],
                                                 data_dictionary[i]['quantity'],
                                                 QTime(int(data_dictionary[i]['working_time_range'][0:2]),
                                                       int(data_dictionary[i]['working_time_range'][3:5])),
                                                 QTime(int(data_dictionary[i]['working_time_range'][6:8]),
                                                       int(data_dictionary[i]['working_time_range'][9:11]))))
            breaks = data_dictionary[i]['brakes'].split(" ")

            for remove in range(5):
                btn_defaults.clicked.connect(partial(self.remove_break))

            for break_time in breaks:
                if break_time:
                    btn_defaults.clicked.connect(partial(self.add_break,
                                                         QTime(int(break_time[0:2]),
                                                               int(break_time[3:5])),
                                                         QTime(int(break_time[6:8]),
                                                               int(break_time[9:11]))))

            data_dictionary[i]["button"] = btn_defaults

        self.table.setRowCount(len(data_dictionary))
        for i, row in enumerate(data_dictionary):
            self.table.setItem(i, 0, QTableWidgetItem(line_tuple[row['line']]))
            self.table.setItem(i, 1, QTableWidgetItem(shift_tuple[row['shift']]))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['working_time_range'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(row['brakes'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(row['quantity'])))
            self.table.setItem(i, 5, QTableWidgetItem(str(row['working_time'])))
            self.table.setItem(i, 6, QTableWidgetItem(str(row['takt_time'])))
            self.table.setCellWidget(i, 7, row['button'])
        self.table.resizeColumnsToContents()
