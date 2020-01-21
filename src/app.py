from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QMessageBox \
    , QRadioButton, QCheckBox, QLineEdit
from PyQt5 import QtCore
from src.logic import generate_output

from logging import getLogger

logger = getLogger(__name__)

qa_dict = {
    "Wybierz typ sieci": [
        "Sieć bezprzewodowa",
        "Sieć przewodowa"
    ],
    "Wybierz fizyczną topologię sieci": [  # pytania gdy sieć przewodowa
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
    "Wybierz ilość okablowania sieci": [
        "amount"
    ],
    "Wybierz długość wybranego okablowania": [
        "length"
    ],
    "Wybierz topologię sieci bezprzewodowej": [  # pytania gdy sieć bezprzewodowa
        "Topologia gwiazdy",
        "Topologia kraty"
    ],
    "Wybierz tryb sieci bezprzewodowej": [
        "Tryb ad-hoc",
        "Tryb infrastruktury"
    ],
    "Wybierz ilość okablowania RJ45": [
        "amount"
    ],
    "Wybierz długość wybranego uprzednio okablowania": [
        "length"
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
        "Router wielowarstwowy (switch)",
        "Router jednowarstwowy (standardowy)"
    ],
    "Wybierz typy serwerów jakie będą podłączone do sieci": [
        "Serwer plików",
        "Serwer firewall",
        "Serwer poczty",
        "Serwer www",
        "Serwer DNS"
    ],
    "Czy konsola do zarządzania serwerami": [
        "Tak",
        "Nie"
    ],
    "Wybierz system operacyjny obsługujący serwery": [
        "Fedora",
        "Ubuntu Server",
        "Arch Linux",
        "Windows Server",
        "RedHat Linux",
        "Solaris"
    ]
    # TODO think of another questions
}

dict_of_answers = {}

assumptions_dict = {

    "Światłowód": {"PATCHCORD ŚWIATŁOWODOWY SM 2M SIMPLEX 9/125, SC/UPC-SC/UPC 3MM": "19.99",
                   "PATCHCORD ŚWIATŁOWODOWY SM 3M SIMPLEX 9/125, SC/APC-SC/APC 3MM ": "12.99",
                   "PATCHCORD ŚWIATŁOWODOWY SM 5M DUPLEX 9/125, LC/UPC-LC/UPC 3.0MM ": "19.99",
                   "PATCHCORD ŚWIATŁOWODOWY SM 1M DUPLEX 9/125, SC/APC-LC/UPC 3MM ": "13.99"},

    "Skrętka nieekranowa (UTP)": {"PRZEWÓD TELEINFORMATYCZNY SIECIOWY UTP 4x2x0,5mm2 cat. 5e TI0006 BITNER": "0.72",
                                  "PRZEWÓD TELEINFORMATYCZNY SIECIOWY UTP 4x2x0,5mm2 cat. 6 TI0044 BITNER": "1.08",
                                  "PRZEWÓD TELEINFORMATYCZNY SIECIOWY UTPf ZEWNĘTRZNY ZIEMNY żelowany 4x2x0,5mm2 cat. "
                                  "5e TI0012 ": "1.29"},
    "Skrętka ekranowa (STP)": {
        "PRZEWÓD TELEINFORMATYCZNY SIECIOWY EKRANOWANY F/UTP 4x2x0,5mm2 cat. 5e TI0007 BITNER": "0.99"},
    "Skrętka foliowana (FTP)": {"PRZEWÓD OGNIOODPORNY NHXH-J FE180/E30 3x1,5 0,6/1 kV BITNER": "11.53"},
    "Skrętka hybrydowa": {"PRZEWÓD KONCENTRYCZNY BiTSAT 757 BIAŁY BITNER": "1.09",
                          "PRZEWÓD KONCENTRYCZNY BiTSAT 757 CZARNY BITNER": "1.14"},

    "Router wielowarstwowy (switch)": {"Switch EX16905 ( 5x10/100/1000TBASE-X )": "257.00",
                                       "Switch EX16908 ( 8x10/100/1000TBASE-X )": "288.00",
                                       "Switch EX16914-3 ( 4x10/100/1000BASE-TX + 1 x 1000SX-550m SC )": "641.00",
                                       "Switch EX16914-5 ( 4x10/100/1000BASE-TX + 1 x 1000SX-550m ST )": "641.00"},
    "Router jednowarstwowy (standardowy)": {"TP‑Link Archer C6 (1200Mb/s a/b/g/n/ac) DualBand": "149.00",
                                            "Xiaomi Mi Router 4A (1200Mb/s a/b/g/n/ac) DualBand": "119.00",
                                            "Razer Portal Gaming (2400Mb/s a/b/g/n/ac, 2xUSB)": "399.00",
                                            "TP‑Link Archer C7 (1750Mb/s a/b/g/n/ac) USB DualBand": "265.00",
                                            "TP‑Link Archer C1200 (1200Mb/s a/b/g/n/ac) USB DualBand": "199.00"},

    "Serwer plików": {"Serwer NAS SYNOLOGY DiskStation DS218j ": "779",
                      "Serwer NAS SYNOLOGY DiskStation DS119j ": "479",
                      "Dysk sieciowy WD My Cloud Home 3TB WDBVXC0030HWT-EESN ": "899",
                      "Serwer plików QNAP TS-231P ": "799"},
    "Serwer firewall": {"LES v3": "699",
                        "LES network+": "899",
                        "RI1101H": "1099",
                        "RI1102H": "999"},
    "Serwer poczty": {"Serwer NAS QNAP TS-451+-4G ": "2549",
                      "Serwer NAS QNAP TS-253Be-2G ": "1749",
                      "Serwer NAS QNAP TS-473-8G ": "3599",
                      "Serwer NAS QNAP TVS-473e-8G ": "4699"},
    "Serwer www": {"HP 460-a200nw J3060/4GB": "1499",
                   "HP 460-a203nw J3710/4GB/1TB": "1499",
                   "ACER Aspire C22-820 DQ.BCMEP.005 J5005/4GB/128GB": "1699",
                   "Aspire C22-820 DQ.BCKEP.001 J4005/4GB/1TB/INT": "1599"},
    "Serwer DNS": {"LES v3": "699",
                   "LES network+": "899",
                   "RI1101H": "1099",
                   "RI1102H": "999"},

    "Fedora": "0",
    "Ubuntu Server": "0",
    "Arch Linux": "0",
    "Windows Server": "499.00",
    "RedHat Linux": "199.00",
    "Solaris": "0"
}


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
        self.setWindowTitle("Tryb projektowania")
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
        self.output_win = None
        self.main_grid = QGridLayout()
        self.wid = QWidget()
        self.answers_wid = QWidget()
        self.answers_grid = QGridLayout()
        self.question_index = 0
        self.question = list(qa_dict.keys())[self.question_index]
        self.question_label = QLabel(self.question)
        self.prev = QPushButton("Poprzednie pytanie")
        self.next = QPushButton("Następne pytanie")
        self.generate = QPushButton("Generuj projekt")
        self.next.clicked.connect(self.show_next_question)
        self.prev.clicked.connect(self.show_next_question)
        self.generate.clicked.connect(self.show_project)
        self.initialize()

    def closeEvent(self, event):
        result = QMessageBox.question(self,
                                      "Potwierdż wyjście...",
                                      "Czy na pewno chcesz wyjść z trybu projektowania ?",
                                      QMessageBox.Yes | QMessageBox.No)
        event.ignore()
        if result == QMessageBox.Yes:
            event.accept()

    def initialize(self):  # window initialization with first question
        self.resize(400, 200)
        self.setWindowTitle("Projekt sieci")
        self.setCentralWidget(self.wid)
        radio_1 = QRadioButton("Sieć bezprzewodowa")
        radio_2 = QRadioButton("Sieć przewodowa")
        radio_1.clicked.connect(self.handle_qa)
        radio_2.clicked.connect(self.handle_qa)
        self.answers_grid.addWidget(radio_1, 0, 0)
        self.answers_grid.addWidget(radio_2, 0, 1)
        self.answers_wid.setLayout(self.answers_grid)
        self.main_grid.addWidget(self.question_label, 0, 0, 2, 0)
        self.main_grid.addWidget(self.answers_wid, 1, 0, 2, 0)
        self.main_grid.addWidget(self.prev, 2, 0)
        self.main_grid.addWidget(self.next, 2, 2)
        self.main_grid.addWidget(self.generate, 2, 2)
        self.prev.setVisible(False)
        self.generate.setVisible(False)
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
            self.question = list(qa_dict.keys())[self.question_index]
            if self.question_index + 1 >= len(list(qa_dict.keys())):
                self.next.setVisible(False)
                self.generate.setVisible(True)

        if sender.text() == "Poprzednie pytanie":
            self.question_index -= 1
            self.question = list(qa_dict.keys())[self.question_index]
            self.generate.setVisible(False)
            if self.question_index - 1 < 0:
                self.prev.setVisible(False)

        self.handle_answers()
        self.handle_questions()
        print("next question printed, %d", self.question_index)

    def handle_questions(self):
        if self.question == "Wybierz typ sieci":
            print("Wybierz typ sieci")
            if self.radio_buttons is not None:
                self.radio_buttons[0].clicked.connect(lambda: self.change_index(5))
        if self.question == "Wybierz rodzaj okablowania sieci":
            print("Wybierz rodzaj okablowania sieci")
            if self.radio_buttons is not None:
                self.radio_buttons[1].clicked.connect(lambda: self.change_index(1))
        else:
            print("Radios empty")

    def handle_answers(self):
        answer_index = 0
        self.question_label.setText(self.question)  # set layout items
        for item in qa_dict[str(self.question)]:
            if self.question == "Wybierz typy serwerów jakie będą podłączone do sieci":
                dict_of_answers.update({self.question: list()})
                checkbox = QCheckBox(item)
                self.checkboxes.append(checkbox)
                self.checkboxes.append(checkbox)
                self.answers_grid.addWidget(checkbox, 0, answer_index)
                checkbox.stateChanged.connect(self.handle_qa)
            elif self.question == "Wybierz ilość okablowania RJ45" \
                    or self.question == "Wybierz ilość okablowania sieci" \
                    or self.question == "Wybierz długość wybranego okablowania" \
                    or self.question == "Wybierz długość wybranego uprzednio okablowania":
                q_line = QLineEdit()
                q_line.setMaximumSize(40, 20)
                q_line.textChanged.connect(self.handle_qa)
                self.answers_grid.addWidget(q_line, 1, answer_index)
            else:
                radio = QRadioButton(item)
                self.radio_buttons.append(radio)
                self.answers_grid.addWidget(radio, 0, answer_index)
                radio.clicked.connect(self.handle_qa)
            answer_index += 1

    def handle_qa(self):
        if isinstance(self.sender(), QLineEdit):
            if self.sender().text() != "":
                dict_of_answers.update({self.question: self.sender().text()})
                print(self.sender().text())
        elif isinstance(self.sender(), QRadioButton):
            dict_of_answers.update({self.question: self.sender().text()})
            print(self.sender().text())
        elif isinstance(self.sender(), QCheckBox):
            if self.sender().isChecked():
                if len(dict_of_answers[self.question]) != 0:
                    if self.sender().text() not in dict_of_answers[self.question]:
                        dict_of_answers[self.question].append(self.sender().text())
                else:
                    dict_of_answers[self.question].append(self.sender().text())
                    # dict_of_answers.update({self.question: self.sender().text()})
                print(self.sender().text())
            if not self.sender().isChecked():
                print("odklikuje")
        print(dict_of_answers)

    @QtCore.pyqtSlot()
    def show_qline_edit(self, index):
        return

    def change_index(self, index):
        if self.sender().isChecked():
            self.question_index += index

    def show_project(self):
        self.output_win = OutputWindow(self)
        self.showMinimized()
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


class OutputWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_grid = QGridLayout()
        self.main_wid = QWidget()
        self.initialize()

    def initialize(self):
        layout_index = 0
        self.resize(500, 300)
        self.setWindowTitle("Tryb projektowania")
        out_list = generate_output(assumptions_dict, dict_of_answers)
        print(out_list)
        type_ = QLabel("Typ urządzenia:")
        device = QLabel("Urządzenia:")
        price = QLabel("Ceny produktów:")
        self.main_grid.addWidget(type_, 0, layout_index)
        self.main_grid.addWidget(device, 1, layout_index)
        self.main_grid.addWidget(price, 2, layout_index)
        layout_index+=1
        for item in out_list:
            type_ = QLabel(item[0])
            device = QLabel(item[1])
            price = QLabel(item[2])
            print(item[0])
            print(item[1])
            print(item[2])
            self.main_grid.addWidget(type_, 0, layout_index)
            self.main_grid.addWidget(device, 1, layout_index)
            self.main_grid.addWidget(price, 2, layout_index)
            layout_index += 1

        for key in dict_of_answers:

            if key == "Wybierz typ sieci":
                self.main_grid.addWidget(QLabel("Typ sieci: " + dict_of_answers[key]), 3, 1)
            if key == "Wybierz fizyczną topologię sieci":
                self.main_grid.addWidget(QLabel("Topologia fizyczna sieci: " + dict_of_answers[key]), 4, 1)
            if key == "Wybierz ilość okablowania sieci":
                self.main_grid.addWidget(QLabel("Ilość potrzebnych kabli: " + dict_of_answers[key]), 3, 0)
            if key == "Wybierz długość wybranego okablowania":
                self.main_grid.addWidget(QLabel("Długość potrzebnych kabli: " + dict_of_answers[key]), 4, 0)
            if key == "Wybierz topologię sieci bezprzewodowej":
                self.main_grid.addWidget(QLabel("Topologia sieci: " + dict_of_answers[key]), 3, 0)
            if key == "Wybierz tryb sieci bezprzewodowej":
                self.main_grid.addWidget(QLabel("Tryb sieci bezprzewodowej: " + dict_of_answers[key]), 4, 0)
            if key == "Wybierz logiczną topologię sieci":
                self.main_grid.addWidget(QLabel("Logiczna topologia sieci: " + dict_of_answers[key]), 4, 1)
            if key == "Wybierz sposób przydzielania adresów IP w sieci":
                self.main_grid.addWidget(QLabel("Sposób przydzielania adresów IP: " + dict_of_answers[key]), 5, 1)

        self.setCentralWidget(self.main_wid)
        self.main_wid.setLayout(self.main_grid)
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())
