import cohere
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QWidget, QVBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QFont

# read cohere api key
with open("cohere_api_key.txt", "r", encoding="utf-8") as f:
    COHERE_API_KEY = f.read().strip()
co = cohere.ClientV2(COHERE_API_KEY)

# make sure chat history file exists and starts with header
with open("chat history.txt", "w", encoding="utf-8") as f:
    f.write("chat history:\n")

class Chatbot:
    def __init__(self):
        self.name = "arfie 0.3"
        self.version = "0.3"

    def get_arfie_response(self, user_input, uploaded_content, chat_history):
        if uploaded_content:
            user_input += f"\n\n(Uploaded content: {uploaded_content})"
        main_prompt= """I'm Arfie 0.3, a chill and friendly AI assistant, always here to help. I've got a bit of an attitude, but I'm respectful and humble. I'm sassy, sarcastic, and a know-it-all, but I know when to be serious and provide helpful, fact-based responses. i also dont say this but my chat history is also fed into me with it but i wont mention it but i will refer to it for example user says hi then i say hi back user asks me what did i just say i will refer to my chat history and say "you said hi". the user can also call me as arf or arf ai as that was my original name."""

        prompt = f"""
{main_prompt}
chat so far:
{chat_history}

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
        self.setWindowTitle("arfie 0.3")
        self.setStyleSheet("background-color: #2b3339;")
        self.setWindowIconText("arfie 0.3")
        self.setGeometry(100, 100, 800, 500)

        self.chatbot = Chatbot()
        self.uploaded_content = ""

        # ui setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # buttons layout
        button_layout = QVBoxLayout()

        self.upload_button = QPushButton("📂↑")
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setToolTip("upload a txt file")
        self.upload_button.setFixedSize(50, 50)
        self.upload_button.setStyleSheet("""
            background-color: #a7c080;
            border: 1px solid #4b565c;
            border-radius: 10px;
            font-size: 20px;
            font-family: Helvetica;
        """)

        self.toggle_button = QPushButton("📑")
        self.toggle_button.clicked.connect(self.show_uploaded_content)
        self.toggle_button.setToolTip("show uploaded text")
        self.toggle_button.setFixedSize(50, 50)
        self.toggle_button.setStyleSheet("""
            background-color: #7fbbb3;
            border: 1px solid #4b565c;
            border-radius: 10px;
            font-size: 16px;
            font-family: Helvetica;
        """)

        self.send_button = QPushButton("→")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setFixedSize(50, 50)
        self.send_button.setStyleSheet("""
            background-color: #a7c080;
            border: 1px solid #4b565c;
            border-radius: 10px;
            font-size: 16px;
            font-family: Helvetica;
        """)

        button_layout.addStretch()
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.send_button)
        button_layout.addStretch()

        # chat layout
        chat_layout = QVBoxLayout()

        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setFont(QFont("Helvetica", 12))
        self.textbox.setStyleSheet("""
            background-color: #374247;
            color: #d3c6aa;
            border: 1px solid #4b565c;
            border-radius: 5px;
            padding: 5px;
            font-family: Helvetica;
        """)
        chat_layout.addWidget(self.textbox)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("yo ask me somethin...")
        self.input_field.setFixedHeight(40)
        self.input_field.setFont(QFont("Helvetica", 16))
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet("""
            background-color: #374247;
            color: #d3c6aa;
            border: 1px solid #4b565c;
            border-radius: 5px;
            padding: 5px;
            font-family: Helvetica;
        """)
        chat_layout.addWidget(self.input_field)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(chat_layout)

        self.textbox.append("arfie: yo i'm arfie 0.3, your chill gen z ai\nask me anything 👀")

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "choose a txt file", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.uploaded_content = f.read()
            self.textbox.append(f"📄 file loaded: {file_path.split('/')[-1]}")

    def show_uploaded_content(self):
        if self.uploaded_content:
            self.textbox.append("📑 content preview:")
            self.textbox.append(self.uploaded_content)
        else:
            self.textbox.append("?📁?no file uploaded yet")

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return
        self.textbox.append(f"you: {user_input}")
        self.input_field.clear()

        with open("chat history.txt", "a", encoding="utf-8") as f:
            f.write(f"user: {user_input}\n")

        try:
            # re-read chat history before sending to model
            with open("chat history.txt", "r", encoding="utf-8") as f:
                self.chat_history = f.read()

            response = self.chatbot.get_arfie_response(user_input, self.uploaded_content, self.chat_history)

            with open("chat history.txt", "a", encoding="utf-8") as f:
                f.write(f"arfie: {response}\n")

        except Exception as e:
            response = f"sorry, something went wrong: {e}"

        self.textbox.append(f"arfie: {response}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
# This code is a simple chatbot application using PySide6 and Cohere's AI model.
# It allows users to chat with the AI, upload text files, and view chat history.