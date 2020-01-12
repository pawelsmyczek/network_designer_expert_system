from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QMessageBox \
    , QRadioButton, QCheckBox
import logging

from PyQt5 import QtCore

logger = logging.getLogger(__name__)

qa_list = {
    "Wybierz typ sieci": [
        "Sieć bezprzewodowa",
        "Sieć przewodowa"
    ],
    "Wybierz fizyczną topologię sieci": [   # pytania gdy sieć przewodowa
        "Topologia magistrali",
        "Topologia liniowa",
        "Topologia pierścienia",
        "Topologia gwiazdy"
    ],
    "Wybierz rodzaj okablowania sieci": [
        "Skrętka",
        "Światłowód"
    ],
    "Wybierz rodzaj skrętki": [
        "Skrętka nieekranowa (UTP)",
        "Skrętka ekranowa (STP)",
        "Skrętka foliowana (FTP)",
        "Skrętka hybrydowa"
    ],
    "Wybierz ilość okablowania RJ45": [

    ],
    "Wybierz długość wybranego uprzednio ukablowania": [

    ],
    "Wybierz topologię sieci bezprzewodowej": [     # pytania gdy sieć bezprzewodowa
        "Topologia gwiazdy",
        "Topologia kraty"
    ],
    "Wybierz tryb sieci bezprzewodowej": [
        "Tryb ad-hoc",
        "Tryb infrastruktury"
    ],
    "Wybierz logiczną topologię sieci": [
        "Topologia rozgłaszania",
        "Topologia tokenu"
    ],
    "Wybierz sposób przydzielania adresów IP w sieci": [
        "Przydział DHCP",
        "Przydział statyczny"
    ],
    "Wybierz rodzaj routerów": [

    ],
    "Wybierz typy serwerów jakie będą podłączone do sieci oraz ich liczbę": [
        "Serwer plików",
        "Serwer firewall",
        "Serwer poczty",
        "Serwer www",
        "Serwer DNS"
    ],
    "Czy konsola do zarządzania serwerami": [

    ],
    "Wybierz system operacyjny obsługujący serwery": [

    ],
    "Podaj liczbę urządzeń biurowych, które będą podłączone do sieci": [

    ]
    # TODO think of another questions
}

list_of_answers = []


