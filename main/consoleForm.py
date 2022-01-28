import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton

from side.consoleUI import Ui_Form


class console(QWidget, Ui_Form):
    # allow it to receive any number of arguments
    def __init__(self, room_start_x, room_start_y):
        super().__init__()
        self.setupUi(self)
        self.x = room_start_x
        self.y = room_start_y
        self.isdebug = False
        self.room_change = False
        self.setWindowTitle("Console")
        self.consoleEdit.setFocus()
        self.big_map = False
        self.pushButton.clicked.connect(self.command_console)
        self.text = "debug is off, map is mini"

    def command_console(self):
        command = self.consoleEdit.text().split()
        wrongcommand = "\nWrong command\ntry: command /help"
        try:
            if command[0] == "/help":
                text = "\ncommands:\n/help (show avalible commands)\n/map (change map mode)\n"\
                    + "/debug (change debug mode)\n/tp room 'x' 'y' (change player room. work only if debug is on)"
                self.text += text
            elif command[0] == "/tp":
                if command[1] == "room":
                    self.x = command[2]
                    self.y = command[3]
                    self.room_change = True
                else:
                    self.text += wrongcommand
            elif command[0] == "/map":
                if self.big_map:
                    self.big_map = False
                else:
                    self.big_map = True
                self.text = f"debug is {self.isdebug}, big map is {self.big_map}"
            elif command[0] == "/debug":
                if self.isdebug:
                    self.isdebug = False
                else:
                    self.isdebug = True
                self.text = f"debug is {self.isdebug}, big map is {self.big_map}"
            else:
                self.text += wrongcommand
        except IndexError:
            self.text += wrongcommand
        self.textEdit.setText(self.text)

    @property
    def room(self):
        return self.x, self.y

    @property
    def change_room(self):
        return self.room_change

    @change_room.setter
    def change_room(self, other):
        self.room_change = other

    @room.setter
    def room(self, other):
        self.x, self.y = other

    @property
    def debug(self):
        return self.isdebug

    @property
    def map_type(self):
        return self.big_map


if __name__ == "__main__":
    app = QApplication(sys.argv)
    self = QMainWindow()
    ui = console()
    ui.show()
    sys.exit(app.exec_())
