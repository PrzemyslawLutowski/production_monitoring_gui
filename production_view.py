from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from sqlalchemy import create_engine, text, select
from datetime import datetime
from create_widget import (create_section_widget, create_label_widget, create_time_widget, create_plan_value_widget,
                           create_balance_value_widget, create_status_widget)
import json
import sys


class ProductionLineMonitoring(QWidget):
    def __init__(self):
        super().__init__()
        self.db_data_update_timer = QTimer()
        self.db_data_update_timer.timeout.connect(self.data_update)
        self.config = None
        self.engine = None
        self.header_label = None
        self.label_grid = None
        self.variables_values = {}
        self.status_blink_timer = QTimer()
        self.status_blink_timer.timeout.connect(self.status_blink_red)
        self.line_blink_state = False
        self.setWindowTitle("Production Monitor")
        self.setGeometry(100, 100, 800, 400)  # Rozmiar okna
        self.red = "background-color: red; color: white; font-weight: bold; padding: 5px; border-radius: 5px;"
        self.light_red = "background-color: #ff6666; color: black; font-weight: bold; padding: 5px; border-radius: 5px;"
        self.green = "background-color: green; color: white; font-weight: bold; padding: 5px; border-radius: 5px;"
        self.init_UI()

    def error_view_UI(self, message):
        main_layout = QVBoxLayout()
        gird = QGridLayout()
        gird_error = create_section_widget(
            f"{message} \n czytaj README",
            baseFontSize=20)
        gird.addWidget(gird_error)
        main_layout.addLayout(gird)
        self.setLayout(main_layout)

    def open_config_file(self, file_name):

        try:

            with open(file_name, "r", encoding="utf-8") as config_file:
                jason_file_df = json.load(config_file)

        except FileNotFoundError:
            jason_file_df = False
            self.error_view_UI(message="Brak pliku config.json")

        return jason_file_df

    def create_db_engine(self):
        print("tutaj")
        try:

            DB_CONFIG = {
                "dbname": self.config["db_config"]["dbname"],
                "user": self.config["db_config"]["user"],
                "password": self.config["db_config"]["password"],
                "host": self.config["db_config"]["host"],
                "port": self.config["db_config"]["port"]
            }

            db_url = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
            self.engine = create_engine(db_url)


        except KeyError:
            self.engine = False

    def init_UI(self):
        self.config = self.open_config_file("config.json")

        if self.config:
            initial_one_characters = "&&&&&&&"
            initial_two_characters = f"&&&&&&& \n &&&&&&&"

            plan_base_font_size = 30
            result_base_font_size = 40
            current_base_font_size = 40
            position_base_font_size = 10

            main_layout = QVBoxLayout()

            # Nagłówek
            top_grid = QGridLayout()
            self.header_label = QLabel()
            pixmap = QPixmap("Logo.png")
            self.header_label.setPixmap(pixmap)
            self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.time_value = create_time_widget(initial_one_characters, baseFontSize=result_base_font_size)

            setattr(self, list(self.config.keys())[0],
                    create_time_widget(self.config[list(self.config.keys())[0]], baseFontSize=current_base_font_size))
            setattr(self, list(self.config.keys())[1],
                    create_time_widget(initial_one_characters, baseFontSize=result_base_font_size))
            setattr(self, list(self.config.keys())[2],
                    create_plan_value_widget(initial_one_characters, baseFontSize=plan_base_font_size))
            setattr(self, list(self.config.keys())[3],
                    create_plan_value_widget(initial_one_characters, baseFontSize=plan_base_font_size))
            setattr(self, list(self.config.keys())[4],
                    create_balance_value_widget(initial_one_characters, baseFontSize=result_base_font_size))
            setattr(self, list(self.config.keys())[5],
                    create_balance_value_widget(initial_one_characters, baseFontSize=result_base_font_size))

            top_grid.addWidget(self.time_value, 0, 0)
            top_grid.addWidget(self.header_label, 0, 3)
            top_grid.addWidget(getattr(self, list(self.config.keys())[0]), 0, 2)
            top_grid.addWidget(getattr(self, list(self.config.keys())[1]), 0, 1)
            top_grid.addWidget(getattr(self, list(self.config.keys())[2]), 1, 0)
            top_grid.addWidget(getattr(self, list(self.config.keys())[3]), 1, 1)
            top_grid.addWidget(getattr(self, list(self.config.keys())[4]), 1, 2)
            top_grid.addWidget(getattr(self, list(self.config.keys())[5]), 1, 3)
            main_layout.addLayout(top_grid)

            # Sekcja trzech głównych kategorii: Assembly, Inspection, Packing
            category_grid = QGridLayout()

            setattr(self, list(self.config.keys())[6],
                    create_section_widget(initial_two_characters, baseFontSize=current_base_font_size))
            setattr(self, list(self.config.keys())[7],
                    create_section_widget(initial_two_characters, baseFontSize=current_base_font_size))
            setattr(self, list(self.config.keys())[8],
                    create_section_widget(initial_two_characters, baseFontSize=current_base_font_size))
            setattr(self, list(self.config.keys())[9],
                    create_section_widget(initial_two_characters, baseFontSize=current_base_font_size))

            category_grid.addWidget(getattr(self, list(self.config.keys())[6]), 0, 0)
            category_grid.addWidget(getattr(self, list(self.config.keys())[7]), 0, 1)
            category_grid.addWidget(getattr(self, list(self.config.keys())[8]), 0, 2)
            category_grid.addWidget(getattr(self, list(self.config.keys())[9]), 0, 3)

            main_layout.addLayout(category_grid)

            # Dolna sekcja etykiet
            label_grid = QGridLayout()
            labels = [[], []]

            for i in range(17, 22):
                labels[0].append(list(self.config.keys())[i])

            for i in range(22, 27):
                labels[1].append(list(self.config.keys())[i])

            for row in range(len(labels)):

                for col in range(len(labels[row])):

                    if labels[row][col]:
                        label = create_label_widget(labels[row][col], baseFontSize=position_base_font_size)
                        label_grid.addWidget(label, row, col)

            main_layout.addLayout(label_grid)

            self.label_grid = label_grid
            self.setLayout(main_layout)
            self.update_font_sizes()
            self.db_data_update_timer.start(5000)

    def data_update(self):
        self.create_db_engine()

        if self.engine:

            try:

                self.engine.connect()

            except:

                self.engine = False
                self.time_value.setText("Brak połączenia z db")
                self.time_value.setStyleSheet(self.light_red)

        if self.engine:

            variables_tuple = ()

            for i in range(1, 28):

                variables_tuple = variables_tuple + (self.config[list(self.config.keys())[i]], )

            query = text("SELECT variable_name, cycle_time, variable_value "
                         "FROM variables_variablesmodel WHERE variable_name IN :variables")

            with self.engine.connect() as connect:
                values = connect.execute(query, {
                    "variables": variables_tuple}).fetchall()

            for i in range(1, 28):

                for value in values:

                    if value[0] == self.config[list(self.config.keys())[i]]:
                        self.variables_values[list(self.config.keys())[i]] = [value[1], value[2]]

            self.header_update()

    def header_update(self):
        self.time_value.setText(datetime.now().strftime("%H:%M"))
        self.time_value.setStyleSheet(None)
        view_status = getattr(self, list(self.variables_values.keys())[0])
        variable_value = self.variables_values[(list(self.variables_values.keys())[0])][1]

        if variable_value == '1':
            view_status.setText("ON")
            view_status.setStyleSheet(self.green)

        else:
            view_status.setText("OFF")
            view_status.setStyleSheet(self.light_red)

        self.plan_and_balance_values_update()

    def plan_and_balance_values_update(self):

        for i in range(1, 5):
            values = self.variables_values[(list(self.variables_values.keys())[i])]

            if i % 2 > 0:
                getattr(self, list(self.variables_values.keys())[i]).setText(f"{values[0]}s")

            else:
                getattr(self, list(self.variables_values.keys())[i]).setText(f"{values[1]}szt")

                if i == 4:
                    balance_style_sheet = getattr(self, list(self.variables_values.keys())[i])

                    if int(values[1]) < 0:
                        balance_style_sheet.setStyleSheet(
                            f"background-color: #ff6666; color: black; font-weight: bold; padding: 5px;")

                    else:
                        balance_style_sheet.setStyleSheet(
                            f"background-color: white; color: black; font-weight: bold; padding: 5px;")

        self.current_production_values_update()

    def current_production_values_update(self):
        scan_in_values = self.variables_values[(list(self.variables_values.keys())[5])]
        hvt_values = self.variables_values[(list(self.variables_values.keys())[6])]
        tv_tracer_values = self.variables_values[(list(self.variables_values.keys())[7])]
        pac_values = self.variables_values[(list(self.variables_values.keys())[8])]

        getattr(self, list(self.variables_values.keys())[5]).setText(f"{scan_in_values[1]}szt \n {scan_in_values[0]}s")
        getattr(self, list(self.variables_values.keys())[6]).setText(f"{hvt_values[1]}szt \n {hvt_values[0]}s")
        getattr(self, list(self.variables_values.keys())[7]).setText(f"{tv_tracer_values[1]}szt \n {tv_tracer_values[0]}s")
        getattr(self, list(self.variables_values.keys())[8]).setText(f"{pac_values[1]}szt \n {pac_values[0]}s")

        self.status_blink_timer.start(750)

    def status_blink_red(self):
        j = 5
        for i in range(12, 16):
            line_widget = getattr(self, list(self.variables_values.keys())[j])
            values = self.variables_values[(list(self.variables_values.keys())[i])][1]

            if values == "1":

                if self.line_blink_state:
                    line_widget.setStyleSheet(self.red)

                else:
                    line_widget.setStyleSheet(self.light_red)

            else:
                line_widget.setStyleSheet(self.green)
            j += 1

        i = 16

        for row in range(self.label_grid.rowCount()):

            for col in range(self.label_grid.columnCount()):
                position = self.label_grid.itemAtPosition(row, col)
                position_label = position.widget()
                values = self.variables_values[(list(self.variables_values.keys())[i])][1]

                if values == "1":

                    if self.line_blink_state:
                        position_label.setStyleSheet(self.red)

                    else:
                        position_label.setStyleSheet(self.light_red)

                else:
                    position_label.setStyleSheet(self.green)

                i += 1

        self.line_blink_state = not self.line_blink_state

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_font_sizes()

    def update_font_sizes(self):
        scale = min(self.width() / 800, self.height() / 400)

        for label in self.findChildren(QLabel):
            base = label.property("baseFontSize")

            if base:
                font = label.font()
                newSize = min(120, max(60, int(base * scale)))
                font.setPixelSize(newSize)
                label.setFont(font)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductionLineMonitoring()
    window.show()
    sys.exit(app.exec())