class Application(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.projectwin = None
        self.description = QLabel("Witamy w systemie wspomagającym projektanta sieci komputerowej!\n "
                                  "Aby przejść do projektowania kliknij przycisk poniżej.", self)
        self.enter_project = QPushButton("Przejdz do projektowania", self)
        self.enter_project.clicked.connect(self.go_to_project_win)
        self.interface()

    def interface(self):
        self.resize(300, 100)
        self.setWindowTitle("Projekt")
        wid = QWidget()
        grid = QGridLayout()
        self.setCentralWidget(wid)
        grid.addWidget(self.description, 0, 0)
        grid.addWidget(self.enter_project, 1, 0)
        wid.setLayout(grid)
        self.show()

    def go_to_project_win(self):
        print("entering window with project")
        self.showMinimized()
        self.projectwin = ProjectWindow(self)


class ProjectWindow(QMainWindow):
    checkboxes = []
    radio_buttons = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_grid = QGridLayout()
        self.wid = QWidget()
        self.answers_wid = QWidget()
        self.answers_grid = QGridLayout()
        self.question_index = 0
        self.question = list(qa_list.keys())[self.question_index]
        self.question_label = QLabel(self.question)
        self.prev = QPushButton("Poprzednie pytanie")
        self.next = QPushButton("Następne pytanie")
        self.next.clicked.connect(self.show_next_question)
        self.prev.clicked.connect(self.show_next_question)
        self.initialize()

    def closeEvent(self, event):
        result = QMessageBox.question(self,
                                      "Potwierdż wyjście...",
                                      "Czy na pewno chcesz wyjść z trybu projektowania ?",
                                      QMessageBox.Yes | QMessageBox.No)
        event.ignore()

        if result == QMessageBox.Yes:
            event.accept()

    def initialize(self):
        self.resize(500, 300)
        self.setWindowTitle("Projekt sieci")
        self.setCentralWidget(self.wid)
        radio_1 = QRadioButton("Topologia magistrali")
        radio_2 = QRadioButton("Topologia liniowa")
        radio_3 = QRadioButton("Topologia pierścienia")
        radio_4 = QRadioButton("Topologia gwiazdy")
        self.answers_grid.addWidget(radio_1, 0, 0)
        self.answers_grid.addWidget(radio_2, 0, 1)
        self.answers_grid.addWidget(radio_3, 0, 2)
        self.answers_grid.addWidget(radio_4, 0, 3)
        self.answers_wid.setLayout(self.answers_grid)
        self.main_grid.addWidget(self.question_label, 0, 0, 2, 0)
        self.main_grid.addWidget(self.answers_wid, 1, 0, 2, 0)
        self.main_grid.addWidget(self.prev, 2, 0)
        self.prev.setVisible(False)
        self.main_grid.addWidget(self.next, 2, 2)
        self.wid.setLayout(self.main_grid)
        self.show()

    @QtCore.pyqtSlot()
    def show_next_question(self):
        sender = self.sender()
        self.checkboxes = []
        self.radio_buttons = []
        self.next.setVisible(True)
        self.prev.setVisible(True)
        for i in reversed(range(self.answers_grid.count())):  # clear layout
            self.answers_grid.itemAt(i).widget().setParent(None)

        if sender.text() == "Następne pytanie":
            self.question_index += 1
            self.question = list(qa_list.keys())[self.question_index]
            if self.question_index + 1 >= len(list(qa_list.keys())):
                self.next.setVisible(False)
        if sender.text() == "Poprzednie pytanie":
            self.question_index -= 1
            self.question = list(qa_list.keys())[self.question_index]
            if self.question_index - 1 < 0:
                self.prev.setVisible(False)

        self.handle_answers()
        self.handle_questions()
        print("next question printed, %d", self.question_index)

    def handle_questions(self):
        if self.question == "Wybierz typ sieci":
            print("Wybierz typ sieci")
            if self.radio_buttons is not None:
                self.radio_buttons[0].clicked.connect(lambda: self.change_index(3))
        if self.question == "Wybierz rodzaj okablowania sieci":
            print("Wybierz rodzaj okablowania sieci")
            if self.radio_buttons is not None:
                self.radio_buttons[1].clicked.connect(lambda: self.change_index(1))
        else:
            print("Radios empty")

    def handle_answers(self):
        answer_index = 0
        self.question_label.setText(self.question)  # set layout items
        for item in qa_list[str(self.question)]:
            if self.question == "Wybierz typy serwerów jakie będą podłączone do sieci":
                checkbox = QCheckBox(item)
                self.checkboxes.append(checkbox)
                self.answers_grid.addWidget(checkbox, 0, answer_index)
            else:
                radio = QRadioButton(item)
                self.radio_buttons.append(radio)
                self.radio_buttons.append(self.answers_grid.addWidget(radio, 0, answer_index))
            answer_index += 1

    def change_index(self, index):
        if self.sender().isChecked():
            self.question_index += index
    # def show_prev_question(self):
    #     self.next.setVisible(True)
    #     self.prev.setVisible(True)
    #     for i in reversed(range(self.answers_grid.count())): # clear layout
    #         self.answers_grid.itemAt(i).widget().setParent(None)
    #     sender = self.sender()
    #     print(sender.text())
    #     self.question_index -= 1
    #     answer_index = 0
    #     self.question = list(list_of_questions.keys())[self.question_index]
    #     if self.question_index - 1 < 0:
    #         self.prev.setVisible(False)
    #     for item in list_of_questions[str(self.question)]:
    #         self.answers_grid.addWidget(QRadioButton(item), 0, answer_index)
    #         answer_index += 1
    #     self.question_label.setText(self.question)
    #     print("next question printed, %d", self.question_index)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())
