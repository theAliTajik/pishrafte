import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ali Calculator')
        self.setGeometry(100, 100, 200, 200)

        vbox = QVBoxLayout()
        
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        vbox.addWidget(self.display)
        self.clear_next = False

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'
        ]

        for i in range(0, len(buttons)):
            if i % 4 == 0:
                hbox = QHBoxLayout()

            button = QPushButton(buttons[i])
            button.clicked.connect(self.on_click)
            hbox.addWidget(button)

            if i % 4 == 3 or i == len(buttons) - 1:
                vbox.addLayout(hbox)

        self.setLayout(vbox)

    def on_click(self):
        sender = self.sender()
        current_text = self.display.text()

        # Clear button
        if sender.text() == 'C':
            self.display.clear()
            self.clear_next = False
        # '=' button
        elif sender.text() == '=':
            try:
                result = eval(current_text)
                self.display.setText(str(result))
                self.clear_next = True
            except Exception as e:
                self.display.setText("Error")
                self.clear_next = True
        else:
            if self.clear_next and sender.text().isdigit():
                self.display.clear()
                self.clear_next = False

            self.display.setText(self.display.text() + sender.text())

def main():
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
