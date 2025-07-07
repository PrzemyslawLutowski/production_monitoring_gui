import psycopg2
import json


class DataBaseTransfer:
    def __init__(self, line, shift, save_data_dict=None):
        self.line = line
        self.shift = shift
        self.save_data_dict = save_data_dict
        self.config = False
        self.connected = False

    def open_config_file(self, file_name):

        try:

            with open(file_name, "r", encoding="utf-8") as config_file:
                jason_file_df = json.load(config_file)

        except FileNotFoundError:
            jason_file_df = False

        return jason_file_df

    def create_db_connection(self):
        self.config = self.open_config_file("../config.json")

        DATABASE_HOST = self.config["db_config"]["host"]
        DATABASE_USER = self.config["db_config"]["user"]
        DATABASE_PASSWORD = self.config["db_config"]["password"]
        DATABASE_NAME = self.config["db_config"]["dbname"]
        PORT = self.config["db_config"]["port"]

        try:

            self.connected = psycopg2.connect(
                database=DATABASE_NAME,
                user=DATABASE_USER,
                host=DATABASE_HOST,
                password=DATABASE_PASSWORD,
                port=PORT
            )

        except KeyError:
            self.connected = False

    def read_data(self):
        read_data_list = []

        self.create_db_connection()
        current = self.connected.cursor()

        query = ('select * '
                 'from plan_result_productionlines prpl '
                 'join plan_result_plannedworkingtime prpw on prpl.planned_working_time_id = prpw.id '
                 'join plan_result_planresultquantity plt on prpl.plan_result_id = plt.id '
                 'where production_line=%(line)s ')
        current.execute(query, {"line": self.line})
        data = current.fetchall()

        for i in range(len(data)):
            read_data_list.append({'line': None, 'shift': None, "working_time_range": None, "brakes": "",
                                            "quantity": None, "working_time": None, "takt_time": None})

            read_data_list[i]['line'] = data[i][1]
            read_data_list[i]['shift'] = data[i][4]
            read_data_list[i]['working_time_range'] = f"{str(data[i][7])[0:5]}-{str(data[i][8])[0:5] }"
            read_data_list[i]["quantity"] = data[i][11]
            read_data_list[i]["working_time"] = str(data[i][13] / 60)[0:3]
            read_data_list[i]["takt_time"] = data[i][14]

            query_breaks = 'select * from plan_result_plannedbreaktime where production_line_id=%(id)s '
            current.execute(query_breaks, {"id": data[i][0]})
            data_breaks = current.fetchall()

            for break_time in data_breaks:
                read_data_list[i]["brakes"] += f"{str(break_time[1])[0:5]}-{str(break_time[2])[0:5]} "

        self.connected.close()

        return read_data_list

    def save_data(self):
        return self.save_data_dict


if __name__ == "__main__":
    DataBaseTransfer(line=0, shift=0).read_data()
