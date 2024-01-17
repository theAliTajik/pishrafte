import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QListWidget, QTextEdit, QInputDialog, QMessageBox
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import QRegExp
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        # Keyword format (blue)
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(48, 48, 255))
        keywordPatterns = [
            "\\bFalse\\b", "\\bNone\\b", "\\bTrue\\b", "\\band\\b", "\\bas\\b",
            "\\bassert\\b", "\\bbreak\\b", "\\bclass\\b", "\\bcontinue\\b", "\\bdef\\b",
            "\\bdel\\b", "\\belif\\b", "\\belse\\b", "\\bexcept\\b", "\\bfinally\\b",
            "\\bfor\\b", "\\bfrom\\b", "\\bglobal\\b", "\\bif\\b", "\\bimport\\b",
            "\\bin\\b", "\\bis\\b", "\\blambda\\b", "\\bnonlocal\\b", "\\bnot\\b",
            "\\bor\\b", "\\bpass\\b", "\\braise\\b", "\\breturn\\b", "\\btry\\b",
            "\\bwhile\\b", "\\bwith\\b", "\\byield\\b"
        ]
        self.highlightingRules = [(QRegExp(pattern), keywordFormat) for pattern in keywordPatterns]

        # Class name format (green)
        classFormat = QTextCharFormat()
        classFormat.setForeground(QColor(0, 128, 0))
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"), classFormat))

        # String format (orange)
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(206, 123, 0))
        self.highlightingRules.append((QRegExp("\".*\""), stringFormat))
        self.highlightingRules.append((QRegExp("\'.*\'"), stringFormat))

        # Single line comment format (light grey)
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor(128, 128, 128))
        self.highlightingRules.append((QRegExp("#[^\n]*"), singleLineCommentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)

class Notebook:
    def __init__(self, name):
        self.name = name
        self.notes = {}

    def create_note(self, title, body):
        self.notes[title] = body
        self.save_to_file()

    def delete_note(self, title):
        del self.notes[title]
        self.save_to_file()

    def rename_note(self, old_title, new_title):
        self.notes[new_title] = self.notes.pop(old_title)
        self.save_to_file()

    def edit_note(self, title, new_body):
        self.notes[title] = new_body
        self.save_to_file()

    def list_notes(self):
        return list(self.notes.keys())

    def find_note(self, title):
        return self.notes.get(title, None)

    def save_to_file(self):
        notes_dir = "notes"
        if not os.path.exists(notes_dir):
            os.makedirs(notes_dir)
        with open(os.path.join(notes_dir, f"{self.name}.json"), 'w') as file:
            json.dump(self.notes, file, indent=4)

    @staticmethod
    def load_from_file(name):
        notes_dir = "notes"
        if not os.path.exists(notes_dir):
            os.makedirs(notes_dir)
        try:
            with open(os.path.join(notes_dir, f"{name}.json"), 'r') as file:
                notes = json.load(file)
                notebook = Notebook(name)
                notebook.notes = notes
                return notebook
        except FileNotFoundError:
            logging.warning(f'file: {name}, not found in path: {os.path.join(notes_dir, f"{name}.json")} when trying to load notebook.  returning empty notebook')
            return Notebook(name)

class NotebookGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.notebooks = {}
        self.current_notebook = None
        self.current_note = None
        self.initUI()
        self.load_existing_notebooks()


    def load_existing_notebooks(self):
        notes_dir = 'notes'
        # Load existing notebooks
        for file in os.listdir(notes_dir):
            logging.info(f'found file in notes dir {file}')
            if file.endswith(".json"):
                name = file.replace(".json", "")
                notebook = Notebook.load_from_file(name)
                self.notebook_list.addItem(name)
                self.notebooks[name] = notebook
                logging.info(f'added file: {file} with name: {name}, to notes now notes includes: {self.notebooks}')


    def initUI(self):
        self.setWindowTitle('Notebook GUI')
        main_layout = QHBoxLayout()
        logging.info('init ui')

        # Notebook layout
        notebook_layout = QVBoxLayout()
        self.notebook_list = QListWidget()
        notebook_layout.addWidget(self.notebook_list)

        # Notebook buttons
        self.add_notebook_btn = QPushButton('Add Notebook')
        self.remove_notebook_btn = QPushButton('Remove Notebook')
        self.edit_notebook_btn = QPushButton('Edit Notebook Title')
        notebook_layout.addWidget(self.add_notebook_btn)
        notebook_layout.addWidget(self.remove_notebook_btn)
        notebook_layout.addWidget(self.edit_notebook_btn)
        main_layout.addLayout(notebook_layout)

        self.add_notebook_btn.clicked.connect(self.add_notebook)
        self.remove_notebook_btn.clicked.connect(self.remove_notebook)
        self.edit_notebook_btn.clicked.connect(self.edit_notebook)
        self.notebook_list.itemClicked.connect(self.on_notebook_selected)

        # Note layout
        note_layout = QVBoxLayout()
        self.note_list = QListWidget()
        note_layout.addWidget(self.note_list)

        # Note buttons
        self.add_note_btn = QPushButton('Add Note')
        self.remove_note_btn = QPushButton('Remove Note')
        self.edit_note_btn = QPushButton('Edit Note Title')
        note_layout.addWidget(self.add_note_btn)
        note_layout.addWidget(self.remove_note_btn)
        note_layout.addWidget(self.edit_note_btn)
        main_layout.addLayout(note_layout)

        self.add_note_btn.clicked.connect(self.add_note)
        self.remove_note_btn.clicked.connect(self.remove_note)
        self.edit_note_btn.clicked.connect(self.edit_note)

        # Note body text editor
        body_layout = QVBoxLayout()
        self.note_body = QTextEdit()
        self.pythonHighlighter = PythonSyntaxHighlighter(self.note_body.document())
        body_layout.addWidget(self.note_body)

        # Save and Execute buttons
        self.save_note_btn = QPushButton("Save Note")
        self.execute_code_btn = QPushButton('Execute Code')
        body_layout.addWidget(self.save_note_btn)
        body_layout.addWidget(self.execute_code_btn)
        main_layout.addLayout(body_layout)

        self.save_note_btn.clicked.connect(self.save_note)
        self.execute_code_btn.clicked.connect(self.execute_code)
        self.note_list.itemClicked.connect(self.on_note_selected)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set the window size
        self.setGeometry(100, 100, 900, 600)

    def add_notebook(self):
        name, ok = QInputDialog.getText(self, 'Add Notebook', 'Enter notebook name:')
        if ok and name:
            notebook = Notebook(name)
            self.notebook_list.addItem(name)
            self.notebooks[name] = notebook
            notebook.save_to_file()

    def on_notebook_selected(self, item):
        notebook_name = item.text()
        notebook = self.notebooks.get(notebook_name)
        if notebook:
            logging.info(f'the selected notebook is {notebook_name}, and does exist')
            self.note_body.clear()
            self.note_list.clear()
            logging.info(f'the titles in note book are: {notebook.list_notes()}')
            for title in notebook.list_notes():
                self.note_list.addItem(title)
            self.current_notebook = notebook

    def add_note(self):
        if not self.current_notebook:
            QMessageBox.information(self, "No Notebook Selected", "Please select a notebook first")
            return
        name, ok = QInputDialog.getText(self, 'Add Note', 'Enter note name:')
        if ok and name:
            self.note_list.addItem(name)
            self.current_notebook.create_note(name, "")

    def on_note_selected(self, item):
        note_name = item.text()
        if note_name:
            self.note_body.clear()
            self.note_body.setText(self.current_notebook.find_note(note_name))
            self.current_note = note_name

    def save_note(self):
        if self.current_notebook and self.current_note:
            self.current_notebook.edit_note(self.current_note, self.note_body.toPlainText())

    def execute_code(self):
        if self.current_note:
            code = self.note_body.toPlainText()
            try:
                exec(code)
            except Exception as e:
                QMessageBox.critical(self, "Execution Error", f"An error occurred: {e}")

    def remove_notebook(self):
        notebook_name = self.notebook_list.currentItem()
        if notebook_name:
            notebook_name = notebook_name.text()
            del self.notebooks[notebook_name]
            self.notebook_list.takeItem(self.notebook_list.currentRow())
            # Optionally, also delete the notebook's file
            try:
                os.remove(os.path.join("notes", f"{notebook_name}.json"))
            except OSError:
                pass

    def edit_notebook(self):
        notebook_name = self.notebook_list.currentItem()
        if notebook_name:
            notebook_name = notebook_name.text()
            new_name, ok = QInputDialog.getText(self, 'Edit Notebook', 'Enter new notebook name:')
            if ok and new_name:
                notebook = self.notebooks.pop(notebook_name)
                notebook.name = new_name
                self.notebooks[new_name] = notebook
                self.notebook_list.currentItem().setText(new_name)
                # Save the notebook with the new name and delete the old file
                notebook.save_to_file()
                os.remove(os.path.join("notes", f"{notebook_name}.json"))

    def remove_note(self):
        note_name = self.note_list.currentItem()
        if note_name and self.current_notebook:
            note_name = note_name.text()
            self.current_notebook.delete_note(note_name)
            self.note_list.takeItem(self.note_list.currentRow())

    def edit_note(self):
        note_name = self.note_list.currentItem()
        if note_name and self.current_notebook:
            note_name = note_name.text()
            new_name, ok = QInputDialog.getText(self, 'Edit Note', 'Enter new note name:')
            if ok and new_name:
                self.current_notebook.rename_note(note_name, new_name)
                self.note_list.currentItem().setText(new_name)
                if self.current_note == note_name:
                    self.current_note = new_name

def main():
    app = QApplication(sys.argv)
    ex = NotebookGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
