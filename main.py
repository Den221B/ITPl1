import sys

import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QLabel,
                             QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.add_row_button = None
        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Выберите таблицу для редактирования")
        self.combo_box.addItem("Учителя")
        self.combo_box.addItem("Предметы")
        self.combo_box.addItem("1-ая неделя")
        self.combo_box.addItem("2-ая неделя")
        self.combo_box.currentTextChanged.connect(self.on_combobox_changed)

        # Создаем QLabel для вывода выбранного элемента
        self.label = QLabel(self)
        self.table_widget = QTableWidget(self)

        # Создаем QVBoxLayout для размещения виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def on_combobox_changed(self, s):
        self.table_widget.clear()
        if s == '1-ая неделя':
            self.cursor.execute(
                "SELECT days.id, s1, k1, t1, s2, k2, t2, s3, k3, t3, s4, k4, t4, s5, k5, t5 FROM days JOIN kabs ON days.id = kabs.id")
            data = self.cursor.fetchall()
            data = data[1:7]
            print(data)
            da = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(19)
            self.table_widget.setColumnHidden(1, True)
            for row, item in enumerate(data):
                self.table_widget.setItem(row, 0, QTableWidgetItem(da[row]))
                for col, val in enumerate(item):
                    self.table_widget.setItem(row, col + 1, QTableWidgetItem(str(val)))
                self.update_row_button = QPushButton("Обновить")
                self.table_widget.setCellWidget(row, 17, self.update_row_button)
                self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
                self.delete_row_button = QPushButton("Удалить")
                self.table_widget.setCellWidget(row, 18, self.delete_row_button)
                self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))

            self.table_widget.setHorizontalHeaderLabels(
                ['День недели','id', '1-ая пара', '1-ая пара (кабинет)', '1-ая пара (время)', '2-ая пара',
                 '2-ая пара (кабинет)', '2-ая пара (время)', '3-ая пара', '3-ая пара (кабинет)', '3-ая пара (время)',
                 '4-ая пара', '4-ая пара (кабинет)', '4-ая пара (время)', '5-ая пара', '5-ая пара (кабинет)',
                 '5-ая пара (время)'])
            self.add_row_button = QPushButton("Добавить новую строчку")
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 17, self.add_row_button)
            self.add_row_button.clicked.connect(lambda: self.add_row(s))

        if s == '2-ая неделя':
            self.cursor.execute(
                "SELECT days.id, s1, k1, t1, s2, k2, t2, s3, k3, t3, s4, k4, t4, s5, k5, t5 FROM days JOIN kabs ON days.id = kabs.id")
            data = self.cursor.fetchall()
            data = data[7:13]
            da = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(18)
            self.table_widget.setColumnHidden(1, True)
            for row, item in enumerate(data):
                self.table_widget.setItem(row, 0, QTableWidgetItem(da[row]))
                for col, val in enumerate(item):
                    self.table_widget.setItem(row, col + 1, QTableWidgetItem(str(val)))
                self.update_row_button = QPushButton("Обновить")
                self.table_widget.setCellWidget(row, 16, self.update_row_button)
                self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
                self.delete_row_button = QPushButton("Удалить")
                self.table_widget.setCellWidget(row, 17, self.delete_row_button)
                self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))
            self.table_widget.setHorizontalHeaderLabels(
                ['День недели','id', '1-ая пара', '1-ая пара (кабинет)', '1-ая пара (время)', '2-ая пара',
                 '2-ая пара (кабинет)', '2-ая пара (время)', '3-ая пара', '3-ая пара (кабинет)', '3-ая пара (время)',
                 '4-ая пара', '4-ая пара (кабинет)', '4-ая пара (время)', '5-ая пара', '5-ая пара (кабинет)',
                 '5-ая пара (время)'])
            self.add_row_button = QPushButton("Добавить новую строчку")
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 17, self.add_row_button)
            self.add_row_button.clicked.connect(lambda: self.add_row(s))

        if s == 'Учителя':
            self.cursor.execute("SELECT t_name, id, subject FROM teacher")
            data = self.cursor.fetchall()
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(5)
            self.table_widget.setColumnHidden(1, True)
            for row, item in enumerate(data):
                for col, val in enumerate(item):
                    self.table_widget.setItem(row, col, QTableWidgetItem(str(val)))
                self.update_row_button = QPushButton("Обновить")
                self.table_widget.setCellWidget(row, 3, self.update_row_button)
                self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
                self.delete_row_button = QPushButton("Удалить")
                self.table_widget.setCellWidget(row, 4, self.delete_row_button)
                self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))

            self.table_widget.setHorizontalHeaderLabels(['Учитель', 'id', 'Предмет'])

            self.add_row_button = QPushButton("Добавить новую строчку")
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 3, self.add_row_button)
            self.add_row_button.clicked.connect(lambda: self.add_row(s))

        if s == 'Предметы':
            self.cursor.execute("SELECT name, id FROM sub")
            data = self.cursor.fetchall()

            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(4)
            self.table_widget.setColumnHidden(1, True)

            for row, item in enumerate(data):
                for col, val in enumerate(item):
                    self.table_widget.setItem(row, col, QTableWidgetItem(str(val)))
                self.update_row_button = QPushButton("Обновить")
                self.table_widget.setCellWidget(row, 2, self.update_row_button)
                self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
                self.delete_row_button = QPushButton("Удалить")
                self.table_widget.setCellWidget(row, 3, self.delete_row_button)
                self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))

            self.table_widget.setHorizontalHeaderLabels(['Предметы', 'id'])
            self.add_row_button = QPushButton("Добавить новую строчку")
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 2, self.add_row_button)
            self.add_row_button.clicked.connect(lambda: self.add_row(s))

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def render_w1(self):
        s = '1-ая неделя'
        self.table_widget.clear()

        self.cursor.execute(
            "SELECT days.id, s1, k1, t1, s2, k2, t2, s3, k3, t3, s4, k4, t4, s5, k5, t5 FROM days JOIN kabs ON days.id = kabs.id")
        data = self.cursor.fetchall()
        data = data[1:7]
        print(data)
        da = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(19)

        for row, item in enumerate(data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(da[row]))
            for col, val in enumerate(item):
                self.table_widget.setItem(row, col + 1, QTableWidgetItem(str(val)))
            self.update_row_button = QPushButton("Обновить")
            self.table_widget.setCellWidget(row, 17, self.update_row_button)
            self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
            self.delete_row_button = QPushButton("Удалить")
            self.table_widget.setCellWidget(row, 18, self.delete_row_button)
            self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))

        self.table_widget.setHorizontalHeaderLabels(
            ['День недели', 'id', '1-ая пара', '1-ая пара (кабинет)', '1-ая пара (время)', '2-ая пара',
             '2-ая пара (кабинет)', '2-ая пара (время)', '3-ая пара', '3-ая пара (кабинет)', '3-ая пара (время)',
             '4-ая пара', '4-ая пара (кабинет)', '4-ая пара (время)', '5-ая пара', '5-ая пара (кабинет)',
             '5-ая пара (время)'])
        self.add_row_button = QPushButton("Добавить новую строчку")
        self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
        self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 17, self.add_row_button)
        self.add_row_button.clicked.connect(lambda: self.add_row(s))

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def render_w2(self):
        s = '2-ая неделя'
        self.table_widget.clear()

        self.cursor.execute(
            "SELECT days.id, s1, k1, t1, s2, k2, t2, s3, k3, t3, s4, k4, t4, s5, k5, t5 FROM days JOIN kabs ON days.id = kabs.id")
        data = self.cursor.fetchall()
        data = data[7:13]
        da = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(18)
        self.table_widget.setColumnHidden(1, True)
        for row, item in enumerate(data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(da[row]))
            for col, val in enumerate(item):
                self.table_widget.setItem(row, col + 1, QTableWidgetItem(str(val)))
            self.update_row_button = QPushButton("Обновить")
            self.table_widget.setCellWidget(row, 16, self.update_row_button)
            self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
            self.delete_row_button = QPushButton("Удалить")
            self.table_widget.setCellWidget(row, 17, self.delete_row_button)
            self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))
        self.table_widget.setHorizontalHeaderLabels(
            ['День недели', 'id', '1-ая пара', '1-ая пара (кабинет)', '1-ая пара (время)', '2-ая пара',
             '2-ая пара (кабинет)', '2-ая пара (время)', '3-ая пара', '3-ая пара (кабинет)', '3-ая пара (время)',
             '4-ая пара', '4-ая пара (кабинет)', '4-ая пара (время)', '5-ая пара', '5-ая пара (кабинет)',
             '5-ая пара (время)'])
        self.add_row_button = QPushButton("Добавить новую строчку")
        self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
        self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 17, self.add_row_button)
        self.add_row_button.clicked.connect(lambda: self.add_row(s))

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def render_t(self):
        s = 'Учителя'
        print('render')
        self.table_widget.clear()
        self.cursor.execute("SELECT t_name, id, subject FROM teacher")
        data = self.cursor.fetchall()
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(5)
        self.table_widget.setColumnHidden(1, True)
        for row, item in enumerate(data):
            for col, val in enumerate(item):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(val)))
            self.update_row_button = QPushButton("Обновить")
            self.table_widget.setCellWidget(row, 3, self.update_row_button)
            self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
            self.delete_row_button = QPushButton("Удалить")
            self.table_widget.setCellWidget(row, 4, self.delete_row_button)
            self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))
        self.table_widget.setHorizontalHeaderLabels(['Учитель', 'id', 'Предмет'])

        self.add_row_button = QPushButton("Добавить новую строчку")
        self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
        self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 3, self.add_row_button)
        self.add_row_button.clicked.connect(lambda: self.add_row(s))


    def render_s(self):
        s = 'Предметы'
        self.table_widget.clear()

        self.cursor.execute("SELECT name, id FROM sub")
        data = self.cursor.fetchall()

        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(4)
        self.table_widget.setColumnHidden(1, True)

        for row, item in enumerate(data):
            for col, val in enumerate(item):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(val)))
            self.update_row_button = QPushButton("Обновить")
            self.table_widget.setCellWidget(row, 2, self.update_row_button)
            self.update_row_button.clicked.connect(lambda _, r=row: self.update_row(r, s))
            self.delete_row_button = QPushButton("Удалить")
            self.table_widget.setCellWidget(row, 3, self.delete_row_button)
            self.delete_row_button.clicked.connect(lambda _, r=row: self.delete_row(r, s))

        self.table_widget.setHorizontalHeaderLabels(['Предметы', 'id'])
        self.add_row_button = QPushButton("Добавить новую строчку")
        self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
        self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 2, self.add_row_button)
        self.add_row_button.clicked.connect(lambda: self.add_row(s))

    def update_row(self, r, s):
        if s == 'Учителя':
            p1 = self.table_widget.item(r, 0).text()
            id = self.table_widget.item(r, 1).text()
            p2 = self.table_widget.item(r, 2).text()
            self.cursor.execute(f"UPDATE teacher SET t_name = '{p1}', subject ='{p2}' WHERE id = '{id}'")
            self.conn.commit()
        if s == 'Предметы':
            t_sub = self.table_widget.item(r, 0).text()
            id = self.table_widget.item(r, 1).text()
            print(t_sub, r + 1)
            self.cursor.execute(f"UPDATE sub SET name = '{t_sub}' WHERE id = '{id}'")
            self.conn.commit()
        if s == '1-ая неделя':
            id = self.table_widget.item(r, 1).text()
            s1 = self.table_widget.item(r, 2).text()
            k1 = self.table_widget.item(r, 3).text()
            t1 = self.table_widget.item(r, 4).text()
            s2 = self.table_widget.item(r, 5).text()
            k2 = self.table_widget.item(r, 6).text()
            t2 = self.table_widget.item(r, 7).text()
            s3 = self.table_widget.item(r, 8).text()
            k3 = self.table_widget.item(r, 9).text()
            t3 = self.table_widget.item(r, 10).text()
            s4 = self.table_widget.item(r, 11).text()
            k4 = self.table_widget.item(r, 12).text()
            t4 = self.table_widget.item(r, 13).text()
            s5 = self.table_widget.item(r, 14).text()
            k5 = self.table_widget.item(r, 15).text()
            t5 = self.table_widget.item(r, 16).text()

            self.cursor.execute(f"UPDATE days SET s1 = '{s1}', s2 = '{s2}', s3 = '{s3}', s4 = '{s4}', s5 = '{s5}', t1 = '{t1}', t2 = '{t2}', t3 = '{t3}', t4 = '{t4}', t5 = '{t5}' WHERE id = '{id}'")
            self.conn.commit()
            self.cursor.execute(
                f"UPDATE kabs SET k1 = '{k1}', k2 = '{k2}', k3 = '{k3}', k4 = '{k4}', k5 = '{k5}' WHERE id = '{id}'")
            self.conn.commit()
        if s == '2-ая неделя':
            id = self.table_widget.item(r, 1).text()
            s1 = self.table_widget.item(r, 2).text()
            k1 = self.table_widget.item(r, 3).text()
            t1 = self.table_widget.item(r, 4).text()
            s2 = self.table_widget.item(r, 5).text()
            k2 = self.table_widget.item(r, 6).text()
            t2 = self.table_widget.item(r, 7).text()
            s3 = self.table_widget.item(r, 8).text()
            k3 = self.table_widget.item(r, 9).text()
            t3 = self.table_widget.item(r, 10).text()
            s4 = self.table_widget.item(r, 11).text()
            k4 = self.table_widget.item(r, 12).text()
            t4 = self.table_widget.item(r, 13).text()
            s5 = self.table_widget.item(r, 14).text()
            k5 = self.table_widget.item(r, 15).text()
            t5 = self.table_widget.item(r, 16).text()

            self.cursor.execute(
                f"UPDATE days SET s1 = '{s1}', s2 = '{s2}', s3 = '{s3}', s4 = '{s4}', s5 = '{s5}', t1 = '{t1}', t2 = '{t2}', t3 = '{t3}', t4 = '{t4}', t5 = '{t5}' WHERE id = '{id}'")
            self.conn.commit()
            self.cursor.execute(
                f"UPDATE kabs SET k1 = '{k1}', k2 = '{k2}', k3 = '{k3}', k4 = '{k4}', k5 = '{k5}' WHERE id = '{id}'")
            self.conn.commit()

    def delete_row(self, row, s):
        if s == 'Учителя':
            id = self.table_widget.item(row, 1).text()
            self.cursor.execute(f"DELETE from teacher WHERE id = '{id}'")
            print(row)
            self.conn.commit()
            self.render_t()
        if s == 'Предметы':
            id = self.table_widget.item(row, 1).text()
            print(row)
            self.cursor.execute(f"DELETE from sub WHERE id = '{id}'")
            self.conn.commit()
            self.render_s()

    def add_row(self, s):
        if s == 'Учителя':
            p1 = self.table_widget.item(self.table_widget.rowCount() - 1, 0).text()
            p2 = self.table_widget.item(self.table_widget.rowCount() - 1, 2).text()
            self.cursor.execute(f"Insert into teacher (t_name, subject) VALUES ('{p1}','{p2}')")
            self.conn.commit()
            self.render_t()
        if s == 'Предметы':
            p1 = self.table_widget.item(self.table_widget.rowCount() - 1, 0).text()
            self.cursor.execute(f"Insert into sub (name) VALUES ('{p1}')")
            self.conn.commit()
            self.render_s()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="mt_rasp",
                                     user="postgres",
                                     password=" ",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
