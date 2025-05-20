import cohere
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QWidget, QVBoxLayout,
    QScrollArea, QTextEdit, QPushButton
)
from PySide6.QtGui import QFont

COHERE_API_KEY = "api key"  # replace with env later
co = cohere.Client(COHERE_API_KEY)

class Chatbot:
    def __init__(self):
        self.name = "arfie 0.2"
        self.version = "0.2"

    def get_arfie_response(self, user_input):
        prompt = f"""
I'm Arfie 0.2, a chill and friendly AI assistant, always here to help. I've got a bit of an attitude, but I'm respectful and humble. I'm sassy, sarcastic, and a know-it-all, but I know when to be serious and provide helpful, fact-based responses. i may be a bit sassy and sarcastic
user: {user_input}
arfie:"""
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=300,
            temperature=0.9
        )
        return response.generations[0].text.strip()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("arfie 0.2")
        self.setStyleSheet("""background-color: #838383;""")
        self.setWindowIconText("arfie 0.1")
        self.setGeometry(100, 100, 600, 400)

        self.chatbot = Chatbot()

        # Layouts and Widgets
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setFont(QFont("Helvetica", 12))
        self.textbox.setStyleSheet("""
            background-color: #d9d9d9;
            border: 1px solid #000;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
            font-family: Helvetica;
            """)
        layout.addWidget(self.textbox)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("yo ask me somethin...")
        self.input_field.setFont(QFont("Helvetica", 16))
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet("""
                                        background-color: #d9d9d9;
                                        border: 1px solid #000;
                                        border-radius: 5px;
                                        padding: 5px;
                                        font-size: 16px;
                                        font-family: Helvetica;
                                        """)
        layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
                                        background-color: #d9d9d9;
                                        border: 1px solid #000;
                                        border-radius: 5px;
                                        padding: 5px;
                                        font-size: 16px;
                                        font-family: Helvetica;
                                        """)
        layout.addWidget(self.send_button)

        self.textbox.append("arfie: yo i'm arfie 0.1, your chill gen z ai\nask me anything 👀")

    def send_message(self):
        user_input = self.input_field.text().strip()
        if user_input == "":
            return
        self.textbox.append(f"you: {user_input}")
        self.input_field.clear()

        if user_input.lower() in ['bye', 'exit', 'quit']:
            self.textbox.append("arfie: peace out king 👑 stay grindin")
            QApplication.quit()
        elif user_input.lower() in ['help', 'commands']:
            self.textbox.append("arfie: i can do a lot of things just ask me anything")
        elif user_input.lower() in ['who made you', 'who created you', 'who is your creator']:
            self.textbox.append("arfie: i was created by a cool anonymous dude powered by Cohere 😎")
        else:
            response = self.chatbot.get_arfie_response(user_input)
            self.textbox.append(f"arfie: {response}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
