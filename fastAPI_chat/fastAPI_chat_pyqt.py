import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit
import websockets
import threading

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WebSocket Chat")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.lineEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.send_message)

        layout.addWidget(self.textEdit)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.sendButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.websocket_thread = threading.Thread(target=self.start_websocket)
        self.websocket_thread.start()

    async def connect_websocket(self):
        async with websockets.connect("ws://localhost:8000/ws") as websocket:
            self.websocket = websocket
            while True:
                message = await websocket.recv()
                self.textEdit.append(message)

    def start_websocket(self):
        asyncio.run(self.connect_websocket())

    def send_message(self):
        message = self.lineEdit.text()
        if message:
            asyncio.run(self.websocket.send(message))
            self.lineEdit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())
